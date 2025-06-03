import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

class Settings(BaseSettings):
    BOT_TOKEN: str
    BASE_SITE: str
    ADMIN_IDS: List[int]

    FORMAT_LOG: str = "{level.icon} {time:DD-MM-YYYY at HH:mm:ss}: {level} -> {message}"
    LOG_ROTATION: str = "10 MB"

    # Postgres
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    # SQLite
    SQLITE_URL: str = 'sqlite+aiosqlite:///db.sqlite3'


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )

    def get_webhook_url(self) -> str:
        """Возвращает URL вебхука с кодированием специальных символов."""
        return f"{self.BASE_SITE}/webhook"

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @classmethod
    def load(cls) -> "settings":
        return cls()


settings = Settings.load()

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log", "log.txt")
logger.add(sink=log_file_path, backtrace=False, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)