from src.utils.data import load_graph_data

def compute_hub_usage_ratio(path: list[str]) -> float:
    """
    Compute the hub usage ratio for a given path based on the top 200 hubs by PageRank score.

    Args:
        path (list[str]): List of article names in the path.

    Returns:
        float: Ratio of hub articles in the path.
    """
    graph_data = load_graph_data()
    top_hubs = {article for article, score in graph_data['top_200_hubs']}
    
	# Return hub usage ratio
    # This assumes path of length 1 are removed from the dataset
    hub_count = sum(1 for article in path if article in top_hubs)
    return hub_count / len(path) if path else 0.0
