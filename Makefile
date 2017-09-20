install:
	pip install -r requirements-dev.txt

run:
	python3 run.py

test:
	pytest

clear:
	find . -name "*.pyc" -exec rm -rf {} \;

lint:
	flake8 tests user_api
