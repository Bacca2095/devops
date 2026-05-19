from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.infrastructure.repositories.project_repository import PostgresProjectRepository
from app.domain.interfaces.project_repository import ProjectRepository
from app.application.use_cases.project.create_project import CreateProjectUseCase
from app.application.use_cases.project.find_projects import FindProjectsUseCase
from app.application.use_cases.project.find_project_by_id import FindProjectByIdUseCase
from app.application.use_cases.project.update_project import UpdateProjectUseCase
from app.application.use_cases.project.update_project_status import (
    UpdateProjectStatusUseCase,
)
from app.application.use_cases.project.find_project_summary import (
    FindProjectSummaryUseCase,
)


def get_project_repository(
    db: AsyncSession = Depends(get_db),
) -> ProjectRepository:
    return PostgresProjectRepository(db)


def get_create_project(
    repo: ProjectRepository = Depends(get_project_repository),
) -> CreateProjectUseCase:
    return CreateProjectUseCase(repo)


def get_find_projects(
    repo: ProjectRepository = Depends(get_project_repository),
) -> FindProjectsUseCase:
    return FindProjectsUseCase(repo)


def get_find_project_by_id(
    repo: ProjectRepository = Depends(get_project_repository),
) -> FindProjectByIdUseCase:
    return FindProjectByIdUseCase(repo)


def get_update_project(
    repo: ProjectRepository = Depends(get_project_repository),
) -> UpdateProjectUseCase:
    return UpdateProjectUseCase(repo)


def get_update_project_status(
    repo: ProjectRepository = Depends(get_project_repository),
) -> UpdateProjectStatusUseCase:
    return UpdateProjectStatusUseCase(repo)


def get_find_project_summary(
    repo: ProjectRepository = Depends(get_project_repository),
) -> FindProjectSummaryUseCase:
    return FindProjectSummaryUseCase(repo)
