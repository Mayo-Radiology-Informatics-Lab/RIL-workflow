from fastapi import APIRouter, Depends, File, UploadFile, Form
from app.models.user_model import User
from app.api.deps.user_deps import get_current_user
from app.schemas.project_schema import ProjectOut, ProjectCreate, ProjectUpdate
from app.services.project_service import ProjectService
from uuid import UUID
from typing import List

project_router = APIRouter()

@project_router.get("/", summary="Get all projects of a user", response_model= List[ProjectOut])
async def List(current_user: User = Depends(get_current_user)):
    return await ProjectService.List_projects(current_user)

@project_router.post("/create", summary="Create a Project", response_model=ProjectOut)
async def Create_project(data: ProjectCreate, current_user: User = Depends(get_current_user)):
    return await ProjectService.Create_project(data,  current_user)

@project_router.get("/{project_id}", summary="Get a project by project_id", response_model=ProjectOut)
async def Get_project(project_id: UUID, current_user: User = Depends(get_current_user)):
    return await ProjectService.Get_project(project_id, current_user)

@project_router.put("/{project_id}", summary="Update a project by project_id", response_model=ProjectOut)
async def Update_project(project_id: UUID, data: ProjectUpdate, current_user: User = Depends(get_current_user)):
    return await ProjectService.Update_project(project_id, data, current_user)

@project_router.delete("/{project_id}", summary="Delete a project by project_id", response_model=None)
async def Delete_project(project_id: UUID, current_user: User = Depends(get_current_user)):
    await ProjectService.Delete_project(project_id, current_user)
    return None