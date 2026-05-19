from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entity.time_log_entity import TimeLogEntity
from app.domain.interfaces.time_log_repository import TimeLogRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.infrastructure.models import TimeLogModel
from app.infrastructure.mappers.time_log_mapper import TimeLogMapper


class PostgresTimeLogRepository(TimeLogRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, time_log: TimeLogEntity) -> TimeLogEntity:
        orm = TimeLogMapper.to_model(time_log)
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return TimeLogMapper.to_entity(orm)

    async def find_by_assignment(
        self,
        assignment_id: int,
        pagination: Pagination,
    ) -> PaginatedResult[TimeLogEntity]:
        query = (
            select(TimeLogModel)
            .where(TimeLogModel.assignment_id == assignment_id)
            .order_by(TimeLogModel.logged_date.desc())
        )

        total_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()

        offset = (pagination.page - 1) * pagination.page_size
        query = query.offset(offset).limit(pagination.page_size)
        result = await self._session.execute(query)
        items = [TimeLogMapper.to_entity(row) for row in result.scalars().all()]

        return PaginatedResult(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )
