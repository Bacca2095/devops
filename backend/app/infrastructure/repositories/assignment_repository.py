from typing import Optional
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entity.assignment_entity import AssignmentEntity, AssignmentStatus
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.assignment_values import AssignmentWithHours
from app.infrastructure.models import AssignmentModel, TimeLogModel
from app.infrastructure.mappers.assignment_mapper import AssignmentMapper


class PostgresAssignmentRepository(AssignmentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, assignment: AssignmentEntity) -> AssignmentEntity:
        orm = AssignmentMapper.to_model(assignment)
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return AssignmentMapper.to_entity(orm)

    async def find_by_id(self, assignment_id: int) -> Optional[AssignmentEntity]:
        result = await self._session.get(AssignmentModel, assignment_id)
        return AssignmentMapper.to_entity(result) if result else None

    async def find_by_project(
        self,
        project_id: int,
        pagination: Pagination,
    ) -> PaginatedResult[AssignmentEntity]:
        query = select(AssignmentModel).where(AssignmentModel.project_id == project_id)

        total_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()

        offset = (pagination.page - 1) * pagination.page_size
        query = query.offset(offset).limit(pagination.page_size)
        result = await self._session.execute(query)
        items = [AssignmentMapper.to_entity(row) for row in result.scalars().all()]

        return PaginatedResult(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )

    async def find_by_project_with_hours(
        self,
        project_id: int,
        pagination: Pagination,
    ) -> PaginatedResult[AssignmentWithHours]:
        total_result = await self._session.execute(
            select(func.count(AssignmentModel.id)).where(
                AssignmentModel.project_id == project_id
            )
        )
        total = total_result.scalar_one()

        offset = (pagination.page - 1) * pagination.page_size
        query = (
            select(
                AssignmentModel,
                func.coalesce(func.sum(TimeLogModel.hours), 0).label("total_hours"),
            )
            .outerjoin(TimeLogModel, TimeLogModel.assignment_id == AssignmentModel.id)
            .where(AssignmentModel.project_id == project_id)
            .group_by(AssignmentModel.id)
            .offset(offset)
            .limit(pagination.page_size)
        )
        result = await self._session.execute(query)
        items = [
            AssignmentWithHours(
                assignment=AssignmentMapper.to_entity(row.AssignmentModel),
                total_hours=row.total_hours,
            )
            for row in result.all()
        ]

        return PaginatedResult(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )

    async def find_by_project_and_member(
        self,
        project_id: int,
        team_member_id: int,
    ) -> Optional[AssignmentEntity]:
        result = await self._session.execute(
            select(AssignmentModel).where(
                and_(
                    AssignmentModel.project_id == project_id,
                    AssignmentModel.team_member_id == team_member_id,
                    AssignmentModel.status == AssignmentStatus.ACTIVE,
                )
            )
        )
        orm = result.scalar_one_or_none()
        return AssignmentMapper.to_entity(orm) if orm else None

    async def update(self, assignment: AssignmentEntity) -> AssignmentEntity:
        orm = await self._session.get(AssignmentModel, assignment.id)
        orm.status = assignment.status
        orm.assignment_role = assignment.assignment_role
        orm.end_date = assignment.end_date
        orm.updated_at = assignment.updated_at
        await self._session.flush()
        await self._session.refresh(orm)
        return AssignmentMapper.to_entity(orm)
