from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    searxng_base_url: HttpUrl = HttpUrl("http://localhost:8080")
