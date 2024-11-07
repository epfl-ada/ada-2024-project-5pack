from functools import cache
from urllib.parse import unquote
from datetime import datetime

import os
import numpy as np
import pandas as pd
import networkx as nx

PATHS_AND_GRAPH_FOLDER = "data/wikispeedia_paths-and-graph"
WP_SOURCE_DATA_FOLDER = "data/wpcd/wp"


def load_data_from_file(file_path):
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


@cache
def load_graph_data():
	if not os.path.isdir(PATHS_AND_GRAPH_FOLDER):
		raise ValueError("The data is not setup correctly, please follow the instructions in `data/README.md`.")

	graph_data = {}

	print("loading raw data from tsv files...")
	with os.scandir(PATHS_AND_GRAPH_FOLDER) as it:
		for entry in it:
			if (entry.name.endswith(".tsv") or entry.name.endswith(".txt")) and entry.is_file():
				key = entry.name.split(".")[0]
				graph_data[key] = load_data_from_file(entry.path)

	print("formatting articles...")
	graph_data["articles"]["name"] = graph_data["articles"]["article"].apply(unquote)
	graph_data["articles"].drop(columns=["article"], inplace=True)

	print("formatting categories...")
	graph_data["categories"]["article_name"] = graph_data["categories"]["article"].apply(unquote)
	graph_data["categories"].drop(columns=["article"], inplace=True)

	print("formatting links...")
	graph_data["links"]["source_name"] = graph_data["links"]["linkSource"].apply(unquote)
	graph_data["links"]["target_name"] = graph_data["links"]["linkTarget"].apply(unquote)
	graph_data["links"].drop(columns=["linkSource", "linkTarget"], inplace=True)

	print("formatting paths...")
	for k in ["paths_finished", "paths_unfinished"]:
		graph_data[k]["path"] = graph_data[k]["path"].apply(lambda path: path.split(";"))
		graph_data[k]["source"] = graph_data[k]["path"].apply(lambda path: path[0])
		graph_data[k]["datetime"] = graph_data[k]["timestamp"].astype(int).apply(datetime.fromtimestamp)

	graph_data["paths_finished"]["target"] = graph_data["paths_finished"]["path"].apply(lambda path: path[-1])

	print("formatting distance matrix...")
	graph_data["shortest-path-distance-matrix"] = np.array(
		list(
			map(
				lambda s: np.array([*map(lambda e: np.nan if e == "_" else int(e), list(s))]),
				graph_data["shortest-path-distance-matrix"].value.values,
			)
		)
	)

	assert graph_data["shortest-path-distance-matrix"].shape == (len(graph_data["articles"]), len(graph_data["articles"]))

	print("building graph...")
	wikispeedia_graph = nx.DiGraph()
	wikispeedia_graph.add_nodes_from(graph_data["articles"].name)
	wikispeedia_graph.add_edges_from(graph_data["links"].values)

	graph_data["graph"] = wikispeedia_graph

	return graph_data
