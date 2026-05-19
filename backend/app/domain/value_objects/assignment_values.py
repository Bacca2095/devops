from dataclasses import dataclass
from decimal import Decimal

from app.domain.entity.assignment_entity import AssignmentEntity


@dataclass(frozen=True)
class AssignmentWithHours:
    assignment: AssignmentEntity
    total_hours: Decimal
