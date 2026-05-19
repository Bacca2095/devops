from app.domain.entity.project_entity import (
    ProjectEntity,
    ProjectStatus,
    ProjectPriority,
)
from app.infrastructure.models import ProjectModel


class ProjectMapper:
    @staticmethod
    def to_entity(orm: ProjectModel) -> ProjectEntity:
        return ProjectEntity(
            id=orm.id,
            name=orm.name,
            description=orm.description,
            status=ProjectStatus(orm.status),
            priority=ProjectPriority(orm.priority),
            start_date=orm.start_date,
            end_date=orm.end_date,
            created_at=orm.created_at,
            updated_at=orm.updated_at,
        )

    @staticmethod
    def to_model(entity: ProjectEntity) -> ProjectModel:
        return ProjectModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            status=entity.status,
            priority=entity.priority,
            start_date=entity.start_date,
            end_date=entity.end_date,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
