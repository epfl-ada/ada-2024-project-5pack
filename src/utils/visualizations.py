"""Visualization Module.

------------------
Creates visualizations for Wikispeedia analysis results
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns
from matplotlib import gridspec


class WikispeediaVisualizer:
	def __init__(self, style="whitegrid"):
		"""Initialize visualizer."""
		sns.set_theme()
		sns.set_style(style)

		self.colors = ["#2ecc71", "#e74c3c", "#3498db", "#f1c40f"]

	def plot_navigation_patterns(self, paths_df: pd.DataFrame, stats):
		"""Create visualization of navigation patterns.

		Parameters
		----------
		paths_df : pd.DataFrame
		    DataFrame containing path information
		stats : dict
		    Dictionary containing path statistics

		"""
		figure = plt.figure(figsize=(20, 15))
		gs = gridspec.GridSpec(2, 2)

		# 1. Success Rate by Strategy
		ax1 = plt.subplot(gs[0, 0])
		success_rates = stats["path_stats"]["success_by_strategy"]
		pd.Series(success_rates).plot(kind="bar", ax=ax1, color=self.colors)
		ax1.set_title("Success Rate by Navigation Strategy")
		ax1.set_ylabel("Success Rate")

		# 2. Path Length Distribution
		ax2 = plt.subplot(gs[0, 1])
		paths_df["path_length"].hist(ax=ax2, bins=30)
		ax2.set_title("Path Length Distribution")
		ax2.set_xlabel("Path Length")

		# 3. Temporal Patterns
		ax3 = plt.subplot(gs[1, 0])
		hourly_success = pd.Series(stats["time_patterns"]["hourly_success_rate"])
		hourly_success.plot(ax=ax3)
		ax3.set_title("Success Rate by Hour")
		ax3.set_xlabel("Hour of Day")
		ax3.set_ylabel("Success Rate")

		# 4. Strategy Distribution
		ax4 = plt.subplot(gs[1, 1])
		strategy_counts = paths_df["strategy"].value_counts()
		ax4.pie(
			strategy_counts,
			labels=strategy_counts.index,
			autopct="%1.1f%%",
			colors=self.colors,
		)
		ax4.set_title("Navigation Strategy Distribution")

		plt.tight_layout()
		return figure

	def plot_network_structure(self, graph: nx.Graph, centrality_metrics):
		"""Visualize network structure and metrics.

		Parameters
		----------
		graph : networkx.Graph
		    NetworkX graph object
		centrality_metrics : dict
		    Dictionary containing centrality metrics

		"""
		figure = plt.figure(figsize=(15, 12))
		gs = gridspec.GridSpec(2, 2)

		# 1. Degree Distribution
		ax1 = plt.subplot(gs[0, 0])
		degrees = [d for n, d in graph.degree()]
		ax1.hist(degrees, bins=50, color=self.colors[0])
		ax1.set_title("Node Degree Distribution")
		ax1.set_xlabel("Degree")
		ax1.set_ylabel("Count")

		# 2. PageRank Distribution
		ax2 = plt.subplot(gs[0, 1])
		if "pagerank" in centrality_metrics:
			pageranks = list(centrality_metrics["pagerank"].values())
			ax2.hist(pageranks, bins=50, color=self.colors[1])
			ax2.set_title("PageRank Distribution")
			ax2.set_xlabel("PageRank")

		# 3. Top Hubs
		ax3 = plt.subplot(gs[1, :])
		if "degree" in centrality_metrics:
			top_degrees = pd.Series(centrality_metrics["degree"]).sort_values(
				ascending=False,
			)[:20]
			top_degrees.plot(kind="bar", ax=ax3, color=self.colors[2])
			ax3.set_title("Top 20 Hub Articles by Degree")
			ax3.set_xlabel("Article")
			ax3.set_ylabel("Degree")
			plt.xticks(rotation=45, ha="right")

		plt.tight_layout()
		return figure

	def plot_model_performance(self, model_results: dict):
		"""Visualize model performance metrics.

		Parameters
		----------
		model_results : dict
		    Dictionary containing model results

		"""
		figure = plt.figure(figsize=(15, 10))
		gs = gridspec.GridSpec(2, 2)

		# 1. Feature Importance
		ax1 = plt.subplot(gs[0, :])
		if "feature_importance" in model_results:
			importance_df = pd.DataFrame(model_results["feature_importance"])
			importance_df.sort_values("coefficient", key=abs, ascending=True).plot(
				kind="barh",
				y="coefficient",
				x="feature",
				ax=ax1,
				color=self.colors[0],
			)
			ax1.set_title("Feature Importance")

		# 2. Model Performance Metrics
		ax2 = plt.subplot(gs[1, 0])
		if "cv_scores" in model_results:
			ax2.bar(
				["CV Score"],
				[model_results["cv_scores"]["mean"]],
				yerr=[model_results["cv_scores"]["std"]],
				color=self.colors[1],
			)
			ax2.set_title("Cross-validation Score")
			ax2.set_ylim(0, 1)

		# 3. ROC AUC
		ax3 = plt.subplot(gs[1, 1])
		if "roc_auc" in model_results:
			ax3.text(
				0.5,
				0.5,
				f"ROC AUC: {model_results['roc_auc']:.3f}",
				horizontalalignment="center",
				fontsize=14,
			)
			ax3.axis("off")

		plt.tight_layout()
		return figure

	def plot_temporal_patterns(self, time_patterns: dict):
		"""Visualize temporal patterns.

		Parameters
		----------
		time_patterns : dict
		    Dictionary containing temporal analysis results

		"""
		figure = plt.figure(figsize=(15, 10))
		gs = gridspec.GridSpec(2, 1)

		# 1. Daily Success Rate
		ax1 = plt.subplot(gs[0])
		daily_success = pd.Series(time_patterns["daily_success_rate"])
		daily_success.plot(kind="bar", ax=ax1, color=self.colors[0])
		ax1.set_title("Success Rate by Day of Week")
		ax1.set_ylabel("Success Rate")

		# 2. Hourly Success Rate
		ax2 = plt.subplot(gs[1])
		hourly_success = pd.Series(time_patterns["hourly_success_rate"])
		hourly_success.plot(ax=ax2, color=self.colors[1], marker="o")
		ax2.set_title("Success Rate by Hour")
		ax2.set_xlabel("Hour of Day")
		ax2.set_ylabel("Success Rate")

		plt.tight_layout()
		return figure
