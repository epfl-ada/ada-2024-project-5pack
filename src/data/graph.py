import networkx as nx


def _get_edge_weights(graph_data: dict, dataframe_key: str) -> dict[tuple[str, str], int]:
	"""
	Return a dictionary where the keys are tuples representing an edge (u, v) and values are the edges weights.
	The weight of an edge (u, v) is the number of times users went from u to v in their path.
	If a user clicked on '<', the article that was discarded does not contribute to the weight.
	"""
	assert dataframe_key in graph_data

	# Initialize all edge weights to zero
	edge_weights = {link_tuple: 0 for link_tuple in graph_data["links"][["source_name", "target_name"]].apply(tuple, axis=1)}

	edge_weights |= {(source, "<"): 0 for source in graph_data["articles"]["name"]}

	# Increase edge weights
	unrecognized_edges: set[tuple[str, str]] = set()
	for _, row in graph_data[dataframe_key].iterrows():
		path = row["path"]
		clean_path = []  # Path without '<'
		for element in path:
			if element == "<":
				edge_weights[(clean_path[-1], "<")] += 1
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
		print(f"Note that the following edges are present in '{dataframe_key}' but not in 'links'")
		print(unrecognized_edges)

	assert sum(edge_weights.values()) == sum(graph_data[dataframe_key]["path"].apply(len)) - sum(
		graph_data[dataframe_key]["path"].apply(lambda list: list.count("<"))
	) - len(graph_data[dataframe_key])

	return edge_weights


def extract_players_graph(graph_data: dict, finished=True) -> nx.DiGraph:
	"""
	Generates a directed graph from the given dataframe (either 'paths_finished' or 'paths_unfinished').
	The nodes of the graph are the articles.
	The weight of the edges of the graph represents the number of times users went from one article to another.
	A special node '<' is created.
	The weight of an edge from u to '<' represents the number of times users clicked on the back button after visiting u.
	"""
	graph = nx.DiGraph()

	# Add nodes to graph
	graph.add_node("<")
	graph.add_nodes_from(graph_data["articles"]["name"])

	# Add edges to graph
	edge_weights = _get_edge_weights(graph_data, "paths_finished" if finished else "paths_unfinished")
	for (source, dest), count in edge_weights.items():
		graph.add_edge(source, dest, weight=count)

	# TODO: see why this assertion is needed and why it does not pass
	# assert(abs(graph.number_of_edges() - len(graph_data['links']) - len(graph_data['articles'])) <= 4)

	return graph
