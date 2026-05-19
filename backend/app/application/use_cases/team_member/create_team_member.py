from dataclasses import dataclass

from app.domain.entity.team_member_entity import (
    TeamMemberEntity,
    MemberRole,
    MemberSeniority,
)
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.exceptions.conflict import DuplicateEmailException


@dataclass
class CreateTeamMemberCommand:
    full_name: str
    email: str
    document_number: str
    role: MemberRole
    seniority: MemberSeniority


class CreateTeamMemberUseCase:
    def __init__(self, team_member_repository: TeamMemberRepository) -> None:
        self._team_member_repository = team_member_repository

    async def execute(self, command: CreateTeamMemberCommand) -> TeamMemberEntity:
        existing = await self._team_member_repository.find_by_email(command.email)
        if existing:
            raise DuplicateEmailException(command.email)

        team_member = TeamMemberEntity(
            full_name=command.full_name,
            email=command.email,
            document_number=command.document_number,
            role=command.role,
            seniority=command.seniority,
        )
        return await self._team_member_repository.create(team_member)
