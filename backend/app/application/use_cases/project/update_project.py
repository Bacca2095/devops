from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.entity.project_entity import ProjectEntity, ProjectPriority
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.exceptions.not_found import ProjectNotFoundException


@dataclass
class UpdateProjectCommand:
    project_id: int
    name: str
    priority: ProjectPriority
    start_date: date
    description: Optional[str] = None
    end_date: Optional[date] = None


class UpdateProjectUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self._project_repository = project_repository

    async def execute(self, command: UpdateProjectCommand) -> ProjectEntity:
        project = await self._project_repository.find_by_id(command.project_id)
        if not project:
            raise ProjectNotFoundException(command.project_id)

        project.update(
            name=command.name,
            priority=command.priority,
            start_date=command.start_date,
            description=command.description,
            end_date=command.end_date,
        )

        return await self._project_repository.update(project)
