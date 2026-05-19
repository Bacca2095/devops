from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entity.team_member_entity import TeamMemberEntity
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.team_member_values import TeamMemberFilters


class TeamMemberRepository(ABC):
    @abstractmethod
    async def create(self, team_member: TeamMemberEntity) -> TeamMemberEntity:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, team_member_id: int) -> Optional[TeamMemberEntity]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[TeamMemberEntity]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self,
        pagination: Pagination,
        filters: TeamMemberFilters,
    ) -> PaginatedResult[TeamMemberEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, team_member: TeamMemberEntity) -> TeamMemberEntity:
        raise NotImplementedError
