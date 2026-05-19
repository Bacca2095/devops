from dataclasses import dataclass

from app.domain.entity.team_member_entity import TeamMemberEntity, MemberStatus
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.exceptions.not_found import TeamMemberNotFoundException


@dataclass
class UpdateTeamMemberStatusCommand:
    team_member_id: int
    status: MemberStatus


class UpdateTeamMemberStatusUseCase:
    def __init__(self, team_member_repository: TeamMemberRepository) -> None:
        self._team_member_repository = team_member_repository

    async def execute(self, command: UpdateTeamMemberStatusCommand) -> TeamMemberEntity:
        team_member = await self._team_member_repository.find_by_id(
            command.team_member_id
        )
        if not team_member:
            raise TeamMemberNotFoundException(command.team_member_id)

        if command.status == MemberStatus.ACTIVE:
            team_member.activate()
        else:
            team_member.deactivate()

        return await self._team_member_repository.update(team_member)
