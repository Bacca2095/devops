from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.infrastructure.repositories.time_log_repository import (
    PostgresTimeLogRepository,
)
from app.domain.interfaces.time_log_repository import TimeLogRepository
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.api.dependencies.assignment import get_assignment_repository
from app.application.use_cases.time_log.create_time_log import CreateTimeLogUseCase
from app.application.use_cases.time_log.find_time_logs_by_assignment import (
    FindTimeLogsByAssignmentUseCase,
)


def get_time_log_repository(
    db: AsyncSession = Depends(get_db),
) -> TimeLogRepository:
    return PostgresTimeLogRepository(db)


def get_create_time_log(
    assignment_repo: AssignmentRepository = Depends(get_assignment_repository),
    time_log_repo: TimeLogRepository = Depends(get_time_log_repository),
) -> CreateTimeLogUseCase:
    return CreateTimeLogUseCase(assignment_repo, time_log_repo)


def get_find_time_logs_by_assignment(
    assignment_repo: AssignmentRepository = Depends(get_assignment_repository),
    time_log_repo: TimeLogRepository = Depends(get_time_log_repository),
) -> FindTimeLogsByAssignmentUseCase:
    return FindTimeLogsByAssignmentUseCase(assignment_repo, time_log_repo)
