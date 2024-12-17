from collections.abc import Generator

import numpy as np
import pandas as pd
from tqdm import tqdm

from src.utils.data import load_graph_data
from src.utils.llm import get_tokenizer_and_model, next_token_probs

BATCH_SIZE = 16
RESULT_FILE_PATH = "./data/generated/pairs_categories.csv"


def get_category_prompt(article_1: str, article_2: str) -> str:
	"""Returning few-shot LLM prompt for categorizing relationship between two articles.

	Args:
	        article_1 (str): first article to consider
	        article_2 (str): second article to consider

	Returns:
	        str: a prompt designed for language models following the Granite-3.0 Instruct chat template.

	"""
	return f"""<|start_of_role|>user<|end_of_role|>
You are acting as a classifier. I will give you two words corresponding to two concepts.
I need you to help me decide of relations between the first and second concept.

There are four categories:

1. Geographical relationship.
The concepts are related in this sense: the second concept is geographically included in the first.
Typically: (United States, California) have this relationship, (United States, Bordeaux) does not have this relationship, (Home, me) does not have this relationship.

2. Temporal relationship.
Similarly, the second concept is temporaly linked to the first one.
(21th Century, Internet bubble crisis) is an example, (Prehistory, Michael Jackson) is not.

3. Categorical relationship.
This relationship is about the category. The first concept should be a categorical feature of the first.
One example is (Animal, Dog), whereas (Computer, Ant) is not.

4. Other
This is how you classify all other pairs of concepts.

I give you precisely two concepts, and you should give me the corresponding number (1, 2, 3 or 4). Answer with the number and only the number.

For example:
- I give you (Moon, Beattles), your answer: 4.
- I give you (Spain, Science), your answer: 4.
- I give you (January, New Year), your answer: 2.
- I give you (Africa, Kenya), your answer: 1.
- I give you (Europe, France), your answer: 1.

Now it is your turn to give an answer.

First concept: {article_1}.
Second concept: {article_2}.

Your answer:<|end_of_text|>
<|start_of_role|>assistant<|end_of_role|>"""


def categories_generator() -> Generator[tuple[list[tuple[str, str]], list[tuple]], None, None]:
	"""Generator of LLM probs for next token using the get category prompt.

	Yields:
			Tuple[List[Tuple[str, str]], List[Tuple]]: _description_

	"""
	for i in range(len(unique_pairs) // BATCH_SIZE):
		batch = [unique_pairs[i * BATCH_SIZE + j] for j in range(BATCH_SIZE)]

		prompts = [get_category_prompt(*t) for t in batch]
		probs = next_token_probs(prompts)

		results = []
		for i in range(BATCH_SIZE):
			dist = np.array(
				[probs[i, ...][numbers[str(answer)]] for answer in [1, 2, 3, 4]],
			)
			total_llm_probs = dist.sum()

			dist /= total_llm_probs

			total_llm_probs = str(total_llm_probs)
			dist = [str(e) for e in dist]

			results.append((*dist, total_llm_probs))

		yield batch, results


def retrieve_unique_pairs() -> list[tuple[str, str]]:
	"""Retrieve and returns all the unique pairs of consecutive articles (corresponding to links) in realised paths.

	Returns:
	        list[tuple[str, str]]: a list of unique pairs of consecutive articles present in user paths.

	"""
	# retrieve all distinct links used by the players
	graph_data = load_graph_data()

	paths_finished = graph_data["paths_finished"]
	paths_unfinished = graph_data["paths_unfinished"]

	paths = np.concatenate([paths_finished.path.values, paths_unfinished.path.values])

	df = pd.DataFrame(data=paths, columns=["path"]).reset_index(names="path_id")
	df = df.explode("path")

	pairs = pd.concat(
		[
			df.shift().rename(columns={"path_id": "ref_index", "path": "article_1"}),
			df.rename(columns={"path_id": "matched_index", "path": "article_2"}),
		],
		axis=1,
	)

	pairs = pairs[pairs.ref_index == pairs.matched_index]

	unique_pairs = pairs[["article_1", "article_2"]].apply(tuple, axis=1).unique()
	return unique_pairs


if __name__ == "__main__":
	tokenizer = get_tokenizer_and_model()[0]
	numbers = {str(number): tokenizer(str(number), return_tensors="pt")["input_ids"].flatten()[0] for number in range(10)}

	unique_pairs = retrieve_unique_pairs()

	with open(RESULT_FILE_PATH, "w") as file:
		file.write(
			"Article 1,Article 2,Geographical,Temporal,Categorical,Other,Total\n",
		)

		for batch, results in tqdm(
			categories_generator(),
			total=(len(unique_pairs) // BATCH_SIZE),
		):
			for i, (article_1, article_2) in enumerate(batch):
				file.write(f"{article_1},{article_2}," + ",".join(results[i]))
				file.write("\n")

			file.flush()
