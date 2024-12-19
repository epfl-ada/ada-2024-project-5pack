from functools import cache
from urllib.parse import quote

from scipy.sparse import spmatrix
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils.constants import PLAINTEXT_DIR
from src.utils.data import load_graph_data


@cache
def build_tf_idf() -> tuple[spmatrix, dict]:
	"""Builds a TF-IDF matrix from the collection of wikispeedia articles.

	Returns:
	    tf_idf (scipy.sparse.csr.csr_matrix): The TF-IDF matrix.
	    article_to_index (dict): A mapping from article names to their index in the TF-IDF matrix.
	"""
	# Fetch articles
	graph_data = load_graph_data()

	# Build tf_idf vectorizer
	texts = []
	article_to_index = {}
	for i, article in enumerate(graph_data["articles"]["name"]):
		filepath = f"{PLAINTEXT_DIR}/{quote(article)}.txt"
		article_to_index[article] = i
		with open(filepath, encoding="utf-8") as f:
			texts.append(f.read())

	vectorizer = TfidfVectorizer(
		stop_words="english",
		max_features=8000,
	)

	tf_idf = vectorizer.fit_transform(texts)
	return tf_idf, article_to_index


def get_semantic_similarity(title1: str, title2: str) -> float:
	"""Use the TF-IDF matrix to compute the semantic similarity between two articles

	Args:
		title1 (str): The title of the first article.
		title2 (str): The title of the second article.
	Returns:
		float: A similarity score between 0 and 1, where 1 indicates identical titles.
	"""
	tf_idf, article_to_index = build_tf_idf()

	vector1 = tf_idf[article_to_index[title1]]
	vector2 = tf_idf[article_to_index[title2]]
	similarity = cosine_similarity(vector1, vector2)[0][0]
	return similarity


def get_semantic_similarities(path: list[str], target_article: str) -> list[float]:
	"""Return a list containing the semantic similarities between each article in the path and the target article.

	If the path contains '<', the article that was "backtracked" will be ignored
	"""
	# Remove '<' from the path
	clean_path = []  # Path without '<'
	for p in path:
		if p == "<":
			clean_path.pop()
		elif p != target_article:
			clean_path.append(p)

	# Compute the similarity score of each article in the path with the target article
	similarities = []
	for article in clean_path:
		similarity = get_semantic_similarity(article, target_article)
		similarities.append(similarity)

	return similarities


def semantic_increase_score(path: list[str], target_article: str) -> tuple[float, float]:
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
	# Compute the similarity score of each article in the path with the target article
	try:
		similarities = get_semantic_similarities(path, target_article)
	except KeyError:
		print(f"Warning: {target_article} was not found in the list of documents")
		return (-1, 1)

	if len(similarities) <= 1:
		return (-1, 1)  # Ignore paths of small lengths as they are not statistically significant

	# Return the semantic increase score
	correlation, p_value = spearmanr(range(len(similarities)), similarities)
	return correlation, p_value
