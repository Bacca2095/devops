from dataclasses import dataclass

from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.assignment_values import AssignmentWithHours
from app.domain.exceptions.not_found import ProjectNotFoundException


@dataclass
class FindAssignmentsByProjectQuery:
    project_id: int
    page: int = 1
    page_size: int = 10


class FindAssignmentsByProjectUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        assignment_repository: AssignmentRepository,
    ) -> None:
        self._project_repository = project_repository
        self._assignment_repository = assignment_repository

    async def execute(
        self, query: FindAssignmentsByProjectQuery
    ) -> PaginatedResult[AssignmentWithHours]:
        project = await self._project_repository.find_by_id(query.project_id)
        if not project:
            raise ProjectNotFoundException(query.project_id)

        return await self._assignment_repository.find_by_project_with_hours(
            project_id=query.project_id,
            pagination=Pagination(page=query.page, page_size=query.page_size),
        )
