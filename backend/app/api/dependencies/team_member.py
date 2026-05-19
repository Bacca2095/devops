from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.infrastructure.repositories.team_member_repository import (
    PostgresTeamMemberRepository,
)
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.application.use_cases.team_member.create_team_member import (
    CreateTeamMemberUseCase,
)
from app.application.use_cases.team_member.find_team_members import (
    FindTeamMembersUseCase,
)
from app.application.use_cases.team_member.find_team_member_by_id import (
    FindTeamMemberByIdUseCase,
)
from app.application.use_cases.team_member.update_team_member import (
    UpdateTeamMemberUseCase,
)
from app.application.use_cases.team_member.update_team_member_status import (
    UpdateTeamMemberStatusUseCase,
)


def get_team_member_repository(
    db: AsyncSession = Depends(get_db),
) -> TeamMemberRepository:
    return PostgresTeamMemberRepository(db)


def get_create_team_member(
    repo: TeamMemberRepository = Depends(get_team_member_repository),
) -> CreateTeamMemberUseCase:
    return CreateTeamMemberUseCase(repo)


def get_find_team_members(
    repo: TeamMemberRepository = Depends(get_team_member_repository),
) -> FindTeamMembersUseCase:
    return FindTeamMembersUseCase(repo)


def get_find_team_member_by_id(
    repo: TeamMemberRepository = Depends(get_team_member_repository),
) -> FindTeamMemberByIdUseCase:
    return FindTeamMemberByIdUseCase(repo)


def get_update_team_member(
    repo: TeamMemberRepository = Depends(get_team_member_repository),
) -> UpdateTeamMemberUseCase:
    return UpdateTeamMemberUseCase(repo)


def get_update_team_member_status(
    repo: TeamMemberRepository = Depends(get_team_member_repository),
) -> UpdateTeamMemberStatusUseCase:
    return UpdateTeamMemberStatusUseCase(repo)
