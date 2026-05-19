from dataclasses import dataclass

from app.domain.entity.project_entity import ProjectEntity, ProjectStatus
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.exceptions.not_found import ProjectNotFoundException


@dataclass
class UpdateProjectStatusCommand:
    project_id: int
    status: ProjectStatus


class UpdateProjectStatusUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self._project_repository = project_repository

    async def execute(self, command: UpdateProjectStatusCommand) -> ProjectEntity:
        project = await self._project_repository.find_by_id(command.project_id)
        if not project:
            raise ProjectNotFoundException(command.project_id)

        project.change_status(command.status)

        return await self._project_repository.update(project)
