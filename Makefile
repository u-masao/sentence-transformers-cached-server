
lint:
	poetry run isort app
	poetry run black -l 79 app
	poetry run flake8 app

test:
	curl -X POST http://localhost:8000/v1/embeddings \
    -H 'Content-Type: application/json' \
    -d '{"text":"This is a test string."}' | jq
