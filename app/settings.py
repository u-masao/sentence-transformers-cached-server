from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    hf_model_name: str = "intfloat/multilingual-e5-small"
    hf_max_length: int = 512
    redis_host: str = "redis"
    redis_port: int = 6379

    class Config:
        env_prefix = "API_"
