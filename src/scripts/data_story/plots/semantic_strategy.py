import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objs as go

from src.utils.strategies.semantic_strategy import get_semantic_similarities, get_semantic_similarity


def generate_plot(data, output_dir):
	fig_path = semantic_path_example()
	fig_matrix = similarity_matrix_figure()
	fig_path.write_html(output_dir / "semantic_path_example.html", include_plotlyjs=True, full_html=True)
	fig_matrix.write_html(output_dir / "similarity_matrix.html", include_plotlyjs=True, full_html=True)


def semantic_path_example(path: list[str] = None):
	if path is None:
		path = [
			"Cinema_of_the_United_States",
			"20th_century",
			"Vitamin",
			"Anemia",
			"Sickle-cell_disease",
			"Malaria",
			"Yellow_fever",
			"Virus",
			"Common_cold",
		]  # Path 9876

	similarities = get_semantic_similarities(path, path[-1])

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=path, y=similarities, mode="lines+markers", name="Semantic Similarities"))

	fig.update_layout(
		title=f"Semantic Similarity Evolution for a Path from '{path[0]}' to '{path[-1]}'",
		xaxis_title="Path",
		yaxis_title="Similarity",
	)
	return fig


def similarity_matrix_figure():
	articles = ["Bee", "Tree", "Computer", "Linux", "Flower"]

	# Compute the confusion matrix
	confusion_matrix = np.zeros((len(articles), len(articles)))
	for i, article1 in enumerate(articles):
		for j, article2 in enumerate(articles):
			confusion_matrix[i, j] = get_semantic_similarity(article1, article2)

	# TODO Fred: Fix color scale
	fig = ff.create_annotated_heatmap(z=np.round(confusion_matrix, 3), x=articles, y=articles, colorscale="Viridis")

	fig.update_layout(
		title="Semantic Similarity Confusion Matrix",
		xaxis_title="Articles",
		yaxis_title="Articles",
	)

	# Add color bar
	fig["data"][0]["colorbar"] = dict(
		title="Cosine Similarity", titleside="right", tickvals=[0, 0.25, 0.5, 0.75, 1], ticktext=["0", "0.25", "0.5", "0.75", "1"]
	)
	fig["data"][0]["showscale"] = True

	return fig
