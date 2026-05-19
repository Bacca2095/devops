from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.api.dependencies.team_member import (
    get_create_team_member,
    get_find_team_members,
    get_find_team_member_by_id,
    get_update_team_member,
    get_update_team_member_status,
)
from app.api.dto.team_member_dto import (
    TeamMemberCreateDto,
    TeamMemberUpdateDto,
    TeamMemberStatusUpdateDto,
    TeamMemberDto,
)
from app.api.dto.common_dto import PaginatedDto
from app.application.use_cases.team_member.create_team_member import (
    CreateTeamMemberUseCase,
    CreateTeamMemberCommand,
)
from app.application.use_cases.team_member.find_team_members import (
    FindTeamMembersUseCase,
    FindTeamMembersQuery,
)
from app.application.use_cases.team_member.find_team_member_by_id import (
    FindTeamMemberByIdUseCase,
)
from app.application.use_cases.team_member.update_team_member import (
    UpdateTeamMemberUseCase,
    UpdateTeamMemberCommand,
)
from app.application.use_cases.team_member.update_team_member_status import (
    UpdateTeamMemberStatusUseCase,
    UpdateTeamMemberStatusCommand,
)
from app.domain.entity.team_member_entity import (
    MemberRole,
    MemberSeniority,
    MemberStatus,
)
from app.domain.value_objects.team_member_values import TeamMemberFilters

router = APIRouter(prefix="/team-members", tags=["Team Members"])


@router.post("/", response_model=TeamMemberDto, status_code=201)
async def create_team_member(
    body: TeamMemberCreateDto,
    use_case: CreateTeamMemberUseCase = Depends(get_create_team_member),
) -> TeamMemberDto:
    team_member = await use_case.execute(
        CreateTeamMemberCommand(
            full_name=body.full_name,
            email=body.email,
            document_number=body.document_number,
            role=body.role,
            seniority=body.seniority,
        )
    )
    return TeamMemberDto.from_entity(team_member)


@router.get("/", response_model=PaginatedDto[TeamMemberDto])
async def get_team_members(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: Optional[MemberStatus] = Query(default=None),
    role: Optional[MemberRole] = Query(default=None),
    seniority: Optional[MemberSeniority] = Query(default=None),
    use_case: FindTeamMembersUseCase = Depends(get_find_team_members),
) -> PaginatedDto[TeamMemberDto]:
    result = await use_case.execute(
        FindTeamMembersQuery(
            page=page,
            page_size=page_size,
            filters=TeamMemberFilters(status=status, role=role, seniority=seniority),
        )
    )
    return PaginatedDto.from_result(result, TeamMemberDto.from_entity)


@router.get("/{team_member_id}", response_model=TeamMemberDto)
async def get_team_member(
    team_member_id: int,
    use_case: FindTeamMemberByIdUseCase = Depends(get_find_team_member_by_id),
) -> TeamMemberDto:
    team_member = await use_case.execute(team_member_id)
    return TeamMemberDto.from_entity(team_member)


@router.put("/{team_member_id}", response_model=TeamMemberDto)
async def update_team_member(
    team_member_id: int,
    body: TeamMemberUpdateDto,
    use_case: UpdateTeamMemberUseCase = Depends(get_update_team_member),
) -> TeamMemberDto:
    team_member = await use_case.execute(
        UpdateTeamMemberCommand(
            team_member_id=team_member_id,
            full_name=body.full_name,
            email=body.email,
            document_number=body.document_number,
            role=body.role,
            seniority=body.seniority,
        )
    )
    return TeamMemberDto.from_entity(team_member)


@router.patch("/{team_member_id}/status", response_model=TeamMemberDto)
async def update_team_member_status(
    team_member_id: int,
    body: TeamMemberStatusUpdateDto,
    use_case: UpdateTeamMemberStatusUseCase = Depends(get_update_team_member_status),
) -> TeamMemberDto:
    team_member = await use_case.execute(
        UpdateTeamMemberStatusCommand(
            team_member_id=team_member_id,
            status=body.status,
        )
    )
    return TeamMemberDto.from_entity(team_member)
