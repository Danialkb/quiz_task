from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
env_path = BASE_DIR / ".env"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class Settings(ConfigBase):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    ALLOWED_ORIGINS: list[str] = ["*"]

    # Rabbit
    RABBITMQ_URL: str
    BALANCE_EXCHANGE: str
    BALANCE_QUEUE: str
    BALANCE_EXCHANGE_TYPE: str
    BALANCE_ROUTING_KEY: str

    # Redis
    REDIS_HOST: str
    REDIS_PORT: str
    CACHE_REDIS_TABLE: int
    TASKIQ_REDIS_TABLE: int


settings = Settings()
