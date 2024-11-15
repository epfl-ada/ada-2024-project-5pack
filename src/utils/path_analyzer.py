"""
Path Analysis Module
------------------
Analyzes navigation paths in Wikispeedia, including:
- Path characteristics computation
- Navigation strategy classification
- Path metrics calculation
"""

import pandas as pd

from src.utils import AnalysisError, logger

STRATEGY_THRESHOLDS = {"direct_efficiency": 0.8, "exploratory_backtrack_ratio": 0.3, "hub_usage_threshold": 0.5}


class PathAnalyzer:
	def __init__(self, semantic_analyzer=None, network_analyzer=None):
		"""Initialize PathAnalyzer"""
		self.semantic_analyzer = semantic_analyzer
		self.network_analyzer = network_analyzer

	def analyze_paths(self, paths_finished, paths_unfinished):
		"""Analyze all paths and compute metrics"""
		try:
			logger.info("Starting path analysis...")

			# Add success flag and combine datasets
			paths_finished["success"] = True
			paths_unfinished["success"] = False

			paths_all = pd.concat(
				[
					paths_finished[["hashedIpAddress", "datetime", "duration_in_seconds", "path", "rating", "success"]],
					paths_unfinished[["hashedIpAddress", "datetime", "duration_in_seconds", "path", "success"]],
				]
			)

			# Calculate basic metrics
			paths_all = self.compute_basic_metrics(paths_all)

			# Classify navigation strategies
			paths_all = self.classify_strategies(paths_all)

			logger.info(f"Analyzed {len(paths_all)} paths successfully")
			return paths_all

		except Exception as e:
			logger.error(f"Error in path analysis: {str(e)}")
			raise AnalysisError(f"Path analysis failed: {str(e)}")

	def compute_basic_metrics(self, paths_df):
		"""Compute basic path metrics"""
		try:
			# Existing metrics
			paths_df["path_length"] = paths_df["path"].apply(len)
			paths_df["backtrack_count"] = paths_df["path"].apply(lambda path: sum(1 for p in path if p == "<"))
			paths_df["unique_articles"] = paths_df["path"].apply(lambda path: len(set(p for p in path if p != "<")))
			paths_df["path_efficiency"] = paths_df["unique_articles"] / paths_df["path_length"]
			paths_df["avg_time_per_click"] = paths_df["duration_in_seconds"] / paths_df["path_length"]

			# Add semantic coherence if semantic analyzer is available
			if self.semantic_analyzer is not None:
				paths_df["semantic_coherence"] = paths_df["path"].apply(self.semantic_analyzer.get_path_similarity)
			else:
				logger.warning("No semantic analyzer available, semantic_coherence will not be computed")
				paths_df["semantic_coherence"] = 0.0  # Default value

			return paths_df

		except Exception as e:
			logger.error(f"Error computing basic metrics: {str(e)}")
			raise AnalysisError(f"Basic metrics computation failed: {str(e)}")

	def classify_strategies(self, paths_df):
		"""Classify navigation strategies for each path"""
		try:

			def get_strategy(row):
				# Get thresholds from configuration
				direct_thresh = STRATEGY_THRESHOLDS["direct_efficiency"]
				explore_thresh = STRATEGY_THRESHOLDS["exploratory_backtrack_ratio"]
				hub_thresh = STRATEGY_THRESHOLDS["hub_usage_threshold"]

				# Calculate metrics
				path_length = row["path_length"]
				backtrack_ratio = row["backtrack_count"] / path_length if path_length > 0 else 0

				# Classify strategy
				if row["backtrack_count"] == 0 and row["path_efficiency"] > direct_thresh:
					return "Direct"
				elif backtrack_ratio > explore_thresh:
					return "Exploratory"
				elif "hub_usage_ratio" in row and row["hub_usage_ratio"] > hub_thresh:
					return "Hub-focused"
				else:
					return "Mixed"

			# Add hub usage if network analyzer is available
			if self.network_analyzer and hasattr(self.network_analyzer, "top_hubs"):
				paths_df["hub_usage"] = paths_df["path"].apply(
					lambda path: sum(1 for p in path if p in self.network_analyzer.top_hubs)
				)
				paths_df["hub_usage_ratio"] = paths_df["hub_usage"] / paths_df["path_length"]

			# Classify strategies
			paths_df["strategy"] = paths_df.apply(get_strategy, axis=1)

			return paths_df

		except Exception as e:
			logger.error(f"Error classifying strategies: {str(e)}")
			raise AnalysisError(f"Strategy classification failed: {str(e)}")

	def compute_path_statistics(self, paths_df):
		"""Compute comprehensive path statistics"""
		try:
			stats = {
				"basic_stats": {
					"total_paths": len(paths_df),
					"success_rate": float(paths_df["success"].mean()),
					"avg_path_length": float(paths_df["path_length"].mean()),
					"avg_duration": float(paths_df["duration_in_seconds"].mean()),
					"avg_backtrack_rate": float(paths_df["backtrack_count"].sum() / paths_df["path_length"].sum()),
				},
				"strategy_distribution": paths_df["strategy"].value_counts().to_dict(),
				"success_by_strategy": paths_df.groupby("strategy")["success"].mean().to_dict(),
			}

			return stats

		except Exception as e:
			logger.error(f"Error computing path statistics: {str(e)}")
			raise AnalysisError(f"Statistics computation failed: {str(e)}")

	def analyze_time_patterns(self, paths_df):
		"""Analyze temporal patterns in navigation"""
		try:
			# Extract time components
			paths_df["hour"] = paths_df["datetime"].dt.hour
			paths_df["day_of_week"] = paths_df["datetime"].dt.day_name()

			# Calculate time-based metrics
			time_patterns = {
				"hourly_success_rate": paths_df.groupby("hour")["success"].mean().to_dict(),
				"daily_success_rate": paths_df.groupby("day_of_week")["success"].mean().to_dict(),
				"avg_duration_by_hour": paths_df.groupby("hour")["duration_in_seconds"].mean().to_dict(),
				"avg_duration_by_day": paths_df.groupby("day_of_week")["duration_in_seconds"].mean().to_dict(),
			}

			return time_patterns

		except Exception as e:
			logger.error(f"Error analyzing time patterns: {str(e)}")
			raise AnalysisError(f"Time pattern analysis failed: {str(e)}")
