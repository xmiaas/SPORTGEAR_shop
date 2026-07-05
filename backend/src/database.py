from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs, AsyncSession

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from typing import Annotated
from fastapi import Depends
from src.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine,expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


async def get_db():
    async with async_session_maker() as session:
        yield session

DbSession = Annotated[AsyncSession, Depends(get_db)]

