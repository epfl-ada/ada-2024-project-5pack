import plotly.graph_objs as go
import networkx as nx
from pathlib import Path
import numpy as np
from src.utils.strategies.hub_focused_strategy import compute_hub_usage_ratio
from src.utils.metrics import average_on_paths, pagerank
import plotly.express as px
import networkx as nx

def create_hub_usage_ratio_plot(data: dict) -> go.Figure:
    """
    Create visualization of hub usage ratios in paths for finished and unfinished paths.
    """
    
    def compute_ratios(paths):
        return [
            compute_hub_usage_ratio(path)
            for path in paths["path"]
        ]

    finished_ratios = compute_ratios(data["paths_finished"])
    unfinished_ratios = compute_ratios(data["paths_unfinished"])

    mean_finished = np.mean(finished_ratios)
    mean_unfinished = np.mean(unfinished_ratios)

    fig = go.Figure()

    for label, ratios, color in [
        ("Finished", finished_ratios, "#2ecc71"),
        ("Unfinished", unfinished_ratios, "#e74c3c")
    ]:
        fig.add_trace(go.Histogram(
            x=ratios,
            name=f"{label} Paths",
            marker_color=color,
            opacity=0.75,
            xbins=dict(start=0, end=1, size=0.05),  # Bins from 0 to 1 in steps of 0.05
            offsetgroup=label  # Group bars for side-by-side comparison
        ))

    # Add dashed lines for means as Scatter traces (for legend inclusion)
    fig.add_trace(go.Scatter(
        x=[mean_finished, mean_finished],
        y=[0, 8000],
        mode="lines",
        line=dict(color="#2ecc71", dash="dash"),
        name="Mean HUR (Finished)"
    ))
    fig.add_trace(go.Scatter(
        x=[mean_unfinished, mean_unfinished],
        y=[0, 8000],
        mode="lines",
        line=dict(color="#e74c3c", dash="dash"),
        name="Mean HUR (Unfinished)"
    ))

    fig.add_annotation(
        x=mean_finished,
        y=8500,  # Position slightly above the maximum y value
        text=f"{mean_finished:.3f}",
        showarrow=False,
        font=dict(color="#2ecc71"),
        align="center"
    )
    fig.add_annotation(
        x=mean_unfinished,
        y=8500,  # Position slightly above the maximum y value
        text=f"{mean_unfinished:.3f}",
        showarrow=False,
        font=dict(color="#e74c3c"),
        align="center"
    )

    fig.update_layout(
        title="Hub Usage Ratio Distribution<br><sup>Comparing finished vs unfinished paths</sup>",
        xaxis_title="Hub Usage Ratio (Top 200 Hubs in Path / Path Length)",
        yaxis_title="Number of Paths",
        template="plotly_white",
        barmode="group",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.0,
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        )
    )

    return fig

def create_pagerank_distribution_plot(data: dict) -> go.Figure:
    """
    Create a simple visualization of PageRank distribution.
    """
    # Calculate and sort PageRank scores
    scores = sorted(nx.pagerank(data["graph"]).items(), key=lambda x: x[1], reverse=True)
    _, values = zip(*scores)

    # Calculate statistics
    top_200_percentage = sum(values[:200]) / sum(values) * 100
    total_articles_percentage = (200 / len(values)) * 100

    fig = go.Figure()

    # Add main distribution curve
    fig.add_trace(go.Scatter(
        x=list(range(len(values))),
        y=values,
        name='PageRank Distribution',
        line=dict(color='#2ecc71')
    ))

    # Add cutoff line
    fig.add_trace(go.Scatter(
        x=[200, 200],
        y=[min(values), max(values)],
        mode='lines',
        line=dict(color='red', dash='dash', width=2),
        showlegend=False
    ))

    # Top 5 hubs text
    top_5_text = "<br>".join(
        f"{i+1}. {art} ({score:.4f})"
        for i, (art, score) in enumerate(scores[:5])
    )

    fig.update_layout(
        title="PageRank Score Distribution",
        xaxis_title="Article Rank",
        yaxis_title="PageRank Score",
        yaxis_type="log",
        template="plotly_white",
        annotations=[
            dict(
                x=1,
                y=0.8,
                xref="paper",
                yref="paper",
                text=f"Top 5 Hubs with Pagerank score:<br>{top_5_text}",
                showarrow=False,
                align="left",
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            ),
            dict(
                x=200,
                y=max(values),
                text=f"Top 200 articles<br>({total_articles_percentage:.1f}% of all articles)<br>"
                     f"capture {top_200_percentage:.1f}% of<br>total PageRank",
                showarrow=False,
                yshift=10
            )
        ],
        margin=dict(r=200)
    )

    return fig

def generality_behavior(graph_data):
	scores, percent = average_on_paths(10, graph_data["paths_finished"], pagerank(graph_data["graph"]))

	plot = px.line(
		x=percent,
		y=scores,
		labels={"x": "Percentage of path", "y": "Generality Score (higher is more general)"},
		title="Average generality behavior (taken accross all finished paths)",
	)

	return plot


def generate_plot(data: dict, output_dir: Path) -> None:
    """
    Generate and save the plots.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    plot_gen = generality_behavior(data)
    plot_gen.write_html(output_dir / "plot_gen.html", include_plotlyjs=True, full_html=True)

    pagerank_fig = create_pagerank_distribution_plot(data)
    pagerank_fig.write_html(output_dir / "pagerank_distribution.html", include_plotlyjs=True, full_html=True)

    hub_usage_fig = create_hub_usage_ratio_plot(data)
    hub_usage_fig.write_html(output_dir / "hub_usage_ratios.html", include_plotlyjs=True, full_html=True)
