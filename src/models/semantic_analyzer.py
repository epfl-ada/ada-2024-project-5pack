"""
Semantic Analysis Module with plaintext article content
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils import logger

PLAINTEXT_DIR = "./data/plaintext_articles"


class SemanticAnalyzer:
	def __init__(self, max_features=5000):
		self.vectorizer = TfidfVectorizer(stop_words="english", max_features=max_features, max_df=0.95, min_df=2)
		self.tfidf_matrix = None
		self.articles = None

	def load_article_content(self, article_name):
		"""Load article content from plaintext file"""
		try:
			filepath = PLAINTEXT_DIR / f"{article_name}.txt"
			with open(filepath, "r", encoding="utf-8") as f:
				return f.read()
		except Exception as e:
			logger.warning(f"Could not read article {article_name}: {e}")
			return ""

	def process_articles(self, articles_df):
		"""Process articles using their full content"""
		logger.info("Processing articles for semantic analysis...")

		# Store article names
		print(articles_df)
		self.articles = articles_df["name"].tolist()

		# Load full content for each article
		article_contents = []
		for article in self.articles:
			content = self.load_article_content(article)
			article_contents.append(content)

		logger.info(f"Loaded content for {len(article_contents)} articles")

		# Compute TF-IDF with limited vocabulary
		self.tfidf_matrix = self.vectorizer.fit_transform(article_contents)

		vocab_size = len(self.vectorizer.vocabulary_)
		logger.info(f"Processed articles with vocabulary size: {vocab_size}")

	def get_path_similarity(self, path):
		"""Compute average semantic similarity along path"""
		try:
			if isinstance(path, list):
				articles = path
			else:
				articles = path.split(";")

			if len(articles) < 2:
				return 1.0

			scores = []
			for i in range(len(articles) - 1):
				try:
					idx1 = self.articles.index(articles[i])
					idx2 = self.articles.index(articles[i + 1])

					sim = cosine_similarity(self.tfidf_matrix[idx1 : idx1 + 1], self.tfidf_matrix[idx2 : idx2 + 1])[0][0]
					scores.append(sim)
				except ValueError:
					continue

			return np.mean(scores) if scores else 0.0
		except:
			return 0.0
