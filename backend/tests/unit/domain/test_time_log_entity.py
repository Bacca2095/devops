import pytest
from datetime import date
from decimal import Decimal

from app.domain.entity.time_log_entity import TimeLogEntity
from app.domain.exceptions.business_rules import InvalidHoursException


class TestTimeLogEntityHoursValidation:
    def test_minimum_hours_accepted(self):
        log = TimeLogEntity(assignment_id=1, logged_date=date.today(), hours=Decimal("0.5"))
        assert log.hours == Decimal("0.5")

    def test_maximum_hours_accepted(self):
        log = TimeLogEntity(assignment_id=1, logged_date=date.today(), hours=Decimal("24"))
        assert log.hours == Decimal("24")

    def test_midrange_hours_accepted(self):
        log = TimeLogEntity(assignment_id=1, logged_date=date.today(), hours=Decimal("8"))
        assert log.hours == Decimal("8")

    def test_below_minimum_raises(self):
        with pytest.raises(InvalidHoursException):
            TimeLogEntity(assignment_id=1, logged_date=date.today(), hours=Decimal("0.3"))

    def test_zero_hours_raises(self):
        with pytest.raises(InvalidHoursException):
            TimeLogEntity(assignment_id=1, logged_date=date.today(), hours=Decimal("0"))

    def test_above_maximum_raises(self):
        with pytest.raises(InvalidHoursException):
            TimeLogEntity(assignment_id=1, logged_date=date.today(), hours=Decimal("24.5"))
