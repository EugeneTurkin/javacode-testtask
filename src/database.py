from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import config


if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from sqlalchemy.ext.asyncio import AsyncSession


async_engine = create_async_engine(config.POSTGRES_CONNECTION_URI, echo=True)

async_session = async_scoped_session(async_sessionmaker(bind=async_engine), scopefunc=asyncio.current_task)


class Base(DeclarativeBase):
    """Base class for all models."""



async def get_session() -> AsyncIterator[AsyncSession]:
    """Get database session. FastAPI dependency for database session."""
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await session.close()
