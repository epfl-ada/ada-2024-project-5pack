from pathlib import Path

DATA_DIR = Path("./data")

# Related to datasets

PATHS_AND_GRAPH_FOLDER = DATA_DIR / "wikispeedia_paths-and-graph"
WP_SOURCE_DATA_FOLDER = DATA_DIR / "wpcd/wp"
PLAINTEXT_DIR = DATA_DIR / "plaintext_articles"

# Related to configuration for LLMs

HF_KEY = None
LM_PATH = "ibm-granite/granite-3.0-2b-instruct"
LM_CACHE_DIR = DATA_DIR / "models"

# Related to plots

PLOT_COLORS = ["#2ecc71", "#e74c3c", "#3498db", "#f1c40f"]
