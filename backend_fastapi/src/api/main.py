from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func

from src.core.config import settings
from src.api.routes import tasks
from src.core.database import engine, Base, AsyncSessionLocal
from src.models.task import Task

app = FastAPI(
    title="Simple To-Do List API",
    description="Backend for the Simple To-Do List application.",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Tasks",
            "description": "Operations with tasks.",
        }
    ]
)

@app.on_event("startup")
async def on_startup():
    # This creates the tables in the database on startup.
    # For production, it's recommended to use a migration tool like Alembic.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Seed the database if it's empty
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count(Task.id)))
        if result.scalar_one() == 0:
            db.add_all([
                Task(title="Create a stunning UI", description="Use React and follow the style guide."),
                Task(title="Implement the backend API", description="Use FastAPI and connect to PostgreSQL.", completed=True),
                Task(title="Deploy the application", description="Ensure everything works in the cloud.")
            ])
            await db.commit()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CLIENT_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

@app.get("/")
def health_check():
    return {"message": "Healthy"}
