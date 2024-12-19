import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.utils.metrics import rank_length_analysis

# Define color map
color_map = {'positive': 'blue', 'negative': 'orange'}
# Sample data similar to your plot

def rank_length_plot(graph_data):
    df = rank_length_analysis(graph_data['paths_finished'])[lambda x: x['count'] > 5][lambda x: x['source'] != '<']
    df['sign'] = df['spearman'].apply(lambda x: 'negative' if x < 0 else 'positive')
    # Main scatter plot
    scatter = go.Scatter(
        x=df['spearman'],
        y=df['pvalue'],
        mode='markers',
        marker=dict(
            size=10,
            color=[color_map[s] for s in df['sign']],
            opacity=0.7
        ),
        name='scatter'
    )

	# Marginal histograms
    hist_x = go.Histogram(
		x=df["spearman"],
		marker_color=df["sign"].map(color_map),
		opacity=0.7,
		name="Spearman Distribution",
		nbinsx=20,
		showlegend=False,
	)

    hist_y = go.Histogram(
		y=df["pvalue"],
		marker_color=df["sign"].map(color_map),
		opacity=0.7,
		name="P-Value Distribution",
		nbinsy=20,
		showlegend=False,
	)

	# Combine plots into a figure with subplots
    from plotly.subplots import make_subplots

    fig = make_subplots(
		rows=2,
		cols=2,
		specs=[[{"type": "histogram"}, None], [{"type": "scatter"}, {"type": "histogram"}]],
		column_widths=[0.8, 0.2],
		row_heights=[0.2, 0.8],
		shared_xaxes=True,
		shared_yaxes=True,
		horizontal_spacing=0.02,
		vertical_spacing=0.02,
	)

    # Add scatter plot
    fig.add_trace(scatter, row=2, col=1)

    # Add histograms
    fig.add_trace(hist_x, row=1, col=1)
    fig.add_trace(hist_y, row=2, col=2)

    # Update layout
    fig.update_layout(
    	title="Scatter Plot with Marginal Histograms",
    	xaxis=dict(title="spearman", showgrid=True),
    	yaxis=dict(title="pvalue", showgrid=True),
    	bargap=0.05,
    	showlegend=True,
    )
    return fig
