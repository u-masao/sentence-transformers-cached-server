from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_name: str = "intfloat/multilingual-e5-small"
    redis_host: str = "redis"
    redis_port: int = 6379

    class Config:
        env_prefix = "API_"
