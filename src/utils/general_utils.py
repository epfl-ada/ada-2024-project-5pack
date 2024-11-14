import networkx as nx
import numpy as np
import pandas as pd


def describe_value(value):
	if isinstance(value, pd.DataFrame):
		return f"DataFrame {value.shape}"

	if isinstance(value, np.ndarray):
		return f"Array {value.shape}"

	if isinstance(value, nx.DiGraph):
		return f"DiGraph {len(value.nodes), len(value.edges)}"

	raise ValueError(f"Cannot describe type {type(value)}")


def describe_dict(data_dict):
	data_infos = {"Keyword": list(data_dict.keys()), "Type (shape)": [*map(describe_value, data_dict.values())]}

	column_lengths = {k: max(map(len, v)) for k, v in data_infos.items()}

	print(" | ".join([k + " " * (v - len(k)) for k, v in column_lengths.items()]))
	print("-" * (sum(column_lengths.values()) + 3 * (len(column_lengths) - 1)))
	for i in range(len(data_dict)):
		print("   ".join([v[i] + " " * (column_lengths[k] - len(v[i])) for k, v in data_infos.items()]))
