from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from decouple import config

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000"
    ]
    PROJECT_NAME: str = "Mayo AI-Lab Workflow"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Mayo AI-Lab workflow for automatic data retrieval, processing, and analysis."

    # Database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    CAMUNDA_REST_URL: str = config("CAMUNDA_REST_URL", cast=str)
    CAMUNDA_WORKFLOW_ID: str = config("CAMUNDA_WORKFLOW_ID", cast=str)

    # Camunda
    CAMUNDA_REST_URL: str = config("CAMUNDA_REST_URL", cast=str)
    CAMUNDA_WORKFLOW_ID: str = config("CAMUNDA_WORKFLOW_ID", cast=str)

    class Config:
        case_sensitive = True

settings = Settings()