"""Hub Strategy Analysis Script.

--------------------------
Analyzes hub usage patterns and optimizes both number of hubs and usage threshold
"""

from functools import cache

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

from src.utils.data import load_graph_data

# Parameters to test
HUB_COUNTS_TO_TEST = [10, 25, 50, 75, 100, 150, 200]  # Different numbers of hubs
THRESHOLDS_TO_TEST = np.linspace(0.1, 0.9, 9)  # Hub usage thresholds


@cache
def get_hub_articles(top_n=50) -> dict:
	"""Get top N hub articles by PageRank score."""
	graph_data = load_graph_data()
	G = graph_data["graph"]

	# Calculate PageRank
	pagerank_scores = nx.pagerank(G)

	# Get distribution of scores to help identify natural cutoffs
	scores = sorted(pagerank_scores.values(), reverse=True)

	# Plot PageRank distribution for first analysis
	if top_n == HUB_COUNTS_TO_TEST[0]:
		plt.figure(figsize=(12, 6))
		plt.plot(scores[:200], linewidth=2, color="#3498db", label="PageRank Score")
		plt.title(
			"PageRank Score Distribution of Articles\n(Top 200 Articles)",
			fontsize=14,
			pad=20,
		)
		plt.xlabel("Article Rank (Most Central to Least Central)", fontsize=12)
		plt.ylabel("PageRank Score", fontsize=12)
		plt.axhline(
			y=scores[top_n],
			color="#e74c3c",
			linestyle="--",
			label=f"Cutoff at top {top_n} articles",
		)
		plt.grid(True, linestyle="--", alpha=0.7)
		plt.legend(fontsize=10, loc="upper right")
		plt.tight_layout()
		plt.savefig("hub_pagerank_distribution.png", dpi=300, bbox_inches="tight")
		plt.close()

	return dict(
		sorted(
			pagerank_scores.items(),
			key=lambda x: x[1],
			reverse=True,
		)[:top_n],
	)


def compute_hub_usage(path: list[str], hub_articles: dict) -> float:
	"""Compute the ratio of hub articles used in a path.

		Args:
			path (list[str]): Navigation path
			hub_articles (dict): Dictionary of hub articles and their scores

		Returns:
	f		loat: Ratio of hub article usage (0 to 1)

	"""
	# Remove backtrack markers
	clean_path = [p for p in path if p != "<"]

	if not clean_path:
		return 0.0

	# Count hub articles used
	hub_count = sum(1 for article in clean_path if article in hub_articles)
	return hub_count / len(clean_path)


def analyze_hub_strategy(paths_df: pd.DataFrame, n_hubs: int, threshold: float) -> dict:
	"""Analyzes navigation success for paths using hub strategy."""
	# Get hub articles for this configuration
	hub_articles = get_hub_articles(n_hubs)

	# Compute hub usage for each path
	paths_df["hub_usage_ratio"] = paths_df["path"].apply(
		lambda p: compute_hub_usage(p, hub_articles),
	)

	# Classify paths using hub strategy
	hub_paths = paths_df[paths_df["hub_usage_ratio"] >= threshold]

	if len(hub_paths) == 0:
		return {
			"n_hubs": n_hubs,
			"threshold": threshold,
			"paths_count": 0,
			"paths_percentage": 0,
			"success_rate": 0,
			"avg_path_length": 0,
		}

	return {
		"n_hubs": n_hubs,
		"threshold": threshold,
		"paths_count": len(hub_paths),
		"paths_percentage": len(hub_paths) / len(paths_df),
		"success_rate": hub_paths["success"].mean(),
		"avg_path_length": hub_paths["path"].apply(len).mean(),
	}


def find_optimal_parameters() -> tuple[pd.DataFrame, pd.Series]:
	"""Grid search for optimal number of hubs and usage threshold."""
	# Load data
	graph_data = load_graph_data()

	# Define success: paths that reached their target
	paths_df = pd.concat(
		[
			graph_data["paths_finished"].assign(success=True),
			graph_data["paths_unfinished"].assign(success=False),
		],
	)

	# Test combinations
	results = [
		analyze_hub_strategy(paths_df, n_hubs, threshold) for n_hubs, threshold in zip(HUB_COUNTS_TO_TEST, THRESHOLDS_TO_TEST)
	]

	results_df = pd.DataFrame(results)

	# Create heatmap of success rates
	plt.figure(figsize=(12, 8))
	heatmap_data = results_df.pivot(
		index="n_hubs",
		columns="threshold",
		values="success_rate",
	)
	sns.heatmap(heatmap_data, annot=True, fmt=".2f", cmap="YlOrRd")
	plt.title("Success Rate by Number of Hubs and Usage Threshold")
	plt.savefig("hub_strategy_heatmap.png")
	plt.close()

	# Create usage percentage heatmap
	plt.figure(figsize=(12, 8))
	usage_data = results_df.pivot(
		index="n_hubs",
		columns="threshold",
		values="paths_percentage",
	)
	sns.heatmap(usage_data, annot=True, fmt=".2%", cmap="YlOrRd")
	plt.title("Percentage of Paths Using Hub Strategy")
	plt.savefig("hub_usage_heatmap.png")
	plt.close()

	# Find optimal parameters
	# Weight success rate more heavily but consider path percentage
	results_df["score"] = results_df["success_rate"] * 0.7 + results_df["paths_percentage"] * 0.3

	optimal_row = results_df.loc[results_df["score"].idxmax()]

	return results_df, optimal_row
