import numpy as np
def get_click_positions(paths, all_links_dict):
    """
    Get click positions of the paths

    Parameters:
    - paths : It is a dataframe with the format:   hashedIpAddress   timestamp   durationInSec   path (list of articles)   rating
    - all_links_dict : dictionnary from articles to their links and relative positions
    

    Returns:
    A list where we mapped path to their relative positions
    """
    c = []
    # for _,row in paths.iterrows():
    #     path = row['path']

    for path in paths.path:    
        for i in range(len(path) - 1):
            before = path[i]
            next = path[i + 1]
            if before in all_links_dict:
                
                for link in all_links_dict[before]:
                    if link.get('title') == next:
                        if 'position' in link:
                            c.append(link['position'])
                        break
    
    return c


def get_probability_link(path_click_positions, threshold = 0.3):
    """
    Get probability that this path clicks on the top links

    Parameters:
    - path_click_positions : A list where we mapped path to their relative positions
    

    Returns:
    A probability (float) in [0,1]
    """
    top_clicks = sum(1 for pos in path_click_positions if pos <= threshold)
    if not path_click_positions:
        return 0

    return top_clicks/len(path_click_positions)


def compute_average_positions(paths, all_links_dict, max_rank=10):
    """
    Computes the average relative position of clicked links for each click rank up to max_rank.

    Parameters:
    - paths: It is a dataframe with the format:   hashedIpAddress   timestamp   durationInSec   path (list of articles)   rating
    - all_links_dict: dictionnary from articles to their links and relative positions
    - max_rank: The maximum rank to consider (default is 10).

    Returns:
    - A dictionary with ranks as keys and average positions for values.
    """
    # Initialize a dictionary for positions for each rank
    rank_positions = {rank: [] for rank in range(1, max_rank + 1)}
    

    
    for path in paths.path:

        for i in range(1, min(len(path), max_rank+1)):
            before = path[i - 1]
            nextt = path[i]
            # Find the position of the clicked link
            if before in all_links_dict:
                for link in all_links_dict[before]:
                    if link.get('title') == nextt:
                        if 'position' in link:
                            rank_positions[i].append(link['position'])
                        break


    average_positions = {}
    for rank, positions in rank_positions.items():
        if positions:
            average_positions[rank] = np.mean(positions)
        # else:
            # average_positions[rank] = np.nan  #When too long
    
    return average_positions