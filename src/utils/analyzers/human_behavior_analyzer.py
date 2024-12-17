import plotly.express as px
import numpy as np
import pandas as pd


def game_stats_comparison_df(graph_data):
	paths_info = graph_data["paths_finished"][["hashedIpAddress", "timestamp", "path_length", "source", "target"]].copy()
	paths_info.sort_values(by="timestamp", inplace=True)

	# only take first path of every player
	paths_info = paths_info.groupby(["source", "target", "hashedIpAddress"], as_index=False).first()

	paths_info = paths_info[["source", "target", "path_length"]]
	paths_info = paths_info.groupby(["source", "target"]).describe()

	paths_info["shortest_distance"] = graph_data["shortest-path-distance-matrix"]["optimal_path_length"]

	# remove one special case where shortest_distance is nan
	paths_info = paths_info[lambda df: ~df.shortest_distance.isna()]
	return paths_info


def game_stats_simple_join(graph_data):
	paths_info = graph_data["paths_finished"][["hashedIpAddress", "timestamp", "path_length", "source", "target"]].copy()
	paths_info.sort_values(by="timestamp", inplace=True)

	# only take first path of every player
	paths_info = paths_info.groupby(["source", "target", "hashedIpAddress"], as_index=False).first()

	paths_info = paths_info[["source", "target", "path_length"]]

	stats = (
		graph_data["shortest-path-distance-matrix"]
		.merge(paths_info, how="left", left_index=True, right_on=["source", "target"])
		.dropna()
	)
	stats = stats[stats["optimal_path_length"] > 0]
	stats

	# remove outliers
	stats = stats[stats.path_length < 100]

	return stats


def game_stats_survival_plot(stats):
	data = stats["path_length"] / stats["optimal_path_length"]
	mean_value = data.mean()
	sorted_data = np.sort(data)
	survival_prob = np.linspace(1, 0, len(data))

	df = pd.DataFrame({"length_ratio": sorted_data, "survival": survival_prob})

	figure = px.line(df, x="length_ratio", y="survival")

	figure.add_vline(
		x=mean_value, line_dash="dash", line_color="red", annotation_text=f"Mean: {mean_value:.2f}", annotation_position="top"
	)

	figure.update_layout(
		xaxis_title="Ratio of path length over optimal path length",
		yaxis_title="Density",
		xaxis=dict(range=[0, 15]),
		yaxis=dict(type="log", tickvals=[1, 0.1, 0.01, 0.001], ticktext=["1", "0.1", "0.01", "0.001"]),
		title="Distribution of the optimality ratio in the game data",
	)

	return figure
