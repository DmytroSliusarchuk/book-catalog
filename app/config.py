from typing import Any

from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class CustomBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


class Config(CustomBaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    DEFAULT_PAGE_SIZE: int = 15

settings = Config()

tags_metadata: list[dict[str, str]] = [
    {"name": "root", "description": "Root endpoint."},
    {"name": "books", "description": "Operations with books."},
    {"name": "reviews", "description": "Operations with reviews."},
]

app_configs: dict[str, Any] = {
    "title": "Book Catalog API",
    "description": "API for books and reviews.",
    "version": "0.0.2",
    "openapi_tags": tags_metadata,
}

