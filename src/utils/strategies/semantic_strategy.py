from scipy.stats import spearmanr
from sklearn.metrics.pairwise import cosine_similarity

from src.utils.metrics import build_tf_idf


def semantic_increase_score(
	path: list[str],
	target_article: str,
) -> tuple[float, float]:
	"""Compute the Semantic Increase Score (SIS) for a given path of articles relative to a target article.

	The SIS quantifies how well the similarity to the target article increases as players progress
	along the path. It is a value between -1 and 1, where 1 indicates a perfect monotonic increase in
	similarity.

	Calculation steps:
		1. Compute the semantic similarity between each article in the path and the target article.
		2. Use Spearman's rank correlation to measure how well the sequence of similarities aligns
		with a strictly increasing trend.

	Args:
		path (list[str]): A list of article names representing the player's navigation path.
		target_article (str): The name of the target article.

	Returns:
		float: The SIS score
		float: p-value indicating the significance of the correlation.

	"""
	tf_idf, article_to_index = build_tf_idf()

	# Remove '<' from the path
	clean_path = []  # Path without '<'
	for p in path:
		if p == "<":
			clean_path.pop()
		elif p != target_article:
			clean_path.append(p)

	if len(clean_path) <= 1:
		return (
			-1,
			1,
		)  # Ignore paths of small lengths as they are not statistically significant

	# Compute the similarity score of each article in the path with the target article
	similarities = []
	for article in clean_path:
		if article not in article_to_index or target_article not in article_to_index:
			print(
				f"Warning: skipping a score as {article} or {target_article} is not in articles list",
			)
			return -1, 1

		vector1 = tf_idf[article_to_index[article]]
		vector2 = tf_idf[article_to_index[target_article]]
		similarity = cosine_similarity(vector1, vector2)[0][0]
		similarities.append(similarity)

	# Return the semantic increase score
	correlation, p_value = spearmanr(range(len(similarities)), similarities)
	return correlation, p_value
