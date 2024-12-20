from pathlib import Path
import plotly.graph_objects as go

def generate_plot(data, output_dir):
    from src.utils.analyzers.score_vs_length_analyzer import scores_vs_length_histograms
    fig = scores_vs_length_histograms(data)
    fig.write_html(output_dir / "score_vs_length.html", include_plotlyjs=True, full_html=True)