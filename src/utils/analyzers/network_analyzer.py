"""Network Analysis Module.

---------------------
Analyzes the Wikipedia article network structure, including:
- Hub identification
- Path analysis
- Network metrics calculation
- Community detection
"""

import networkx as nx

from src.utils import logger

SAMPLING_THRESHOLD = 1_000


class NetworkAnalyzer:
	def __init__(self):
		"""Initialize NetworkAnalyzer."""
		self.graph = None
		self.hub_scores = None
		self.top_hubs = None
		self.centrality_metrics = {}

	def build_graph(self, links_df):
		"""Build network graph from links data.

		Parameters
		----------
		links_df : pd.DataFrame
		    DataFrame containing source and target article links

		"""
		try:
			logger.info("Building network graph...")
			self.graph = nx.from_pandas_edgelist(
				links_df,
				"linkSource",
				"linkTarget",
				create_using=nx.DiGraph(),
			)
			logger.info(
				f"Built graph with {self.graph.number_of_nodes()} nodes and " f"{self.graph.number_of_edges()} edges",
			)

		except Exception as e:
			logger.error(f"Error building graph: {e!s}")
			raise Exception(f"Graph construction failed: {e!s}")

	def compute_network_metrics(self):
		"""Compute basic network metrics.

		Returns
		-------
		dict
		    Dictionary containing network metrics

		"""
		try:
			logger.info("Computing network metrics...")

			metrics = {
				"basic_metrics": {
					"nodes": self.graph.number_of_nodes(),
					"edges": self.graph.number_of_edges(),
					"density": nx.density(self.graph),
					"avg_clustering": nx.average_clustering(self.graph.to_undirected()),
					"strongly_connected_components": nx.number_strongly_connected_components(
						self.graph,
					),
				},
			}

			# Compute average path length
			try:
				largest_cc = max(nx.strongly_connected_components(self.graph), key=len)
				subgraph = self.graph.subgraph(largest_cc)
				metrics["basic_metrics"]["avg_path_length"] = nx.average_shortest_path_length(subgraph)
			except Exception as e:
				logger.warning(f"Could not compute average path length: {e!s}")
				metrics["basic_metrics"]["avg_path_length"] = None

			return metrics

		except Exception as e:
			logger.error(f"Error computing network metrics: {e!s}")
			raise Exception(f"Network metrics computation failed: {e!s}")

	def identify_hubs(self, top_n=20):
		"""Identify hub articles using PageRank.

		Parameters
		----------
		top_n : int
		    Number of top hubs to identify

		"""
		try:
			logger.info("Identifying hub articles...")

			# Compute PageRank
			self.hub_scores = nx.pagerank(self.graph)

			# Get top hubs
			self.top_hubs = dict(
				sorted(self.hub_scores.items(), key=lambda x: x[1], reverse=True)[:top_n],
			)

			logger.info(f"Identified top {top_n} hub articles")

		except Exception as e:
			logger.error(f"Error identifying hubs: {e!s}")
			raise Exception(f"Hub identification failed: {e!s}")

	def compute_centrality_metrics(self):
		"""Compute various centrality metrics."""
		try:
			logger.info("Computing centrality metrics...")

			# Degree centrality
			self.centrality_metrics["degree"] = nx.degree_centrality(self.graph)

			# Betweenness centrality (computed on a sample for large graphs)
			if self.graph.number_of_nodes() > SAMPLING_THRESHOLD:
				self.centrality_metrics["betweenness"] = nx.betweenness_centrality(
					self.graph,
					k=SAMPLING_THRESHOLD,  # Use sampling
				)
			else:
				self.centrality_metrics["betweenness"] = nx.betweenness_centrality(
					self.graph,
				)

			# PageRank (if not already computed)
			if not self.hub_scores:
				self.hub_scores = nx.pagerank(self.graph)
			self.centrality_metrics["pagerank"] = self.hub_scores

			logger.info("Computed centrality metrics successfully")

		except Exception as e:
			logger.error(f"Error computing centrality metrics: {e!s}")
			raise Exception(f"Centrality computation failed: {e!s}")
