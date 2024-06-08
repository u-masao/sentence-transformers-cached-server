
lint:
	poetry run isort app
	poetry run black -l 79 app
	poetry run flake8 app

test:
	curl -X POST http://localhost:8000/embeddings \
    -H 'Content-Type: application/json' \
    -d '{"input":"この文字列は日本語で書かれたテスト文字列です","model":"awesome_embedding_model"}' | jq
