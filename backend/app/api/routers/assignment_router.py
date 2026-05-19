from fastapi import APIRouter, Depends, Query

from app.api.dependencies.assignment import (
    get_create_assignment,
    get_find_assignments_by_project,
    get_update_assignment_status,
)
from app.api.dto.assignment_dto import (
    AssignmentCreateDto,
    AssignmentStatusUpdateDto,
    AssignmentDto,
)
from app.api.dto.common_dto import PaginatedDto
from app.application.use_cases.assignment.create_assignment import (
    CreateAssignmentUseCase,
    CreateAssignmentCommand,
)
from app.application.use_cases.assignment.find_assignments_by_project import (
    FindAssignmentsByProjectUseCase,
    FindAssignmentsByProjectQuery,
)
from app.application.use_cases.assignment.update_assignment_status import (
    UpdateAssignmentStatusUseCase,
    UpdateAssignmentStatusCommand,
)

router = APIRouter(tags=["Assignments"])


@router.post(
    "/projects/{project_id}/assignments",
    response_model=AssignmentDto,
    status_code=201,
)
async def create_assignment(
    project_id: int,
    body: AssignmentCreateDto,
    use_case: CreateAssignmentUseCase = Depends(get_create_assignment),
) -> AssignmentDto:
    assignment = await use_case.execute(
        CreateAssignmentCommand(
            project_id=project_id,
            team_member_id=body.team_member_id,
            assignment_role=body.assignment_role,
            start_date=body.start_date,
            end_date=body.end_date,
        )
    )
    return AssignmentDto.from_entity(assignment)


@router.get(
    "/projects/{project_id}/assignments",
    response_model=PaginatedDto[AssignmentDto],
)
async def get_assignments_by_project(
    project_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    use_case: FindAssignmentsByProjectUseCase = Depends(
        get_find_assignments_by_project
    ),
) -> PaginatedDto[AssignmentDto]:
    result = await use_case.execute(
        FindAssignmentsByProjectQuery(
            project_id=project_id,
            page=page,
            page_size=page_size,
        )
    )
    return PaginatedDto.from_result(result, AssignmentDto.from_entity)


@router.patch("/assignments/{assignment_id}/status", response_model=AssignmentDto)
async def update_assignment_status(
    assignment_id: int,
    body: AssignmentStatusUpdateDto,
    use_case: UpdateAssignmentStatusUseCase = Depends(get_update_assignment_status),
) -> AssignmentDto:
    assignment = await use_case.execute(
        UpdateAssignmentStatusCommand(
            assignment_id=assignment_id,
            status=body.status,
        )
    )
    return AssignmentDto.from_entity(assignment)
