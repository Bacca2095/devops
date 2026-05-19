from datetime import date, datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, Field

from app.domain.entity.project_entity import (
    ProjectEntity,
    ProjectStatus,
    ProjectPriority,
)
from app.domain.value_objects.project_values import ProjectSummary


class ProjectCreateDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    priority: ProjectPriority
    start_date: date
    description: Optional[str] = None
    end_date: Optional[date] = None


class ProjectUpdateDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    priority: ProjectPriority
    start_date: date
    description: Optional[str] = None
    end_date: Optional[date] = None


class ProjectStatusUpdateDto(BaseModel):
    status: ProjectStatus


class ProjectDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    priority: ProjectPriority
    start_date: date
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_entity(cls, entity: ProjectEntity) -> "ProjectDto":
        return cls.model_validate(entity.__dict__)


class ProjectSummaryDto(BaseModel):
    project: ProjectDto
    total_assignments: int
    active_assignments: int
    total_logged_hours: Decimal
    last_activity_date: Optional[date]

    @classmethod
    def from_summary(cls, summary: ProjectSummary) -> "ProjectSummaryDto":
        return cls(
            project=ProjectDto.from_entity(summary.project),
            total_assignments=summary.total_assignments,
            active_assignments=summary.active_assignments,
            total_logged_hours=summary.total_logged_hours,
            last_activity_date=summary.last_activity_date,
        )
