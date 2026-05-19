from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional

from app.domain.entity.project_entity import (
    ProjectEntity,
    ProjectStatus,
    ProjectPriority,
)


@dataclass(frozen=True)
class ProjectFilters:
    status: Optional[ProjectStatus] = None
    priority: Optional[ProjectPriority] = None
    name: Optional[str] = None


@dataclass(frozen=True)
class ProjectSummary:
    project: ProjectEntity
    total_assignments: int
    active_assignments: int
    total_logged_hours: Decimal
    last_activity_date: Optional[date]
