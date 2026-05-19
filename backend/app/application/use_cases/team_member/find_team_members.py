from dataclasses import dataclass, field

from app.domain.entity.team_member_entity import TeamMemberEntity
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.team_member_values import TeamMemberFilters


@dataclass
class FindTeamMembersQuery:
    page: int = 1
    page_size: int = 10
    filters: TeamMemberFilters = field(default_factory=TeamMemberFilters)


class FindTeamMembersUseCase:
    def __init__(self, team_member_repository: TeamMemberRepository) -> None:
        self._team_member_repository = team_member_repository

    async def execute(
        self, query: FindTeamMembersQuery
    ) -> PaginatedResult[TeamMemberEntity]:
        return await self._team_member_repository.find_all(
            pagination=Pagination(page=query.page, page_size=query.page_size),
            filters=query.filters,
        )
