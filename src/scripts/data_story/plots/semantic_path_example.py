from src.utils.strategies.semantic_strategy import get_semantic_similarities
import plotly.graph_objs as go


def generate_plot(data, output_dir):
	fig = semantic_path_example()
	fig.write_html(output_dir / "semantic_path_example.html", include_plotlyjs=True, full_html=True)


def semantic_path_example() -> go:
	path = ["Internet", "North_America", "South_America", "Peru", "Alpaca"]
	similarities = get_semantic_similarities(path, path[-1])

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=path, y=similarities, mode="lines+markers", name="Semantic Similarities"))

	fig.update_layout(
		title=f"Semantic Similarity Evolution for a Path from '{path[0]}' to '{path[-1]}'",
		xaxis_title="Path",
		yaxis_title="Similarity",
	)
	return fig
