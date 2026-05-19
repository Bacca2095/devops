from fastapi import APIRouter, Depends, Query

from app.api.dependencies.time_log import (
    get_create_time_log,
    get_find_time_logs_by_assignment,
)
from app.api.dto.time_log_dto import TimeLogCreateDto, TimeLogDto
from app.api.dto.common_dto import PaginatedDto
from app.application.use_cases.time_log.create_time_log import (
    CreateTimeLogUseCase,
    CreateTimeLogCommand,
)
from app.application.use_cases.time_log.find_time_logs_by_assignment import (
    FindTimeLogsByAssignmentUseCase,
    FindTimeLogsByAssignmentQuery,
)

router = APIRouter(tags=["Time Logs"])


@router.post(
    "/assignments/{assignment_id}/timelogs",
    response_model=TimeLogDto,
    status_code=201,
)
async def create_time_log(
    assignment_id: int,
    body: TimeLogCreateDto,
    use_case: CreateTimeLogUseCase = Depends(get_create_time_log),
) -> TimeLogDto:
    time_log = await use_case.execute(
        CreateTimeLogCommand(
            assignment_id=assignment_id,
            logged_date=body.logged_date,
            hours=body.hours,
            description=body.description,
        )
    )
    return TimeLogDto.from_entity(time_log)


@router.get(
    "/assignments/{assignment_id}/timelogs",
    response_model=PaginatedDto[TimeLogDto],
)
async def get_time_logs_by_assignment(
    assignment_id: int,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    use_case: FindTimeLogsByAssignmentUseCase = Depends(
        get_find_time_logs_by_assignment
    ),
) -> PaginatedDto[TimeLogDto]:
    result = await use_case.execute(
        FindTimeLogsByAssignmentQuery(
            assignment_id=assignment_id,
            page=page,
            page_size=page_size,
        )
    )
    return PaginatedDto.from_result(result, TimeLogDto.from_entity)
