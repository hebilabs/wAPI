from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    APP_NAME: str = "Weak Application Programming Interface (wAPI)"
    DEBUG: bool = True
    SECRET_KEY: str = "supersecret_ctf_key"
    DATABASE_URL: str = "database.db"
    VULNERABLE_MODE: bool = True


    FLAG: str = os.getenv("FLAG", "CTF{dev_flag}")

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


@lru_cache
def get_settings():
    return Settings()