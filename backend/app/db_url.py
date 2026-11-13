"""Database URL helpers. Kept free of third-party imports so they are easy to test."""


def normalize_database_url(url: str) -> str:
    """Return a SQLAlchemy URL that uses the psycopg 3 driver for PostgreSQL.

    Hosted providers (Supabase, Neon, Render) hand out URLs that start with
    ``postgres://`` or ``postgresql://``. SQLAlchemy needs the driver named
    explicitly, so both are rewritten to ``postgresql+psycopg://``. URLs that
    already name a driver, and non-PostgreSQL URLs such as SQLite, pass through
    unchanged.
    """
    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        url = "postgresql+psycopg://" + url[len("postgresql://"):]
    return url


def is_sqlite(url: str) -> bool:
    return url.startswith("sqlite")


def is_in_memory_sqlite(url: str) -> bool:
    return url in ("sqlite://", "sqlite:///:memory:")
