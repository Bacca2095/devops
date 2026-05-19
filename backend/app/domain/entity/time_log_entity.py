from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from app.domain.exceptions.business_rules import InvalidHoursException


@dataclass
class TimeLogEntity:
    assignment_id: int
    logged_date: date
    hours: Decimal
    description: Optional[str] = None
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        self._validate_hours()

    def _validate_hours(self) -> None:
        if not (Decimal("0.5") <= self.hours <= Decimal("24")):
            raise InvalidHoursException(self.hours)
