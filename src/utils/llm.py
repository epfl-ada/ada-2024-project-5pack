import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List

MODEL_PATH = "ibm-granite/granite-3.0-2b-instruct"
MODEL_CACHE_DIR = "./data/models"

HF_KEY = None

_model, _tokenizer = None, None


def get_tokenizer_and_model():
	# simple utility function to avoid reloading tokenizer and model to memory
	global _model, _tokenizer

	if _model is None:
		_model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, cache_dir=MODEL_CACHE_DIR, token=HF_KEY)

	if _tokenizer is None:
		_tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, cache_dir=MODEL_CACHE_DIR, token=HF_KEY)
		_tokenizer.pad_token = _tokenizer.eos_token

	return _tokenizer, _model


def next_token_probs(prompts: List[str]) -> torch.Tensor:
	"""Get distribution over next token for a batch of prompts.

	Args:
		prompts (List[str]): untokenized batch of prompts.

	Returns:
		torch.Tensor: distributions over the next token for all the prompts.
	"""
	tokenizer, model = get_tokenizer_and_model()

	inputs = tokenizer(prompts, return_tensors="pt", padding=True)

	with torch.no_grad():
		outputs = model(**inputs)

	logits = outputs.logits[:, -1, :]
	probs = torch.nn.functional.softmax(logits, dim=1)

	return probs
