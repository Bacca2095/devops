from app.domain.entity.team_member_entity import (
    TeamMemberEntity,
    MemberRole,
    MemberSeniority,
    MemberStatus,
)
from app.infrastructure.models import TeamMemberModel


class TeamMemberMapper:
    @staticmethod
    def to_entity(orm: TeamMemberModel) -> TeamMemberEntity:
        return TeamMemberEntity(
            id=orm.id,
            full_name=orm.full_name,
            email=orm.email,
            document_number=orm.document_number,
            role=MemberRole(orm.role),
            seniority=MemberSeniority(orm.seniority),
            status=MemberStatus(orm.status),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_model(entity: TeamMemberEntity) -> TeamMemberModel:
        return TeamMemberModel(
            id=entity.id,
            full_name=entity.full_name,
            email=entity.email,
            document_number=entity.document_number,
            role=entity.role,
            seniority=entity.seniority,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
