from dataclasses import dataclass

from app.domain.entity.team_member_entity import (
    TeamMemberEntity,
    MemberRole,
    MemberSeniority,
)
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.exceptions.not_found import TeamMemberNotFoundException
from app.domain.exceptions.conflict import DuplicateEmailException


@dataclass
class UpdateTeamMemberCommand:
    team_member_id: int
    full_name: str
    email: str
    document_number: str
    role: MemberRole
    seniority: MemberSeniority


class UpdateTeamMemberUseCase:
    def __init__(self, team_member_repository: TeamMemberRepository) -> None:
        self._team_member_repository = team_member_repository

    async def execute(self, command: UpdateTeamMemberCommand) -> TeamMemberEntity:
        team_member = await self._team_member_repository.find_by_id(
            command.team_member_id
        )
        if not team_member:
            raise TeamMemberNotFoundException(command.team_member_id)

        existing = await self._team_member_repository.find_by_email(command.email)
        if existing and existing.id != command.team_member_id:
            raise DuplicateEmailException(command.email)

        team_member.update(
            full_name=command.full_name,
            email=command.email,
            document_number=command.document_number,
            role=command.role,
            seniority=command.seniority,
        )

        return await self._team_member_repository.update(team_member)
