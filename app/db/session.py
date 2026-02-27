from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

# create_async_engine is the core connection pool to PostgreSQL via asyncpg
engine = create_async_engine(
    settings.async_database_url,
    echo=False,          # set to True for debugging SQL queries
    pool_pre_ping=True,  # checks if connection is alive before using it
)

# async_sessionmaker creates new database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    # expire_on_commit=False is strictly required in async SQLAlchemy.
    # it makes sure object stay in cache memory after commit
    # there's no need to re-query the database to get the object after commit
    expire_on_commit=False, 
)