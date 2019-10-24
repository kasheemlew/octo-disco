.PHONEY: test

run:
	@export PYTHONPATH="${PYTHONPATH}:." && python src/main.py

test:
	@export PYTHONPATH="${PYTHONPATH}:." && python -m unittest discover tests