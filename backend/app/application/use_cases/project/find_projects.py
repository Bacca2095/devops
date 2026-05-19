from dataclasses import dataclass, field

from app.domain.entity.project_entity import ProjectEntity
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.project_values import ProjectFilters


@dataclass
class FindProjectsQuery:
    page: int = 1
    page_size: int = 10
    filters: ProjectFilters = field(default_factory=ProjectFilters)


class FindProjectsUseCase:
    def __init__(self, project_repository: ProjectRepository) -> None:
        self._project_repository = project_repository

    async def execute(self, query: FindProjectsQuery) -> PaginatedResult[ProjectEntity]:
        return await self._project_repository.find_all(
            pagination=Pagination(page=query.page, page_size=query.page_size),
            filters=query.filters,
        )
