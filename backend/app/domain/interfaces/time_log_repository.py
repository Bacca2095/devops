from abc import ABC, abstractmethod

from app.domain.entity.time_log_entity import TimeLogEntity
from app.domain.value_objects.pagination import PaginatedResult, Pagination


class TimeLogRepository(ABC):
    @abstractmethod
    async def create(self, time_log: TimeLogEntity) -> TimeLogEntity:
        raise NotImplementedError

    @abstractmethod
    async def find_by_assignment(
        self,
        assignment_id: int,
        pagination: Pagination,
    ) -> PaginatedResult[TimeLogEntity]:
        raise NotImplementedError
