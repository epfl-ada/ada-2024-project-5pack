from pathlib import Path
import plotly.graph_objects as go


def generate_plot(data: dict, output_dir: Path) -> None:
	communities = ["Europe 🇪🇺", "Biology 🌱", "Americas 🌎", "Africa and Asia 🌍", "United Kingdom 🇬🇧", "Fundamental sciences ⚛️"]
	articles = [885, 820, 757, 713, 645, 622]

	fig = go.Figure(
		go.Bar(
			x=articles,
			y=communities,
			orientation="h",
			text=communities,
			textposition="inside",
			insidetextanchor="middle",
			textfont={"size": 14},
			textangle=0,
			marker_color="#48a23a",
		)
	)

	fig.update_layout(
		title="Top Communities by Number of Articles",
		title_x=0.5,
		xaxis_title="Number of Articles",
		yaxis={"categoryorder": "total ascending", "showticklabels": False},
		height=500,
		margin={"l": 50},
		showlegend=False,
		yaxis_title=None,
	)

	fig.write_html(output_dir / "communities_graph.html", include_plotlyjs=True, full_html=True)
