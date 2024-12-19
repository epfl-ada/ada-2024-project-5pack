from pathlib import Path

from src.utils.analyzers.human_behavior_analyzer import game_stats_simple_join, game_stats_survival_plot


def generate_plot(data: dict, output_dir: Path) -> None:
	stats = game_stats_simple_join(data)
	figure = game_stats_survival_plot(stats)
	figure.write_html(output_dir / "game_stats_intro.html", include_plotlyjs=True, full_html=True)
