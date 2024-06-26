import json
from typing import List, Tuple

from fastapi import Body, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from redis import Redis
from torch import Tensor
from transformers import AutoModel, AutoTokenizer

from .settings import Settings

app = FastAPI()
settings = Settings()
redis = Redis(host=settings.redis_host, port=settings.redis_port, db=0)
redis.flushall()
tokenizer = AutoTokenizer.from_pretrained(settings.hf_model_name)
embedding_model = AutoModel.from_pretrained(settings.hf_model_name)


class InputData(BaseModel):
    input: str
    model: str

    def __init__(self, **data):
        super().__init__(**data)
        print(f"Received data: {self.dict()}")


class Embedding(BaseModel):
    object: str = "embedding"
    index: int
    embedding: List[float]  # Explicitly declare List[float]


class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int


class ResponseData(BaseModel):
    object: str = "list"
    data: List[Embedding]
    model: str
    usage: Usage


class ResponseDataEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.dict()  # Use .dict() for BaseModel serialization
        elif isinstance(obj, float):  # Handle the floats in List[float]
            return str(obj)  # or round(obj, 4) for rounding to 4 decimals
        return super().default(obj)


def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(
        ~attention_mask[..., None].bool(), 0.0
    )
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def embed(text: str) -> Tuple[List[float], int]:
    global tokenizer, embedding_model, settings

    batch_dict = tokenizer(
        [str(text)],
        max_length=settings.hf_max_length,
        padding=True,
        truncation=True,
        return_tensors="pt",
    )

    tokens = len(batch_dict["input_ids"][0])
    outputs = embedding_model(**batch_dict)
    embeddings = average_pool(
        outputs.last_hidden_state, batch_dict["attention_mask"]
    )

    return embeddings[0].tolist(), tokens


def build_response(
    embedding: List[float],
    model_name: str,
    prompt_tokens: int,
    total_tokens: int,
):
    response_data = ResponseData(
        data=[Embedding(index=0, embedding=embedding)],
        model=model_name,
        usage=Usage(prompt_tokens=prompt_tokens, total_tokens=total_tokens),
    )

    # Explicit JSON serialization with custom encoder
    json_string = json.dumps(response_data, cls=ResponseDataEncoder)
    return JSONResponse(content=json.loads(json_string))


@app.post("/embeddings")
async def post_embeddings(input_data: InputData = Body(...)):
    cache_key = f"embeddings:{settings.hf_model_name}:{input_data.input}"
    cached_result = redis.get(cache_key)

    # cache hit
    if cached_result:
        decoded = json.loads(cached_result.decode())
        return build_response(
            decoded["embedding"],
            settings.hf_model_name,
            decoded["tokens"],
            decoded["tokens"],
        )

    # cache miss
    embedding, tokens = embed(input_data.input)
    redis.set(
        cache_key, json.dumps({"embedding": embedding, "tokens": tokens})
    )
    return build_response(embedding, settings.hf_model_name, tokens, tokens)
