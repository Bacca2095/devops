from app.domain.entity.assignment_entity import (
    AssignmentEntity,
    AssignmentStatus,
)
from app.infrastructure.models import AssignmentModel


class AssignmentMapper:
    @staticmethod
    def to_entity(orm: AssignmentModel) -> AssignmentEntity:
        return AssignmentEntity(
            id=orm.id,
            project_id=orm.project_id,
            team_member_id=orm.team_member_id,
            assignment_role=orm.assignment_role,
            start_date=orm.start_date,
            end_date=orm.end_date,
            status=AssignmentStatus(orm.status),
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_model(entity: AssignmentEntity) -> AssignmentModel:
        return AssignmentModel(
            id=entity.id,
            project_id=entity.project_id,
            team_member_id=entity.team_member_id,
            assignment_role=entity.assignment_role,
            start_date=entity.start_date,
            end_date=entity.end_date,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
