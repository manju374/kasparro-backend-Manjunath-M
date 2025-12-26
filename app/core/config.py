import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/kasparro"
    )

    COINPAPRIKA_API_KEY: str = os.getenv("COINPAPRIKA_API_KEY", "")
    COINGECKO_API_KEY: str = os.getenv("COINGECKO_API_KEY", "")


settings = Settings()
