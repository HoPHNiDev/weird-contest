from src.app.models import User, Works

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pyrogram.types import User as PyrogramUser


async def get_or_create_user(session: AsyncSession, user: PyrogramUser) -> User:
    stmt = select(User).where(User.tg_id == user.id)
    result = await session.execute(stmt)
    required_user = result.scalars().first()

    if not required_user:
        required_user = User(
            tg_id=user.id,
            username=user.username,
        )
        session.add(required_user)
        await session.commit()

    return required_user


async def create_work(session: AsyncSession, user: User, work_link: str) -> Works:
    new_work = Works(
        work_link=work_link,
        user_id=user.id,
    )
    session.add(new_work)
    await session.commit()
    return new_work


async def get_user_works_count(session: AsyncSession, user: User) -> int:
    stmt = select(func.count()).select_from(Works).where(Works.user_id == user.id)
    result = await session.execute(stmt)
    return result.scalar()
