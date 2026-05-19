from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.entity.project_entity import (
    ProjectEntity,
    ProjectPriority,
    ProjectStatus,
)
from app.domain.interfaces.project_repository import ProjectRepository


@dataclass
class CreateProjectCommand:
    name: str
    priority: ProjectPriority
    start_date: date
    description: Optional[str] = None
    end_date: Optional[date] = None


class CreateProjectUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self._project_repository = project_repository

    async def execute(self, command: CreateProjectCommand) -> ProjectEntity:
        project = ProjectEntity(
            name=command.name,
            priority=command.priority,
            start_date=command.start_date,
            description=command.description,
            end_date=command.end_date,
            status=ProjectStatus.ACTIVE,
        )
        return await self._project_repository.create(project)
