"""Centeralized logging configuration for the Forge.

Usage: 
	from logic.logger import get_logger
	logger = get_logger(__name__)
	logger.info("Solver converged in 150 steps")
"""

import logging

def get_logger(name: str) -> logging.Logger:
	"""Get a configured logger for the given module name.
	
	Args:
		name: Module name (use __name__ from calling module)
	
	Returns: 
		Configured logger with console handler
	"""

	logger = logging.getLogger(name)

	#Avoid adding multiple handlers if called repeatedly
	if not logger.handlers: 
		handler = logging.StreamHandler()
		formatter = logging.Formatter(
			"%(asctime)s | %(name)s | %(levelname)s | %(messages)s",
			datefmt="%Y-%m-%d %H:%M:%S",
		)
		handler. setFormatter(formatter)
		logger.addHandler(handler)
		logger.setLevel(logging.INFO)
	
	return logger
