from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from app.domain.entity.time_log_entity import TimeLogEntity
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.interfaces.time_log_repository import TimeLogRepository
from app.domain.exceptions.not_found import AssignmentNotFoundException
from app.domain.exceptions.business_rules import InactiveAssignmentException


@dataclass
class CreateTimeLogCommand:
    assignment_id: int
    logged_date: date
    hours: Decimal
    description: Optional[str] = None


class CreateTimeLogUseCase:
    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        time_log_repository: TimeLogRepository,
    ) -> None:
        self._assignment_repository = assignment_repository
        self._time_log_repository = time_log_repository

    async def execute(self, command: CreateTimeLogCommand) -> TimeLogEntity:
        assignment = await self._assignment_repository.find_by_id(command.assignment_id)
        if not assignment:
            raise AssignmentNotFoundException(command.assignment_id)

        if not assignment.accepts_time_logs():
            raise InactiveAssignmentException(command.assignment_id)

        time_log = TimeLogEntity(
            assignment_id=command.assignment_id,
            logged_date=command.logged_date,
            hours=command.hours,
            description=command.description,
        )
        return await self._time_log_repository.create(time_log)
