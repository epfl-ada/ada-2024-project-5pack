import warnings

import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import ConstantInputWarning, spearmanr

from src.utils.data import explode_paths


def pagerank(graph: nx.Graph) -> pd.DataFrame:
	# Pagerank algorithm using the graph of articles (without weights)
	pagerank_scores = nx.pagerank(graph, alpha=0.85)
	graph_pagerank = pd.DataFrame(
		list(pagerank_scores.items()),
		columns=["Article", "Pagerank"],
	)
	# Normalizing
	graph_pagerank["Generality_score"] = (graph_pagerank["Pagerank"] - graph_pagerank["Pagerank"].min()) / (graph_pagerank["Pagerank"].max() - graph_pagerank["Pagerank"].min())
	return graph_pagerank


def average_on_paths(n_bins: int, paths: pd.DataFrame, graph_pagerank:pd.DataFrame) -> tuple[np.array, np.array]:

	article_gen_score = graph_pagerank.set_index('Article')['Generality_score']

	# Get path finished and filter so that we only keep short paths (other are noise)
	paths = paths[paths['path'].apply(len) <= 20]
	#Remove < from path (but keep the articles that the person attempted to go to)
	paths['path'] = paths['path'].apply(lambda x: [u for u in x if u != '<'])


	paths['Generality_score'] = paths['path'].apply(
    lambda path: article_gen_score.loc[path].tolist())
	scores_bins = [[] for _ in range(n_bins + 1)]

	# We have bins for every steps then add the scores that fall in that bin
	# For ex. if the path is of length 5 we will add step 1 to 1st bin, step 2 to 3rd, etc...
	for _, path in paths.iterrows():
		# This is the previously computed path of generality scores (for each step)
		generality_scores = path["Generality_score"]
		bins = np.linspace(0, 1, len(generality_scores))

		for fraction, score in zip(bins, generality_scores):
			bin_index = int(fraction * n_bins)  # Find bin where this falls
			scores_bins[bin_index].append(score)

	scores = [np.mean(scores) for scores in scores_bins]

	percent = [(100 * i / n_bins) for i in range(n_bins + 1)]

	return scores, percent


def compute_correlation_between_rank_and_path_length(
	path_group: pd.DataFrame,
) -> pd.Series:
	path_group = path_group[["rank", "path_length"]]
	count = len(path_group)
	corr_coeff = np.nan
	cov = np.nan
	res, pvalue = np.nan, np.nan

	# correlation-related values are not defined when there is only one observation
	if count > 1:
		with warnings.catch_warnings():
			warnings.simplefilter(action="ignore", category=RuntimeWarning)
			corr_coeff = np.corrcoef(path_group.values, rowvar=False)[0, 1]
			cov = np.cov(path_group.values, rowvar=False)[0, 1]
		with warnings.catch_warnings():
			warnings.simplefilter(action="ignore", category=ConstantInputWarning)
			res, pvalue = spearmanr(path_group.values)

	vals = pd.Series(
		dict(
			corr_coeff=corr_coeff,
			cov=cov,
			spearman=res,
			pvalue=pvalue,
			count=count,
		),
	)

	return vals


def rank_length_analysis(paths: pd.DataFrame) -> pd.DataFrame:
	"""Compute the correlation between the columns `rank` and `path_length` for distinct pair of articles.

	Args:
			paths: pd.DataFrame, either paths_finished or paths_unfinished as returned by `load_graph_data`

	Returns:
			corr_data	pd.DataFrame, correlation data. One pair of articles per row.
			The correlation coefficient is in the column `correlation_coefficient` and the column
			`count` is the number of times the given pair was found.

	"""
	# We attempt to discriminate games were the player might not have been playing seriously because they
	# would bring a significant unbalance to our dataset
	PATH_LENGTH_THRESHOLD = 50

	corr_data = (
		explode_paths(paths, PATH_LENGTH_THRESHOLD)
		.groupby(["source", "target"])[["source", "target", "rank", "path_length"]]
		.apply(compute_correlation_between_rank_and_path_length)
		.reset_index()
	)

	return corr_data


def explode_paths_and_compute_all_scores(paths: pd.DataFrame, compute: bool = False, write: bool = False) -> pd.DataFrame:
	if compute:
		from src.utils.data import explode_paths
		df = explode_paths(paths, clear_backticks=True)[['source', 'target', 'path', 'path_length', 'rank']][
			lambda x: x['source'] != "<"
		]
		df['sub_path'] = df.apply(
			func=lambda entry: entry['path'][entry['rank']:],
			axis='columns',
		)
		hur, tlr, sis = 'hub_usage_ratio', 'top_link_ratio', 'semantic_increase_score'
		from src.utils.strategies.hub_focused_strategy import compute_hub_usage_ratio
		df[hur] = df['sub_path'].apply(func=compute_hub_usage_ratio)
		from src.utils.strategies.semantic_strategy import semantic_increase_score
		df[sis] = df['sub_path'].apply(func=semantic_increase_score)
		from src.utils.strategies.link_strategy import top_link_ratio
		df[tlr] = df['sub_path'].apply(func=top_link_ratio)
	else:
		df = pd.read_csv('./data/generated/strategy_comparison/exploded_paths_data.csv')
	if write:
		df.to_csv('./data/generated/strategy_comparison/exploded_paths_data.csv')
	return df

def compute_correlation_between_scores_and_game_length(path_group: pd.DataFrame) -> pd.Series:
	count = len(path_group)
	res = {'count': count }
	import warnings
	from scipy.stats import spearmanr, ConstantInputWarning
	for score in ['hub_usage_ratio', 'top_link_ratio', 'semantic_increase_score']:
		corr_coeff, pvalue = np.nan, np.nan
		if count > 1:
			with warnings.catch_warnings():
				warnings.simplefilter(action="ignore", category=ConstantInputWarning)
				corr_coeff, pvalue = spearmanr(path_group[[score, 'path_length']].values)
		res.update({score + "_corr_coeff": corr_coeff, score + "_pvalue": pvalue})
	return pd.Series(res)

def scores_vs_length_analysis(graph_data, compute: bool = False, write: bool = False) -> dict[str, pd.DataFrame]:
	df_exploded = explode_paths_and_compute_all_scores(graph_data['paths_finished'])
	if compute:
		df = df_exploded.groupby(['source', 'target']).apply(compute_correlation_between_scores_and_game_length).reset_index()
	else:
		df = pd.read_csv('./data/generated/strategy_comparison/general_scores.csv')
	if write:
		df.to_csv('./data/generated/strategy_comparison/general_scores.csv')
	scores_dfs = {}
	for score in ['hub_usage_ratio', 'top_link_ratio', 'semantic_increase_score']:
		scores_dfs[score] = df[['source', 'target', 'count']].copy()
		scores_dfs[score]['spearman'] = df[score + '_corr_coeff']
		scores_dfs[score]['pvalue'] = df[score + '_pvalue']
	return scores_dfs