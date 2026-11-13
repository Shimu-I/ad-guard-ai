"""Database engine, session factory and declarative base."""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config import get_settings
from app.db_url import is_in_memory_sqlite, is_sqlite, normalize_database_url


class Base(DeclarativeBase):
    pass


def make_engine(url: str) -> Engine:
    url = normalize_database_url(url)
    if is_sqlite(url):
        kwargs: dict = {"connect_args": {"check_same_thread": False}}
        if is_in_memory_sqlite(url):
            # One shared connection, otherwise each new connection sees an empty database.
            kwargs["poolclass"] = StaticPool
        return create_engine(url, **kwargs)
    # pool_pre_ping recovers from connections that free-tier hosts close while idle.
    return create_engine(url, pool_pre_ping=True)


engine = make_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
