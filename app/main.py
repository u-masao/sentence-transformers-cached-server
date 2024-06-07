from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
from redis import Redis
import os

app = FastAPI()
redis = Redis(host=os.getenv('REDIS_HOST', 'redis'), port=6379, db=0)
model = SentenceTransformer('intfloat/multilingual-e5-large')

@app.get("/embeddings")
async def get_embeddings(input: str):
    cache_key = f"embeddings:{input}"
    cached_result = redis.get(cache_key)

    if cached_result:
        return JSONResponse(content={"embedding": eval(cached_result.decode())})

    embedding = model.encode(input).tolist()
    redis.set(cache_key, str(embedding))

    return JSONResponse(content={"embedding": embedding})
