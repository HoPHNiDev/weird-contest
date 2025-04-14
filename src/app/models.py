from datetime import datetime

from sqlalchemy import Column, DateTime, func, ForeignKey
from sqlmodel import Field, SQLModel, Relationship


class Works(SQLModel, table=True):
    __tablename__ = "works"

    id: int = Field(primary_key=True)
    work_link: str = Field(nullable=False)
    created_at: datetime | None = Field(sa_column=Column(DateTime, default=func.now()))
    user_id: int | None = Field(
        sa_column=Column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    )
    user: "User" = Relationship(back_populates="works")

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    tg_id: int
    username: str
    works: list[Works] = Relationship(back_populates="user")
