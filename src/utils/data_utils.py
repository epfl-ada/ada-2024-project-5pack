from functools import cache
from urllib.parse import unquote
from datetime import datetime
from typing import Dict, Union

from src.utils import logger

import os
import numpy as np
import numpy.typing as npt
import pandas as pd
import networkx as nx

PATHS_AND_GRAPH_FOLDER = "data/wikispeedia_paths-and-graph"
WP_SOURCE_DATA_FOLDER = "data/wpcd/wp"


def load_data_from_file(file_path: str) -> pd.DataFrame:
	"""
	Load a data file using the original format and return a DataFrame containing the data.

	Args:
	    file_path (str): the file to get the data from

	Raises:
	    RuntimeError: if the format of the data cannot be resolved

	Returns:
	    pd.DataFramce: the dataframe with the data
	"""
	columns = None
	data = []
	with open(file_path) as file:
		while line := file.readline():
			line = line.rstrip()
			if line.startswith("# FORMAT:") and not columns:
				data_str = line.split("# FORMAT:   ")[1] if line.startswith("# FORMAT:   ") else "value"
				columns = data_str.split("   ")
			elif line.startswith("# FORMAT:"):
				raise RuntimeError()
			elif len(line) > 0 and not line.startswith("#"):
				data_line = line.split("	")
				assert len(data_line) == len(columns)
				data.append(data_line)

	df = pd.DataFrame(data, columns=columns)

	return df


def _index_based_to_df_matrix(index_based_matrix: npt.NDArray, articles: pd.DataFrame, paths: pd.DataFrame) -> pd.DataFrame:
	"""Transform the shortest path distance matrix from the original format to a Dataframe index with article names

	Args:
		index_based_matrix (np.ndarray): index based shortest distance matrix
		articles (pd.DataFrame): articles data with correct order preserved
		paths (pd.DataFrame): realised path data

	Returns:
		pd.DataFrame: the resulting Dataframe indexed with article names
	"""

	articles = articles.reset_index()
	paths = paths.reset_index(names="path_id")

	# compute all source-target pairs from games and
	# "sub-games" derived from paths
	#
	# this is particular avoids a cross join of the articles
	# which will construct a matrix taking a huge place in
	# in memory

	# compute efficiently to avoid huge memory loads
	idx_fn = lambda k: np.stack(np.triu_indices(k, k=1), axis=-1)
	indices = paths.path.map(lambda path: idx_fn(len(path))).values + np.arange(len(paths))
	indices = np.vstack(indices)

	paths_df = paths[["path"]].explode("path")

	pairs_df = pd.concat(
		[paths_df.iloc[indices[:, 0]].reset_index(drop=True), paths_df.iloc[indices[:, 1]].reset_index(drop=True)], axis=1
	).drop_duplicates()

	pairs_df.columns = ["source", "target"]

	matrix = (
		pairs_df.merge(articles, how="inner", left_on="source", right_on="name")
		.merge(articles, how="inner", left_on="target", right_on="name")
		.drop(columns=["name_x", "name_y"])
		.set_index(["source", "target"])
	)

	matrix["optimal_path_length"] = matrix.apply(lambda row: index_based_matrix[row.index_x, row.index_y], axis=1)
	matrix.drop(columns=["index_x", "index_y"], inplace=True)

	return matrix


@cache
def load_graph_data() -> Dict[str, Union[nx.DiGraph, pd.DataFrame, npt.NDArray]]:
	"""Load the original dataset with some preprocessing

	Raises:
		ValueError: if the data is not configured correctly

	Returns:
		dict: a dictionnary with all the data
	"""
	if not os.path.isdir(PATHS_AND_GRAPH_FOLDER):
		raise ValueError("The data is not setup correctly, please follow the instructions in `data/README.md`.")

	graph_data = {}

	logger.info("loading raw data from tsv files...")
	with os.scandir(PATHS_AND_GRAPH_FOLDER) as it:
		for entry in it:
			if (entry.name.endswith(".tsv") or entry.name.endswith(".txt")) and entry.is_file():
				key = entry.name.split(".")[0]
				graph_data[key] = load_data_from_file(entry.path)

	logger.info("formatting articles...")
	graph_data["articles"]["name"] = graph_data["articles"]["article"].apply(unquote)
	graph_data["articles"].drop(columns=["article"], inplace=True)

	logger.info("formatting categories...")
	graph_data["categories"]["article_name"] = graph_data["categories"]["article"].apply(unquote)
	graph_data["categories"].drop(columns=["article"], inplace=True)

	logger.info("formatting links...")
	graph_data["links"]["source_name"] = graph_data["links"]["linkSource"].apply(unquote)
	graph_data["links"]["target_name"] = graph_data["links"]["linkTarget"].apply(unquote)
	graph_data["links"].drop(columns=["linkSource", "linkTarget"], inplace=True)

	logger.info("formatting paths...")
	for k in ["paths_finished", "paths_unfinished"]:
		graph_data[k]["path"] = graph_data[k]["path"].apply(lambda path: [unquote(p) for p in path.split(";")])
		graph_data[k]["path_length"] = graph_data[k]["path"].apply(lambda path: len(path))
		graph_data[k]["source"] = graph_data[k]["path"].apply(lambda path: path[0])
		graph_data[k]["datetime"] = graph_data[k]["timestamp"].astype(int).apply(datetime.fromtimestamp)
		graph_data[k]["duration_in_seconds"] = graph_data[k]["durationInSec"].astype(np.int64)

		graph_data[k].drop(columns=["durationInSec"], inplace=True)

	graph_data["paths_finished"]["target"] = graph_data["paths_finished"]["path"].apply(lambda path: path[-1])

	logger.info("formatting distance matrix...")
	index_based_matrix = np.array(
		list(
			map(
				lambda s: np.array([*map(lambda e: np.nan if e == "_" else int(e), list(s))]),
				graph_data["shortest-path-distance-matrix"].value.values,
			)
		)
	)

	assert index_based_matrix.shape == (len(graph_data["articles"]), len(graph_data["articles"]))

	logger.info("converting distance matrix to dataframe...")
	all_paths = pd.concat([graph_data["paths_finished"], graph_data["paths_unfinished"]], axis=0)
	graph_data["shortest-path-distance-matrix"] = _index_based_to_df_matrix(
		index_based_matrix, graph_data["articles"].copy(), all_paths
	)

	logger.info("building graph...")
	wikispeedia_graph = nx.DiGraph()
	wikispeedia_graph.add_nodes_from(graph_data["articles"].name)
	wikispeedia_graph.add_edges_from(graph_data["links"].values)
	graph_data["graph"] = wikispeedia_graph

	return graph_data


def explode_paths(paths: pd.DataFrame) -> pd.DataFrame:
	exploded_paths = paths.copy(deep=True)

	# Explode the paths
	exploded_paths["source"] = exploded_paths["path"].map(lambda p: [dict(rank=i, name=node) for i, node in enumerate(p)])
	exploded_paths = exploded_paths.explode("source")

	# Restructure columns
	exploded_paths["rank"] = exploded_paths["source"].apply(lambda src: src["rank"])
	exploded_paths["source"] = exploded_paths["source"].apply(lambda src: src["name"])
	exploded_paths["path_length"] = exploded_paths["path_length"] - exploded_paths["rank"]

	# Remove paths to self
	exploded_paths = exploded_paths[lambda x: x["source"] != x["target"]]

	# Irrelevant rows
	# exploded_paths = exploded_paths[lambda x: x['path_length'] < 20]

	exploded_paths = (
		exploded_paths.groupby(["source", "target"])[["source", "target", "rank", "path_length"]]
		.apply(
			lambda x: pd.Series(
				dict(
					correlation_coefficient=np.corrcoef(
						np.vstack([x["rank"].to_numpy(), x["path_length"].to_numpy()]), rowvar=True
					)[0, 1],
					count=len(x),
				)
			)
		)
		.reset_index()
	)
	return exploded_paths
