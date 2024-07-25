# SentenceTransformersCachedServer

This project is an API server that provides embeddings using SentenceTransformers.

## Introduction

This repository provides a FastAPI-based API server that generates text embeddings using SentenceTransformers. With Redis caching and Docker containerization, it enables high-speed and scalable operation.


## Features

- Receives text input and calculates embeddings using the SentenceTransformers' encode() method.
- Calculated embeddings are cached in Redis for fast retrieval when the same text is input again.
- Can be run as a Docker container for easy environment setup.
- Embeddings can be obtained from the /embeddings endpoint.

## Usage

Environment Setup

```bash
docker-compose up -d --build
```

Getting Embeddings

"model" is dummy.

```bash
curl -X POST http://localhost:8000/embeddings \
   -H 'Content-Type: application/json' \
   -d '{"input":"query: This string is a test string written in English","model":"awesome_embedding_model"}'
```

Specify the text you want to get embeddings for in the text parameter.

The response is in JSON format, with the embedding vector included in the embedding field.

```
{
 "embedding": [
   0.0025373732205480337,
   -0.008475706912577152,
   -0.005010251421481371,
   -0.0677233338356018,
   0.04533613100647926,
   -0.046973951160907745,
   0.026564622297883034,
   0.10488858073949814,
      ....
   0.0399100000000332
 ]
}
```

## Clearing the Redis Cache

The cache is cleared when the API starts. If you want to clear the cache, restart the API with the following command or similar:

```bash
docker compose restart
```

## Customization

- SentenceTransformers Model

  - You can change the model to use by modifying API_HF_MODEL_NAME in docker-compose.yaml.

- Redis Settings

  - You can specify the Redis hostname with the API_REDIS_HOST environment variable in docker-compose.yml.

- Endpoint URL

  - You can change the endpoint URL by modifying the @app.post("/embeddings") decorator in app/main.py.

- Listen Port

  - You can change the listening port by modifying the port number 8000 in docker-compose.yaml.

## License

This project is licensed under the MIT License.

## Notes

This API server was created for demonstration purposes and requires additional security measures for use in a production environment.

Be aware of Redis memory consumption when processing large amounts of text at once.

This embedding server does not process strings beyond 512 tokens. Text splitting is not supported.

## Author

u-masao
