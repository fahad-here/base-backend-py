from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from .base import AsyncSessionLocal

@asynccontextmanager
async def get_async_session():
  """Get SQLAlchemy async session for async context."""
  session: AsyncSession = AsyncSessionLocal()
  try:
    yield session
  finally:
    await session.close()