import os
from contextlib import asynccontextmanager

from app.settings import Settings, get_settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

settings: Settings = get_settings()


engine = create_async_engine(settings.DB_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


def get_engine():
    return create_engine(settings.SYNC_DB_URL, echo=True)
