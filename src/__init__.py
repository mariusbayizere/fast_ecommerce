
from fastapi import FastAPI
from .students.routes import student_router


version = "v1"

app = FastAPI(
    title="Student API",
    description="This is a simple Student API",
    version=version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


app.include_router(student_router, prefix=f'/api/{version}/students', tags=['students'])