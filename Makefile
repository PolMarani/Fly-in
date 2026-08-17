MAP ?= map.txt


install:
	pip install -r requirements.txt

run:
	python3 run.py $(MAP)

debug:
	python3 -m pdb run.py $(MAP)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

lint:
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	flake8 .