"""
Central application configuration.
Loaded once from environment variables (.env) via pydantic-settings.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "SkillPath AI"
    ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "skillpath_ai"

    JWT_SECRET_KEY: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    GEMINI_API_KEY: str = ""
    AI_PROVIDER: str = "gemini"

    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    USE_LOCAL_STORAGE: bool = True
    LOCAL_UPLOAD_DIR: str = "uploads"

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
