from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from app.domain.entity.time_log_entity import TimeLogEntity


class TimeLogCreateDto(BaseModel):
    logged_date: date
    hours: Decimal = Field(..., decimal_places=1)
    description: Optional[str] = None


class TimeLogDto(BaseModel):
    id: int
    assignment_id: int
    logged_date: date
    hours: Decimal
    description: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_entity(cls, entity: TimeLogEntity) -> "TimeLogDto":
        return cls.model_validate(entity.__dict__)
