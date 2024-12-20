from functools import cache

import pandas as pd
import statsmodels.formula.api as smf
from scipy.stats import zscore
from statsmodels.regression.mixed_linear_model import MixedLMResults

from src.utils.data import load_graph_data
from src.utils.metrics import pagerank
from src.utils.strategies.backtrack_strategy import compute_backtrack_ratio
from src.utils.strategies.hub_focused_strategy import compute_hub_usage_ratio
from src.utils.strategies.link_strategy import get_click_positions, get_probability_link, top_link_ratio
from src.utils.strategies.semantic_strategy import semantic_increase_score


@cache
def get_strategies_scores() -> pd.DataFrame:
	"""
	Computes and returns a DataFrame containing various strategy scores for all the finished paths.

	Note that this function will ignore paths that are shorter than two articles, and paths that took more than 15 min to complete

	Returns:
	    pd.DataFrame: A DataFrame containing the filtered paths and their computed strategy scores.
	              The returned data frame contains the columns 'path', 'target', 'duration_in_seconds',
	              'semantic_increase_score', 'top_link_ratio' and 'hub_ratio'.
	"""
	graph_data = load_graph_data()
	paths_scores = graph_data["paths_finished"][["path", "target", "duration_in_seconds"]].copy()
	paths_scores = paths_scores[paths_scores["path"].apply(len) > 2]  # Remove paths that are too short
	paths_scores = paths_scores[paths_scores["duration_in_seconds"] < 1000]  # Remove paths that took more than 15 min to finish

	# Compute the strategies scores
	paths_scores["semantic_increase_score"] = paths_scores["path"].apply(semantic_increase_score)
	paths_scores["top_links_ratio"] = paths_scores["path"].apply(top_link_ratio)
	paths_scores["backtrack_ratio"] = paths_scores["path"].apply(compute_backtrack_ratio)
	paths_scores["hub_ratio"] = paths_scores["path"].apply(compute_hub_usage_ratio)
	return paths_scores


def get_normalized_strategies_scores() -> pd.DataFrame:
	"""
	Same as get_strategies_scores(), but the scores and ratios are normalized using z-score normalization
	"""
	paths_scores = get_strategies_scores()

	# Normalize the scores using z-score normalization
	paths_scores["semantic_increase_score"] = zscore(paths_scores["semantic_increase_score"])
	paths_scores["top_links_ratio"] = zscore(paths_scores["top_links_ratio"])
	paths_scores["backtrack_ratio"] = zscore(paths_scores["backtrack_ratio"])
	paths_scores["hub_ratio"] = zscore(paths_scores["hub_ratio"])

	return paths_scores


def perform_mixed_linear_regression() -> MixedLMResults:
	"""
	Perform a mixed linear regression on strategy scores.

	Returns:
	    MixedLMResults: The results of the fitted mixed linear model.
	"""
	paths_scores = get_strategies_scores()
	model = smf.mixedlm(
		"duration_in_seconds ~ semantic_increase_score + top_links_ratio + hub_ratio + backtrack_ratio",
		data=paths_scores,
		groups=paths_scores["target"],
	)
	return model.fit()


def perform_backward_selection(data: pd.DataFrame) -> MixedLMResults:
	"""
	Runs the backward selection algorithm to select the most important features
	"""
	paths_scores = get_strategies_scores()

	terms = [
		"semantic_increase_score",
		"top_links_ratio",
		"hub_ratio",
		"backtrack_ratio",
		"semantic_increase_score:top_links_ratio",
		"semantic_increase_score:hub_ratio",
		"semantic_increase_score:backtrack_ratio",
		"top_links_ratio:hub_ratio",
		"top_links_ratio:backtrack_ratio",
		"hub_ratio:backtrack_ratio",
		"semantic_increase_score:top_links_ratio:hub_ratio",
		"semantic_increase_score:top_links_ratio:backtrack_ratio",
		"semantic_increase_score:hub_ratio:backtrack_ratio",
		"top_links_ratio:hub_ratio:backtrack_ratio",
		"semantic_increase_score:top_links_ratio:hub_ratio:backtrack_ratio",
	]

	while True:
		formula = f"duration_in_seconds ~ {' + '.join(terms)}"
		model = smf.mixedlm(formula, data=paths_scores, groups=paths_scores["target"])
		result = model.fit()
  
		worst_feature = result.pvalues.iloc[1:-1].idxmax()  # Exclude the Intercept and Group Var
		max_pvalue = result.pvalues.max()

		if len(terms) <= 1 or max_pvalue < 0.0002:
			break

		print(f"Removing '{worst_feature}' with p-value {max_pvalue}")
		terms.remove(worst_feature)

	return result


def build_comparison_df(
	graph_data, top_hubs=200, threshold_semantic=0.8, threshold_link=0.8, threshold_backtrack=0.1, threshold_hub=0.8
):
	graph_pagerank = pagerank(graph_data["graph"])
	article_gen_score = graph_pagerank.set_index("Article")["Generality_score"]
	sorted_scores = article_gen_score.sort_values(ascending=False)
	score_threshold = sorted_scores.iloc[top_hubs]

	article_gen_score = graph_pagerank.set_index("Article")["Generality_score"]

	# Remove < from path (but keep the articles that the person attempted to go to)
	graph_data["paths_finished"]["backtrack_ratio"] = graph_data["paths_finished"]["path"].apply(compute_backtrack_ratio)
	graph_data["paths_unfinished"]["backtrack_ratio"] = graph_data["paths_unfinished"]["path"].apply(compute_backtrack_ratio)
	graph_data["paths_finished"]["path_clean"] = graph_data["paths_finished"]["path"].apply(lambda x: [u for u in x if u != "<"])
	graph_data["paths_unfinished"]["path_clean"] = graph_data["paths_finished"]["path"].apply(
		lambda x: [u for u in x if u != "<"]
	)

	fin_list = []

	for _, row in graph_data["paths_finished"].iterrows():
		path = row["path_clean"]
		time = row["duration_in_seconds"]
		click_positions = get_click_positions(pd.DataFrame({"path": [path]}))
		prob = get_probability_link(click_positions)
		semantic = semantic_increase_score(path, row["target"])
		max_gen = article_gen_score.loc[path].max()
		if len(path) < 4 or semantic < 0 or len(path) > 100:
			continue  # A path too short, too long, or that progressively gets further from target doesn't make sense and will be ignored
		fin_list.append(
			{
				"source": row["source"],
				"target": row["target"],
				"path": path,
				"time": time,
				"finished": True,
				"link_percentage": prob,
				"num_clicks": len(path),
				"top_link_usage": prob > threshold_link,
				"semantic": semantic > threshold_semantic,
				"max_generality": max_gen > score_threshold,
				"hub_usage": compute_hub_usage_ratio(path) > threshold_hub,
				"backtrack": row["backtrack_ratio"] > threshold_backtrack,
			}
		)

	finished = pd.DataFrame(fin_list)

	unfin_list = []
	for _, row in graph_data["paths_unfinished"].iterrows():
		path = row["path_clean"]
		time = row["duration_in_seconds"]
		click_positions = get_click_positions(pd.DataFrame({"path": [path]}))
		prob = get_probability_link(click_positions)
		try:
			semantic = semantic_increase_score(path, row["target"])
		except KeyError:
			print(f"Warning: {row['target']} was not found in the list of documents")
			continue

		max_gen = article_gen_score.loc[path].max()
		if len(path) < 4 or semantic < 0 or len(path) > 100:
			continue  # A path too short, too long, or that progressively gets further from target doesn't make sense and will be ignored

		unfin_list.append(
			{
				"source": row["source"],
				"target": row["target"],
				"path": path,
				"time": time,
				"finished": False,
				"num_clicks": len(path),
				"top_link_usage": prob > threshold_link,
				"semantic": semantic > threshold_semantic,
				"max_generality": max_gen > score_threshold,
				"hub_usage": compute_hub_usage_ratio(path) > threshold_hub,
				"backtrack": row["backtrack_ratio"] > threshold_backtrack,
			}
		)

	unfinished = pd.DataFrame(unfin_list)

	return finished, unfinished
