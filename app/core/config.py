from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "Weak Application Programming Interface (wAPI)"
    DEBUG: bool = True

    SECRET_KEY: str = "supersecret_ctf_key"

    DATABASE_URL: str = "database.db"

    VULNERABLE_MODE: bool = True

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()