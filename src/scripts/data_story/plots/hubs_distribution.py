import plotly.graph_objs as go
import networkx as nx
from pathlib import Path

import plotly.graph_objs as go
import plotly.express as px
import networkx as nx
from pathlib import Path

from src.utils.data import load_graph_data
from src.utils.metrics import average_on_paths, pagerank

def create_pagerank_distribution_plot(data: dict) -> go.Figure:
    """Create simple visualization of PageRank distribution."""
    # Calculate and sort PageRank scores
    scores = sorted(nx.pagerank(data["graph"]).items(), key=lambda x: x[1], reverse=True)
    articles, values = zip(*scores)
    
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
    
    # Layout
    fig.update_layout(
        title="PageRank Score Distribution",
        xaxis_title="Article Rank",
        yaxis_title="PageRank Score",
        yaxis_type="log",
        template="plotly_white",
        # Add x-axis annotation for "200"
        xaxis=dict(
            ticktext=["0", "200", "1000", "2000", "3000", "4000"],
            tickvals=[0, 200, 1000, 2000, 3000, 4000],
        ),
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
    """Generate and save the plot."""
    fig = create_pagerank_distribution_plot(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.write_html(output_dir / "pagerank_distribution.html", include_plotlyjs=True, full_html=True)
    graph_data = load_graph_data()
    
    plot_gen = generality_behavior(graph_data)
    plot_gen.write_html(output_dir / "plot_gen.html", include_plotlyjs=True, full_html=True)
