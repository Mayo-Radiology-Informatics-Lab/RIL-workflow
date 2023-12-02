from typing import List
from fastapi import File
from app.models.user_model import User
from app.models.project_model import Project
from app.schemas.project_schema import ProjectCreate, ProjectUpdate
from app.services.content_service import ContentService
from uuid import UUID


class ProjectService:
    @staticmethod
    async def List_projects(user: User) -> List[Project]:
        projects = await Project.find(Project.owner.id == user.id).to_list()
        return projects

    @staticmethod
    async def Create_project(data: ProjectCreate, user: User) -> Project:
        project = Project(**data.dict(), owner=user)
        return await project.insert()

    @staticmethod
    async def Get_project(project_id: UUID, user: User):
        project = await Project.find_one(
            Project.project_id == project_id, Project.owner.id == user.id
        )
        return project

    @staticmethod
    async def Update_project(project_id: UUID, data: ProjectUpdate, user: User):
        project = await ProjectService.Get_project(project_id, user)
        await project.update({"$set": data.dict(exclude_unset=True)})

        await project.save()
        return project

    @staticmethod
    async def Delete_project(project_id: UUID, user: User):
        project = await ProjectService.Get_project(project_id, user)
        if project:
            await project.delete()
        return None