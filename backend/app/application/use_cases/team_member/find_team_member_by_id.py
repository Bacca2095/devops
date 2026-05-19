from app.domain.entity.team_member_entity import TeamMemberEntity
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.exceptions.not_found import TeamMemberNotFoundException


class FindTeamMemberByIdUseCase:
    def __init__(self, team_member_repository: TeamMemberRepository) -> None:
        self._team_member_repository = team_member_repository

    async def execute(self, team_member_id: int) -> TeamMemberEntity:
        team_member = await self._team_member_repository.find_by_id(team_member_id)
        if not team_member:
            raise TeamMemberNotFoundException(team_member_id)
        return team_member
