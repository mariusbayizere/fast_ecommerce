from sqlmodel import SQLModel
from src.config import Config
from typing import AsyncGenerator
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine


# Create the async engine
engine: AsyncEngine = create_async_engine(
    Config.DATABASE_URL,
    echo=True
)

async def init_db():
    """
    This function initializes the database.
    """
    async with engine.begin() as conn:
        from src.students.models import Student
        # Create the database tables
        await conn.run_sync(SQLModel.metadata.create_all)



async def det_session() -> AsyncGenerator[AsyncSession, None]:
    """
    This function creates a new session for the database.
    """
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session