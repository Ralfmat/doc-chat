from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields an active database session to the endpoint and automatically
    cleans up/closes the connection when the request finishes.
    """
    async with AsyncSessionLocal() as session:
        yield session