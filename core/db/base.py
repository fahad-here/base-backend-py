from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from django.conf import settings

# Create async engine using Django's database settings
DB_CONFIG = settings.DATABASES['default']
DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG['USER']}:{DB_CONFIG['PASSWORD']}@{DB_CONFIG['HOST']}:{DB_CONFIG['PORT']}/{DB_CONFIG['NAME']}"

engine = create_async_engine(
  DATABASE_URL,
  echo=settings.DEBUG,
)

# Create declarative base for models
Base = declarative_base()

# Create async session factory
AsyncSessionLocal = sessionmaker(
  engine,
  class_=AsyncSession,
  expire_on_commit=False,
)