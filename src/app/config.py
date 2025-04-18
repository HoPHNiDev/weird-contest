import os.path
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
from pyromod import Client

BASE_DIR = Path(__file__).parent.parent
DATE_FORMAT = "%d.%m.%Y"

logger.add(
    BASE_DIR / "logs" / "src.log",
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
    BOT_TOKEN: str = "7849308296:AAHDpJPMJQ-YiZeNTStY1--4dVwJ5TKlJLQ"
    API_ID: int = 16233010
    API_HASH: str = "4a64ab8c1674910f6e29ba6f3e3f3cb1"
    ADMIN_CHAT: int = -1002622307442
    MAX_ENTRIES_PER_USER: int = 10
    COMPETITION_START: datetime = datetime.strptime("15.04.2025", DATE_FORMAT)
    COMPETITION_END: datetime = datetime.strptime("20.05.2025", DATE_FORMAT)
    RESULTS_DATE: datetime = datetime.strptime("30.05.2025", DATE_FORMAT)

    db_helper: DatabaseHelper = DatabaseHelper(
        url=f"sqlite+aiosqlite:///{BASE_DIR.parent / 'db.sqlite3'}"
    )

    class Config:
        extra = "ignore"


settings = Settings()

if not os.path.exists(f"{BASE_DIR}/app/sessions"):
    os.makedirs(f"{BASE_DIR}/app/sessions")

bot = Client(
    "bot",
    bot_token=settings.BOT_TOKEN,
    api_id=settings.API_ID,
    api_hash=settings.API_HASH,
    workdir=BASE_DIR / "app" / "sessions",
)
