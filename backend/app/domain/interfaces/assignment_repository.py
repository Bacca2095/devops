from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entity.assignment_entity import AssignmentEntity
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.assignment_values import AssignmentWithHours


class AssignmentRepository(ABC):
    @abstractmethod
    async def create(self, assignment: AssignmentEntity) -> AssignmentEntity:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, assignment_id: int) -> Optional[AssignmentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_project(
        self,
        project_id: int,
        pagination: Pagination,
    ) -> PaginatedResult[AssignmentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_project_and_member(
        self,
        project_id: int,
        team_member_id: int,
    ) -> Optional[AssignmentEntity]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_project_with_hours(
        self,
        project_id: int,
        pagination: Pagination,
    ) -> PaginatedResult[AssignmentWithHours]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, assignment: AssignmentEntity) -> AssignmentEntity:
        raise NotImplementedError
