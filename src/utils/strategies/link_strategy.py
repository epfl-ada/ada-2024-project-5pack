import numpy as np
from src.utils.data_utils import get_links_from_html_files


def build_link_order():
    """
    Return a link with relative positions of all articles
    
    """
    all_links_dict = get_links_from_html_files()
    for article, links in all_links_dict.items():
        for link in links:
            #Normalize to get relative position
            link['position'] = link['position']/len(links)

    return all_links_dict




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
    Get percentage of clicks on the top links

    Parameters:
    - path_click_positions : A list where we mapped path to their relative positions
    

    Returns:
    A float in [0,1] : percentage of usage of top links (top threshold links)
    """
    top_clicks = sum(1 for pos in path_click_positions if pos <= threshold)
    if not path_click_positions:
        return 0

    return top_clicks/len(path_click_positions)


def get_probability_link_onepath(path, all_links_dict, threshold = 0.3):
    """
    Get percentage of clicks on the top links for one path

    Parameters:
    - path : list of articles
    - all_links_dict : dictionnary from articles to their links and relative positions

    Returns:
    A float in [0,1] : percentage of usage of top links (top threshold links)
    """
    click_positions = get_click_positions(pd.DataFrame({'path': [path]}), all_links_dict)
    return get_probability_link(click_positions, threshold)