from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional

from app.domain.exceptions.business_rules import (
    InvalidAssignmentStatusTransitionException,
)


class AssignmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass
class AssignmentEntity:
    project_id: int
    team_member_id: int
    assignment_role: str
    start_date: date
    status: AssignmentStatus = AssignmentStatus.ACTIVE
    end_date: Optional[date] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def complete(self) -> None:
        if self.status != AssignmentStatus.ACTIVE:
            raise InvalidAssignmentStatusTransitionException(
                self.status, AssignmentStatus.COMPLETED
            )
        self.status = AssignmentStatus.COMPLETED
        self.updated_at = datetime.now()

    def cancel(self) -> None:
        if self.status == AssignmentStatus.COMPLETED:
            raise InvalidAssignmentStatusTransitionException(
                self.status, AssignmentStatus.CANCELLED
            )
        self.status = AssignmentStatus.CANCELLED
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        return self.status == AssignmentStatus.ACTIVE

    def accepts_time_logs(self) -> bool:
        return self.status == AssignmentStatus.ACTIVE
