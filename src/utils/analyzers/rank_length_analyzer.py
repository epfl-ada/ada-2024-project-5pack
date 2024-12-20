import plotly.graph_objects as go
import numpy as np
import pandas as pd
from src.utils.metrics import rank_length_analysis
from plotly.subplots import make_subplots

# Define color map
color_map = {'positive': 'blue', 'negative': 'orange'}
# Sample data similar to your plot

def rank_length_plot_old(graph_data):
	# Load and prepare data
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


def rank_length_plot(graph_data):
	# Load and prepare data
	df = rank_length_analysis(graph_data['paths_finished'])[
		lambda x: (x['count'] > 5) & (x['source'] != '<')
   	]
	return rank_length_plot_from_analysis_data(df)

def rank_length_plot_from_analysis_data(df_from_analysis, pvalue_threshold = 0.05):
	df = df_from_analysis[lambda x: x['pvalue'] < pvalue_threshold]

	# Separate data by sign
	df_positive = df[df['spearman'] >= 0]
	df_negative = df[df['spearman'] < 0]

	xbins=dict(
		start=-1,
		end=1,
		size=0.1
	)
	ybins=dict(
		start=0,
		end=pvalue_threshold,
		size=0.005
	)
	# Create separate heatmaps for positive and negative samples
	heatmap_positive = go.Histogram2d(
		x=df_positive['spearman'],
		y=df_positive['pvalue'],
		colorscale='Blues',
		xbins=dict(
			start=0,
			end=1,
			size=xbins['size']
		),
		ybins=ybins,
		showscale=False,
		name='Positive Samples',
	)

	heatmap_negative = go.Histogram2d(
		x=df_negative['spearman'],
		y=df_negative['pvalue'],
		colorscale='Reds',
		xbins=dict(
			start=-1,
			end=0,
			size=xbins['size']
		),
		ybins=ybins,
		showscale=False,
		name='Negative Samples',
	)

	# Histograms for each sign
	hist_x_positive = go.Histogram(
		x=df_positive['spearman'],
		marker=dict(color='blue'),
		opacity=0.7,
		name='Positive Samples',
		xbins=xbins,
		showlegend=False
	)

	hist_x_negative = go.Histogram(
		x=df_negative['spearman'],
		marker=dict(color='red'),
		opacity=0.7,
		name='Negative Samples',
		xbins=xbins,
		showlegend=False
	)

	hist_y_positive = go.Histogram(
		y=df_positive['pvalue'],
		marker=dict(color='blue'),
		opacity=0.7,
		name='Positive Samples',
		ybins=ybins,
		cumulative=dict(
			currentbin='include',
			direction='increasing',
			enabled=True
		),
		showlegend=False
	)

	hist_y_negative = go.Histogram(
		y=df_negative['pvalue'],
		marker=dict(color='red'),
		opacity=0.7,
		name='Negative Samples',
		ybins=ybins,
		cumulative=dict(
			currentbin='include',
			direction='increasing',
			enabled=True
		),
		showlegend=False
	)

	fig = make_subplots(
		rows=2, cols=2,
		specs=[[{"type": "histogram"}, None],
			[{"type": "heatmap"}, {"type": "histogram"}]],
		column_widths=[0.8, 0.2],
		row_heights=[0.4, 0.6],
		shared_xaxes=True,
		shared_yaxes=True,
		horizontal_spacing=0.07,
		vertical_spacing=0.07
	)

	# Add heatmaps
	fig.add_trace(heatmap_positive, row=2, col=1)
	fig.add_trace(heatmap_negative, row=2, col=1)


	# Add histograms
	fig.add_trace(hist_x_positive, row=1, col=1)
	fig.add_trace(hist_x_negative, row=1, col=1)
	fig.add_trace(hist_y_positive, row=2, col=2)
	fig.add_trace(hist_y_negative, row=2, col=2)

	# Update layout
	fig.update_layout(
		title="Spearman correlation and associated p-values",
		bargap=0.05,
		barmode='stack',
		height=1600,
		width=1200,
		showlegend=True,
	)

	# Set axis titles
	fig.update_xaxes(title_text="Spearman Correlation Coefficient", row=2, col=1, showgrid=True)
	fig.update_yaxes(title_text="p-value", row=2, col=1, showgrid=True)

	fig.update_xaxes(showticklabels=True, title_text="Spearman Correlation Coefficient", row=1, col=1)
	fig.update_yaxes(showticklabels=True, title_text="count", row=1, col=1)
	fig.update_xaxes(showticklabels=True, title_text="count (cumulative)", row=2, col=2)
	fig.update_yaxes(showticklabels=True, title_text="p-value", row=2, col=2)

	fig.show()
