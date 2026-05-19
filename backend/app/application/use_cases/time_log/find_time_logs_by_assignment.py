from dataclasses import dataclass

from app.domain.entity.time_log_entity import TimeLogEntity
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.interfaces.time_log_repository import TimeLogRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.exceptions.not_found import AssignmentNotFoundException


@dataclass
class FindTimeLogsByAssignmentQuery:
    assignment_id: int
    page: int = 1
    page_size: int = 10


class FindTimeLogsByAssignmentUseCase:
    def __init__(
        self,
        assignment_repository: AssignmentRepository,
        time_log_repository: TimeLogRepository,
    ) -> None:
        self._assignment_repository = assignment_repository
        self._time_log_repository = time_log_repository

    async def execute(
        self, query: FindTimeLogsByAssignmentQuery
    ) -> PaginatedResult[TimeLogEntity]:
        assignment = await self._assignment_repository.find_by_id(query.assignment_id)
        if not assignment:
            raise AssignmentNotFoundException(query.assignment_id)

        return await self._time_log_repository.find_by_assignment(
            assignment_id=query.assignment_id,
            pagination=Pagination(page=query.page, page_size=query.page_size),
        )
