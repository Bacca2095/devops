from typing import Optional
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entity.project_entity import ProjectEntity
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.project_values import ProjectFilters, ProjectSummary
from app.infrastructure.models import ProjectModel
from app.infrastructure.models import AssignmentModel
from app.infrastructure.models import TimeLogModel
from app.infrastructure.mappers.project_mapper import ProjectMapper


class PostgresProjectRepository(ProjectRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, project: ProjectEntity) -> ProjectEntity:
        orm = ProjectMapper.to_model(project)
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return ProjectMapper.to_entity(orm)

    async def find_by_id(self, project_id: int) -> Optional[ProjectEntity]:
        result = await self._session.get(ProjectModel, project_id)
        return ProjectMapper.to_entity(result) if result else None

    async def find_all(
        self,
        pagination: Pagination,
        filters: ProjectFilters,
    ) -> PaginatedResult[ProjectEntity]:
        query = select(ProjectModel)

        if filters.status:
            query = query.where(ProjectModel.status == filters.status)
        if filters.priority:
            query = query.where(ProjectModel.priority == filters.priority)
        if filters.name:
            query = query.where(ProjectModel.name.ilike(f"%{filters.name}%"))

        total_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()

        offset = (pagination.page - 1) * pagination.page_size
        query = query.offset(offset).limit(pagination.page_size)
        result = await self._session.execute(query)
        items = [ProjectMapper.to_entity(row) for row in result.scalars().all()]

        return PaginatedResult(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )

    async def update(self, project: ProjectEntity) -> ProjectEntity:
        orm = await self._session.get(ProjectModel, project.id)
        orm.name = project.name
        orm.description = project.description
        orm.priority = project.priority
        orm.start_date = project.start_date
        orm.end_date = project.end_date
        orm.status = project.status
        orm.updated_at = project.updated_at
        await self._session.flush()
        await self._session.refresh(orm)
        return ProjectMapper.to_entity(orm)

    async def find_summary(self, project_id: int) -> ProjectSummary:
        project = await self._session.get(ProjectModel, project_id)

        stats_result = await self._session.execute(
            select(
                func.count(AssignmentModel.id).label("total_assignments"),
                func.sum(
                    case((AssignmentModel.status == "ACTIVE", 1), else_=0)
                ).label("active_assignments"),
                func.coalesce(func.sum(TimeLogModel.hours), 0).label("total_hours"),
                func.max(TimeLogModel.logged_date).label("last_activity"),
            )
            .select_from(AssignmentModel)
            .outerjoin(TimeLogModel, TimeLogModel.assignment_id == AssignmentModel.id)
            .where(AssignmentModel.project_id == project_id)
        )
        row = stats_result.one()

        return ProjectSummary(
            project=ProjectMapper.to_entity(project),
            total_assignments=row.total_assignments or 0,
            active_assignments=row.active_assignments or 0,
            total_logged_hours=row.total_hours,
            last_activity_date=row.last_activity,
        )
