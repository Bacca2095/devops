from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional

from app.domain.exceptions.business_rules import InvalidProjectStatusTransitionException


class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ON_HOLD = "ON_HOLD"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ProjectPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class ProjectEntity:
    name: str
    priority: ProjectPriority
    start_date: date
    status: ProjectStatus = ProjectStatus.ACTIVE
    description: Optional[str] = None
    end_date: Optional[date] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(
        self,
        name: str,
        priority: ProjectPriority,
        start_date: date,
        description: Optional[str] = None,
        end_date: Optional[date] = None,
    ) -> None:
        self.name = name
        self.priority = priority
        self.start_date = start_date
        self.description = description
        self.end_date = end_date
        self.updated_at = datetime.now()

    def change_status(self, new_status: ProjectStatus) -> None:
        invalid = (
            self.status == ProjectStatus.CANCELLED
            or self.status == ProjectStatus.COMPLETED and new_status == ProjectStatus.ACTIVE
        )
        if invalid:
            raise InvalidProjectStatusTransitionException(self.status, new_status)
        self.status = new_status
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        return self.status == ProjectStatus.ACTIVE
