from app.domain.entity.project_entity import ProjectEntity
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.exceptions.not_found import ProjectNotFoundException


class FindProjectByIdUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self._project_repository = project_repository

    async def execute(self, project_id: int) -> ProjectEntity:
        project = await self._project_repository.find_by_id(project_id)
        if not project:
            raise ProjectNotFoundException(project_id)
        return project
