from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis import Redis
from sentence_transformers import SentenceTransformer

from .settings import Settings

app = FastAPI()
settings = Settings()
redis = Redis(host=settings.redis_host, port=settings.redis_port, db=0)
embedding_model = SentenceTransformer(settings.hf_model_name)


class InputText(BaseModel):
    text: str


@app.post("/v1/embeddings")
async def embeddings(input_text: InputText = Body(...)):
    cache_key = f"embeddings:{settings.hf_model_name}:{input_text.text}"
    cached_result = redis.get(cache_key)

    # cache hit
    if cached_result:
        return JSONResponse(
            content={"embedding": eval(cached_result.decode())}
        )

    # cache miss
    embedding = embedding_model.encode(input_text.text).tolist()
    redis.set(cache_key, str(embedding))
    return JSONResponse(content={"embedding": embedding})
