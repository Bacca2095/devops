from typing import Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entity.team_member_entity import TeamMemberEntity
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.value_objects.pagination import PaginatedResult, Pagination
from app.domain.value_objects.team_member_values import TeamMemberFilters
from app.infrastructure.models import TeamMemberModel
from app.infrastructure.mappers.team_member_mapper import TeamMemberMapper


class PostgresTeamMemberRepository(TeamMemberRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, team_member: TeamMemberEntity) -> TeamMemberEntity:
        orm = TeamMemberMapper.to_model(team_member)
        self._session.add(orm)
        await self._session.flush()
        await self._session.refresh(orm)
        return TeamMemberMapper.to_entity(orm)

    async def find_by_id(self, team_member_id: int) -> Optional[TeamMemberEntity]:
        result = await self._session.get(TeamMemberModel, team_member_id)
        return TeamMemberMapper.to_entity(result) if result else None

    async def find_by_email(self, email: str) -> Optional[TeamMemberEntity]:
        result = await self._session.execute(
            select(TeamMemberModel).where(TeamMemberModel.email == email)
        )
        orm = result.scalar_one_or_none()
        return TeamMemberMapper.to_entity(orm) if orm else None

    async def find_all(
        self,
        pagination: Pagination,
        filters: TeamMemberFilters,
    ) -> PaginatedResult[TeamMemberEntity]:
        query = select(TeamMemberModel)

        if filters.status:
            query = query.where(TeamMemberModel.status == filters.status)
        if filters.role:
            query = query.where(TeamMemberModel.role == filters.role)
        if filters.seniority:
            query = query.where(TeamMemberModel.seniority == filters.seniority)

        total_result = await self._session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = total_result.scalar_one()

        offset = (pagination.page - 1) * pagination.page_size
        query = query.offset(offset).limit(pagination.page_size)
        result = await self._session.execute(query)
        items = [TeamMemberMapper.to_entity(row) for row in result.scalars().all()]

        return PaginatedResult(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
        )

    async def update(self, team_member: TeamMemberEntity) -> TeamMemberEntity:
        orm = await self._session.get(TeamMemberModel, team_member.id)
        orm.full_name = team_member.full_name
        orm.email = team_member.email
        orm.document_number = team_member.document_number
        orm.role = team_member.role
        orm.seniority = team_member.seniority
        orm.status = team_member.status
        orm.updated_at = team_member.updated_at
        await self._session.flush()
        await self._session.refresh(orm)
        return TeamMemberMapper.to_entity(orm)
