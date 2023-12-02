from fastapi import APIRouter
from app.api.api_v1.handlers import user, project, content, camunda
from app.api.auth.jwt import auth_router

router = APIRouter()

router.include_router(user.user_router, prefix="/users", tags=["users"])
router.include_router(project.project_router, prefix="/projects", tags=["projects"])
router.include_router(content.content_router, prefix="/contents", tags=["project contents"])
router.include_router(camunda.camunda_router, prefix="/camunda", tags=["camunda send task"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])