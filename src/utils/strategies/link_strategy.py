import pandas as pd


def get_click_positions(paths: pd.DataFrame, all_links_dict: dict):
	"""Get click positions of the paths.

	Parameters
	----------
	- paths : It is a dataframe with the following columns:
			hashedIpAddress   timestamp   durationInSec   path (list of articles)   rating
	- all_links_dict : dictionnary from articles to their links and relative positions


	Returns
	-------
	A list where we mapped path to their relative positions

	"""
	c = []
	for _, row in paths.iterrows():
		path = row["path"]
		for i in range(len(path) - 1):
			current_article = path[i]
			next_article = path[i + 1]

			if current_article in all_links_dict:
				for link in all_links_dict[current_article]:
					if link.get("title") == next_article:
						if "position" in link:
							c.append(link["position"])
						break
	return c
