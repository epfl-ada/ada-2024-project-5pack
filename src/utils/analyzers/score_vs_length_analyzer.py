
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.utils.metrics import scores_vs_length_analysis


def scores_vs_length_histograms(graph_data):
    dfs = scores_vs_length_analysis(graph_data)
    srs = [df[lambda x: (x['pvalue'] < 0.05) & (x['count'] > 10)]['spearman'] for df in dfs.values()]

    fig = make_subplots(rows=1, cols=len(dfs), subplot_titles=[f"{name}, mean={sr.mean():.2f}" for name, sr in zip(dfs.keys(), srs)])

    for i, (name, sr) in enumerate(zip(dfs.keys(), srs), start=1):
        fig.add_trace(
            go.Histogram(
                x=sr,
            ),
            row=1,
            col=i
        )

    fig.update_layout(
        title="Distribution of spearman correlation coefficients for each score",
        template="plotly",
        showlegend=False
    )

    return fig