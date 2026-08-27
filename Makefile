PYTHON = python3
MAP = maps/easy/01_linear_path.txt

.PHONY: install run debug clean lint lint-strict

install:
	$(PYTHON) -m pip install flake8 mypy

run:
	$(PYTHON) fly_in.py $(MAP)

debug:
	$(PYTHON) -m pdb fly_in.py $(MAP)

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find . -type d -name .mypy_cache -prune -exec rm -rf {} +

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict
