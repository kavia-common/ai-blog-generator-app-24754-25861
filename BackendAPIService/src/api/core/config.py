from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Use .env file in development. This class centralizes configuration for the
    FastAPI backend including database, auth, CORS, AI provider, and server port.
    """

    # App
    APP_NAME: str = "AI Blog Generator Backend"
    APP_DESCRIPTION: str = "Backend API for AI-powered blog generation with authentication and content management."
    APP_VERSION: str = "0.1.0"

    # Server
    BACKEND_PORT: int = Field(8000, description="Port to run the backend server on")

    # Database
    DATABASE_URL: str = Field(..., description="SQLAlchemy connection string for PostgreSQL")

    # CORS
    CORS_ORIGINS: List[str] = Field(default_factory=lambda: ["*"], description="Allowed CORS origins")

    # Auth
    JWT_SECRET: str = Field(..., description="Secret key used for JWT token signing")
    JWT_ALGORITHM: str = Field("HS256", description="JWT signing algorithm")
    JWT_EXPIRES_MINUTES: int = Field(60 * 24, description="JWT expiration time in minutes")

    # AI
    AI_PROVIDER: str = Field("openai-compatible", description="AI provider type (openai-compatible supported)")
    AI_API_KEY: Optional[str] = Field(None, description="API key for the AI provider")
    AI_MODEL: str = Field("gpt-4o-mini", description="Model name to use for generation")

    # Exports
    PDF_ENGINE: str = Field("placeholder", description="PDF engine choice (placeholder for now)")

    class Config:
        env_file = ".env"
        case_sensitive = True


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings instance."""
    return Settings()  # type: ignore


def get_cors_origins(settings: Settings) -> List[str]:
    """Helper to coerce CORS_ORIGINS env which may be CSV string."""
    origins = settings.CORS_ORIGINS
    if len(origins) == 1 and isinstance(origins[0], str) and "," in origins[0]:
        return [o.strip() for o in origins[0].split(",") if o.strip()]
    return origins
