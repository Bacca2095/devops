from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from app.domain.entity.assignment_entity import AssignmentStatus
from app.domain.value_objects.assignment_values import AssignmentWithHours


class AssignmentCreateDto(BaseModel):
    team_member_id: int
    assignment_role: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: Optional[date] = None


class AssignmentStatusUpdateDto(BaseModel):
    status: AssignmentStatus


class AssignmentDto(BaseModel):
    id: int
    project_id: int
    team_member_id: int
    assignment_role: str
    start_date: date
    end_date: Optional[date]
    status: AssignmentStatus
    total_hours: Decimal
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, item: AssignmentWithHours) -> "AssignmentDto":
        a = item.assignment
        return cls(
            id=a.id,
            project_id=a.project_id,
            team_member_id=a.team_member_id,
            assignment_role=a.assignment_role,
            start_date=a.start_date,
            end_date=a.end_date,
            status=a.status,
            total_hours=item.total_hours,
            created_at=a.created_at,
            updated_at=a.updated_at,
        )
