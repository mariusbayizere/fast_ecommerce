from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlmodel import SQLModel,text
from src.config import Config


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
