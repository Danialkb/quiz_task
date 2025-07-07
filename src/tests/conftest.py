import os
import psycopg2
import pytest
from alembic import command
from alembic.config import Config
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.models import OptionTranslation, Option, QuestionTranslation, Question, QuizTitleTranslation, Quiz, \
    MatchingOptionCorrectPair, QuizSession
from main import app
from db.session import get_session
from resources.config import settings

TEST_DB_NAME = "test_db"
ADMIN_DB_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/postgres"
)
SYNC_TEST_DB_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{TEST_DB_NAME}"
)
ASYNC_TEST_DB_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/{TEST_DB_NAME}"
)


def create_test_database():
    conn = psycopg2.connect(ADMIN_DB_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM pg_database WHERE datname = %s",
        (TEST_DB_NAME,)
    )
    if not cur.fetchone():
        cur.execute(f"CREATE DATABASE {TEST_DB_NAME}")
    cur.close()
    conn.close()


def drop_test_database():
    conn = psycopg2.connect(ADMIN_DB_URL)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        """
        SELECT pg_terminate_backend(pid)
        FROM pg_stat_activity
        WHERE datname = %s AND pid <> pg_backend_pid();
        """,
        (TEST_DB_NAME,)
    )
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
    cur.close()
    conn.close()


def run_migrations():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    alembic_ini = os.path.join(
        base, "resources", "migrations", "alembic.ini"
    )
    cfg = Config(alembic_ini)
    cfg.set_main_option("sqlalchemy.url", SYNC_TEST_DB_URL)
    cfg.set_main_option(
        "script_location",
        os.path.join(base, "resources", "migrations", "alembic")
    )
    command.upgrade(cfg, "head")


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_test_database()
    run_migrations()
    yield
    drop_test_database()


@pytest.fixture(autouse=True)
async def clean_tables(db_session: AsyncSession):
    tables = [
        OptionTranslation,
        Option,
        QuestionTranslation,
        Question,
        QuizTitleTranslation,
        MatchingOptionCorrectPair,
        QuizSession,
        Quiz,
    ]
    for table in tables:
        await db_session.execute(delete(table))
    await db_session.commit()
    yield
    for table in tables:
        await db_session.execute(delete(table))
    await db_session.commit()


@pytest.fixture
async def async_client():
    async_engine = create_async_engine(ASYNC_TEST_DB_URL, echo=False)
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autoflush=False
    )

    async def override_get_session() -> AsyncSession:
        async with async_session_factory() as session:
            try:
                yield session
            finally:
                await session.rollback()

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://testserver",
            follow_redirects=True
    ) as client:
        yield client

    del app.dependency_overrides[get_session]
    await async_engine.dispose()


@pytest.fixture
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(ASYNC_TEST_DB_URL, echo=False)
    async_session_factory = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        autoflush=False
    )

    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
        await async_engine.dispose()
