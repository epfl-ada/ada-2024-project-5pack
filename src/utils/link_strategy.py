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
    for _,row in paths.iterrows():
        path = row['path']
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

    return top_clicks/len(path_click_positions)
