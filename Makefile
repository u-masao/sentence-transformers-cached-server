
lint:
	poetry run isort app
	poetry run black -l 79 app
	poetry run flake8 app
