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

    BALANCE_SERVICE_URL: str


settings = Settings()
