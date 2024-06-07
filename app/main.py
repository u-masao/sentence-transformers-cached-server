from fastapi import FastAPI
from fastapi.responses import JSONResponse
from redis import Redis
from sentence_transformers import SentenceTransformer

from .settings import Settings

app = FastAPI()
settings = Settings()
redis = Redis(host=settings.redis_host, port=settings.redis_port, db=0)
embedding_model = SentenceTransformer(settings.model_name)


@app.post("/v1/embeddings")
async def get_embeddings(input: str, model: str):
    print(model, input)
    cache_key = f"embeddings:{input}"
    cached_result = redis.get(cache_key)

    if cached_result:
        return JSONResponse(
            content={"embedding": eval(cached_result.decode())}
        )

    embedding = embedding_model.encode(input).tolist()
    redis.set(cache_key, str(embedding))

    return JSONResponse(content={"embedding": embedding})
