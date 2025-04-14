from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

from loguru import logger
from pydantic_settings import BaseSettings

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

BASE_DIR = Path(__file__).parent.parent
DATE_FORMAT = "%d.%m.%Y"

logger.add(
    BASE_DIR / "logs" / "app.log",
    format="{time} | {level} | {message}",
    level="DEBUG",
    rotation="10 MB",
    retention="1 week",
)

class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, str]:
        async with self.session_factory() as session:
            yield session
            await session.close()

class Settings(BaseSettings):
    BOT_TOKEN: str
    API_ID: int = 0
    API_HASH: str = 'some_string'
    ADMIN_CHAT: int = 0
    MAX_ENTRIES_PER_USER: int = 10
    COMPETITION_START: datetime = datetime.strptime("15.04.2025", DATE_FORMAT)
    COMPETITION_END: datetime = datetime.strptime("20.05.2025", DATE_FORMAT)
    RESULTS_DATE: datetime = datetime.strptime("30.05.2025", DATE_FORMAT)

    DatabaseHelper = DatabaseHelper(url = 'sqlite+aiosqlite:///db.sqlite3')

    class Config:
        extra = "ignore"

settings = Settings()