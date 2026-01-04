from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.config import settings
import os

def create_engine():
    database_url = settings.DATABASE_URL
    
    if database_url.startswith("sqlite"):

        db_path = database_url.replace("sqlite+aiosqlite:///", "")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        return create_async_engine(
            database_url,
            echo=settings.DEBUG,
            connect_args={"check_same_thread": False},
            poolclass=NullPool
        )
    else:
        return create_async_engine(
            database_url,
            echo=settings.DEBUG,
            pool_size=20,
            max_overflow=0,
            pool_pre_ping=True
        )

engine = create_engine()

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        from app.models import Base
        await conn.run_sync(Base.metadata.create_all)
        print(f"База данных инициализирована: {settings.DATABASE_URL}")