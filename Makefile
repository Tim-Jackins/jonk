run: test
	pipenv run python main.py

test: unit

unit:
	pipenv run python -m pytest tests/unit

lint:
	pipenv run python -m pylint ./main.py ./cogs

format:
	pipenv run python -m black ./main.py ./cogs

up:
	docker build -f Dockerfile -t jonk_bot_image .
	docker run -d --name jonk_bot jonk_bot_image

down:
	docker stop jonk_bot
	docker container rm jonk_bot
