
from fastapi import FastAPI
from .students.routes import student_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from src.auth.routes import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This is a context manager for the lifespan of the FastAPI application.
    It can be used to perform setup and teardown actions.
    """
    print(f"server is starting on port 8000...")
    await init_db()
    yield
    # Perform any cleanup actions here if needed
    print(f"server is stopping...")


version = "v1"

app = FastAPI(
    title="Student API",
    description="This is a simple Student API",
    version=version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)


app.include_router(student_router, prefix=f'/api/{version}/students', tags=['students'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])