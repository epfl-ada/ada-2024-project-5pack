import logging
from typing import Any

import networkx as nx
import numpy as np
import pandas as pd

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def describe_value(value: Any) -> str:
	# utility function to get a textual and useful description of a variable
	if isinstance(value, pd.DataFrame):
		return f"DataFrame {value.shape}"

	if isinstance(value, np.ndarray):
		return f"Array {value.shape}"

	if isinstance(value, nx.DiGraph):
		return f"DiGraph {len(value.nodes), len(value.edges)}"
	
	if isinstance(value, set):
		return f"Set ({len(value)})"
	
	if isinstance(value, list):
		return f"List ({len(value)})"

	if isinstance(value, dict):
		return f"Dict ({len(value)})"
	
	if isinstance(value, tuple):
		return f"Tuple ({len(value)})"

	raise ValueError(f"Cannot describe type {type(value)}")


def describe_dict(data_dict: dict[str, Any]) -> None:
	# utility function to describe a dictionary by printing a table
	data_infos = {
		"Keyword": list(data_dict.keys()),
		"Type (shape)": [*map(describe_value, data_dict.values())],
	}

	column_lengths = {k: max(map(len, v)) for k, v in data_infos.items()}

	print(" | ".join([k + " " * (v - len(k)) for k, v in column_lengths.items()]))
	print("-" * (sum(column_lengths.values()) + 3 * (len(column_lengths) - 1)))
	for i in range(len(data_dict)):
		print(
			"   ".join(
				[v[i] + " " * (column_lengths[k] - len(v[i])) for k, v in data_infos.items()],
			),
		)
