def compute_hub_usage_ratio(hubs: set[str], path: list[str]) -> float:
    """
    Compute the hub usage ratio for a given path based on the top N hubs by PageRank score.

    Args:
        graph (nx.Graph): The graph to compute PageRank scores from.
        path (list[str]): List of article names in the path.

    Returns:
        float: Ratio of hub articles in the path.
    """
	
	# Return hub usage ratio
    hub_count = sum(1 for article in path if article in hubs)
    return hub_count / len(path) if path else 0.0
