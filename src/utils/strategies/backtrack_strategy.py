def compute_backtrack_ratio(path: list[str]) -> float:
    """
    Compute the ratio of backtrack steps in a path.
    
    Args:
        path (list[str]): List of articles in the path, including '<' for backtrack steps
        
    Returns:
        float: Ratio of backtrack steps to total path length (between 0 and 1)
    """
    # Count backtrack steps
    backtrack_count = sum(1 for step in path if step == "<")
    
    # Return ratio
    return backtrack_count / len(path)