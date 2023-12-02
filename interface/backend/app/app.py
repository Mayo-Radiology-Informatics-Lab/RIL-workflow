import uvicorn
from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.middleware.cors import CORSMiddleware

from app.models.user_model import User
from app.models.project_model import Project
from app.models.content_model import Content
from app.api.api_v1.router import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def app_init():
    """
        Initialize the database connection and create the database if it doesn't exist.
    """
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).workflow

    await init_beanie(
        database=db_client,
        document_models=[
            User, 
            Project,
            Content
        ],
    )

app.include_router(router, prefix=settings.API_V1_STR)

def start():
    """Launched with 'poetry run start' when you are in the backend folder """
    uvicorn.run("app.app:app", host="localhost", port=9000, reload=True, log_level="info")