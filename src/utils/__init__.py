import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# Custom exception classes
class AnalysisError(Exception):
	"""Base exception class for analysis errors"""

	pass


class DataError(AnalysisError):
	"""Exception for data-related errors"""

	pass


class ValidationError(AnalysisError):
	"""Exception for validation errors"""

	pass
