from app.domain.entity.time_log_entity import TimeLogEntity
from app.infrastructure.models import TimeLogModel


class TimeLogMapper:
    @staticmethod
    def to_entity(orm: TimeLogModel) -> TimeLogEntity:
        return TimeLogEntity(
            id=orm.id,
            assignment_id=orm.assignment_id,
            logged_date=orm.logged_date,
            hours=orm.hours,
            description=orm.description,
            created_at=orm.created_at,
        )

    @staticmethod
    def to_model(entity: TimeLogEntity) -> TimeLogModel:
        return TimeLogModel(
            id=entity.id,
            assignment_id=entity.assignment_id,
            logged_date=entity.logged_date,
            hours=entity.hours,
            description=entity.description,
            created_at=entity.created_at,
        )
