from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entity.project_entity import ProjectEntity
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.project_values import ProjectFilters, ProjectSummary


class ProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: ProjectEntity) -> ProjectEntity:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, project_id: int) -> Optional[ProjectEntity]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        pagination: Pagination,
        filters: ProjectFilters,
    ) -> PaginatedResult[ProjectEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, project: ProjectEntity) -> ProjectEntity:
        raise NotImplementedError

    @abstractmethod
    async def find_summary(self, project_id: int) -> ProjectSummary:
        raise NotImplementedError
