from app.db_url import is_in_memory_sqlite, is_sqlite, normalize_database_url


def test_postgresql_url_gets_psycopg_driver():
    assert (
        normalize_database_url("postgresql://u:p@host:5432/db")
        == "postgresql+psycopg://u:p@host:5432/db"
    )


def test_legacy_postgres_scheme_is_rewritten():
    assert (
        normalize_database_url("postgres://u:p@host/db")
        == "postgresql+psycopg://u:p@host/db"
    )


def test_explicit_driver_is_left_alone():
    url = "postgresql+psycopg://u:p@host/db"
    assert normalize_database_url(url) == url


def test_sqlite_url_is_left_alone():
    assert normalize_database_url("sqlite:///./adguard.db") == "sqlite:///./adguard.db"


def test_surrounding_whitespace_is_stripped():
    assert normalize_database_url("  postgresql://u:p@h/db\n") == "postgresql+psycopg://u:p@h/db"


def test_sqlite_detection():
    assert is_sqlite("sqlite:///./x.db")
    assert not is_sqlite("postgresql://u:p@h/db")
    assert is_in_memory_sqlite("sqlite://")
    assert not is_in_memory_sqlite("sqlite:///./x.db")
