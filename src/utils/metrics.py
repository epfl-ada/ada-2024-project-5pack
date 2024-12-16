from functools import cache
from urllib.parse import quote

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils.constants import ARTICLES_DIR
from src.utils.data_utils import load_graph_data


@cache
def build_tf_idf():
	"""Builds a TF-IDF matrix from the collection of wikispeedia articles.

	Returns:
	    tf_idf (scipy.sparse.csr.csr_matrix): The TF-IDF matrix.
	    article_to_index (dict): A mapping from article names to their index in the TF-IDF matrix.

	"""  # noqa: D401
	# Fetch articles
	graph_data = load_graph_data()

	# Build tf_idf vectorizer
	texts = []
	article_to_index = {}
	for i, article in enumerate(graph_data["articles"]["name"]):
		filepath = f"{ARTICLES_DIR}/{quote(article)}.txt"
		article_to_index[article] = i
		with open(filepath, encoding="utf-8") as f:
			texts.append(f.read())

	vectorizer = TfidfVectorizer(
		stop_words="english",
		max_features=8000,
	)

	tf_idf = vectorizer.fit_transform(texts)
	return tf_idf, article_to_index


def pagerank(graph):
	# Pagerank algorithm using the graph of articles (without weights)
	pagerank_scores = nx.pagerank(graph, alpha=0.85)
	graph_pagerank = pd.DataFrame(
		list(pagerank_scores.items()),
		columns=["Article", "Pagerank"],
	)
	# Normalizing
	graph_pagerank["Generality_score"] = (graph_pagerank["Pagerank"] - graph_pagerank["Pagerank"].min()) / (
		graph_pagerank["Pagerank"].max() - graph_pagerank["Pagerank"].min()
	)
	return graph_pagerank


def average_path(NUMBER_OF_BINS, paths):
	scores_bins = [[] for _ in range(NUMBER_OF_BINS + 1)]

	# We have bins for every steps then add the scores that fall in that bin
	# For ex. if the path is of length 5 we will add step 1 to 1st bin, step 2 to 3rd, etc...
	for _, path in paths.iterrows():
		# This is the previously computed path of generality scores (for each step)
		generality_scores = path["Generality_score"]
		bins = np.linspace(0, 1, len(generality_scores))

		for fraction, score in zip(bins, generality_scores):
			bin_index = int(fraction * NUMBER_OF_BINS)  # Find bin where this falls
			scores_bins[bin_index].append(score)

	scores = [np.mean(scores) for scores in scores_bins]

	percent = [(100 * i / NUMBER_OF_BINS) for i in range(NUMBER_OF_BINS + 1)]

	return scores, percent
