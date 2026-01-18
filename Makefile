.PHONY: test test-solver test-systems test-plotting test-lean-bridge test-all coverage clean quality format

# Individual test modules
test-solver:
	pytest tests/unit/test_solver.py -v -rs

test-systems:
	pytest tests/unit/test_systems.py -v

test-plotting:
	pytest tests/unit/test_plotting_*.py -v

test-lean-bridge:
	pytest tests/unit/test_lean_bridge_symbolic.py -v

# Run all unit tests
test-all:
	pytest tests/unit/ -v

# Coverage report (80%+ target)
coverage:
	pytest tests/unit/ -v --cov=src/logic --cov-report=term-missing --cov-report=html

# Quality checks (black, ruff, mypy)
quality:
	black src/ tests/ --check
	ruff check src/ tests/
	# mypy -p src.logic  # Deferred: See ARCHITECTURE.md Future Enhancements (mypy strict mode)
	
# Format code with black
format:
	black src/ tests/

# Clean generated files
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Default target
test: test-all

