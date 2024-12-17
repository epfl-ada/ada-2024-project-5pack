from typing import Any

import networkx as nx
import pandas as pd

Node = str
Edge = tuple[str, str]


def _get_edge_weights(
	graph_data: dict[str, Any],
	paths: pd.DataFrame,
) -> tuple[dict[Edge, int], set[Edge]]:
	"""Return a dictionary where the keys are tuples representing an edge (u, v) and values are the edges weights.

	The weight of an edge (u, v) is the number of times users went from u to v in their path.
	If a user clicked on '<', the article that was discarded does not contribute to the weight.

	Also returns the set of edges that are present in 'paths_(un)finished.tsv' but not in 'links.tsv'
	"""
	# Initialize all edge weights to zero
	edge_weights = {
		link_tuple: 0
		for link_tuple in graph_data["links"][["source_name", "target_name"]].apply(
			tuple,
			axis=1,
		)
	}

	# Increase edge weights
	unrecognized_edges: set[tuple[str, str]] = set()
	for _, row in paths.iterrows():
		path = row["path"]
		clean_path = []  # Path without '<'
		for element in path:
			if element == "<":
				clean_path.pop()
			else:
				clean_path.append(element)

		for i in range(1, len(clean_path)):
			edge = (clean_path[i - 1], clean_path[i])
			if edge not in edge_weights:
				unrecognized_edges.add(edge)
				edge_weights[edge] = 0

			edge_weights[edge] += 1

	if len(unrecognized_edges) > 0:
		print(
			f"Note that {len(unrecognized_edges)} edges are present in 'paths_(un)finished.tsv' but not in 'links.tsv':",
		)
		print(unrecognized_edges)

	assert sum(edge_weights.values()) == sum(paths["path"].apply(len)) - 2 * sum(
		paths["path"].apply(lambda list: list.count("<")),
	) - len(paths)

	return edge_weights, unrecognized_edges


def extract_players_graph(graph_data: dict, paths: pd.DataFrame) -> nx.DiGraph:
	"""Generate a directed graph from the provided graph_data.

	- Nodes: Each node in the graph represents an article.
	- Edges: A directed edge (u, v) exists if there is a hyperlink from article u to article v.
	- Edge Weights: The weight of an edge (u, v) represents the number of times users navigated from article u to article v.

	Parameters
	----------
	- graph_data: The graph data
	- finished_paths: Whether to use 'paths_finished' or 'paths_unfinished'

	Returns
	-------
	- The computed graph

	"""
	graph = nx.DiGraph()

	# Add nodes to graph
	graph.add_nodes_from(graph_data["articles"]["name"])

	# Add edges to graph
	edge_weights, unrecognized_edges = _get_edge_weights(graph_data, paths)
	for (source, dest), count in edge_weights.items():
		graph.add_edge(source, dest, weight=count)

	assert graph.number_of_nodes() == len(graph_data["articles"])
	assert graph.number_of_edges() == len(graph_data["links"]) + len(unrecognized_edges)

	return graph
