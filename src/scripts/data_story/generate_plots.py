"""Main script to generate all plots for the data story."""

import logging
from pathlib import Path

from src.utils.data import load_graph_data

from .plots import communities as communities_plot
from .plots import rank_vs_length as rank_plot
from .plots import game_stats_intro as intro_plot
from .plots import semantic_strategy as semantic_plot
from .plots import regression_analysis as regression_plot
from .plots import link_strat
from .plots import hubs_distribution as hubs_plot
from .plots import backtrack_distribution as backtrack_plot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_all_plots() -> None:
	"""Generate all plots for the data story."""
	# Ensure output directory exists
	output_dir = Path("data_story/assets/plots")
	output_dir.mkdir(parents=True, exist_ok=True)

	data = load_graph_data()

	logger.info("Generating plots...")

	plot_modules = [
		communities_plot,
		rank_plot,
		intro_plot,
		semantic_plot,
		regression_plot,
		hubs_plot,
		backtrack_plot,
		link_strat,
	]

	for plot_module in plot_modules:
		try:
			logger.info(f"Generating {plot_module.__name__}...")
			plot_module.generate_plot(data, output_dir)
		except Exception as e:
			logger.error(f"Error generating {plot_module.__name__}: {str(e)}")
			raise  # Re-raise to stop execution on error

	logger.info("Plot generation complete!")


if __name__ == "__main__":
	generate_all_plots()
