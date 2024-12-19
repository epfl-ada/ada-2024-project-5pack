from src.utils.analyzers.rank_length_analyzer import rank_length_plot

from pathlib import Path

def generate_plot(data: dict, output_dir: Path) -> None:
    fig = rank_length_plot(data)
    fig.write_html(output_dir / "spearman_rank_length_graph.html", include_plotlyjs=True, full_html=True)