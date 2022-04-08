run: test
	pipenv run python main.py

test: unit

unit:
	pipenv run python -m pytest tests/unit
