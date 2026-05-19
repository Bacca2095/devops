import pytest
from datetime import date
from decimal import Decimal
from unittest.mock import AsyncMock

from app.application.use_cases.time_log.create_time_log import (
    CreateTimeLogCommand,
    CreateTimeLogUseCase,
)
from app.domain.entity.assignment_entity import AssignmentEntity
from app.domain.entity.time_log_entity import TimeLogEntity
from app.domain.exceptions.business_rules import InactiveAssignmentException, InvalidHoursException
from app.domain.exceptions.not_found import AssignmentNotFoundException


def _make_use_case(assignment_repo: AsyncMock, time_log_repo: AsyncMock) -> CreateTimeLogUseCase:
    return CreateTimeLogUseCase(
        assignment_repository=assignment_repo,
        time_log_repository=time_log_repo,
    )


def _command(assignment_id: int = 100, hours: str = "8") -> CreateTimeLogCommand:
    return CreateTimeLogCommand(
        assignment_id=assignment_id,
        logged_date=date.today(),
        hours=Decimal(hours),
    )


class TestCreateTimeLogNotFound:
    async def test_assignment_not_found_raises(
        self,
        mock_assignment_repo: AsyncMock,
        mock_time_log_repo: AsyncMock,
    ):
        mock_assignment_repo.find_by_id.return_value = None

        use_case = _make_use_case(mock_assignment_repo, mock_time_log_repo)

        with pytest.raises(AssignmentNotFoundException):
            await use_case.execute(_command())


class TestCreateTimeLogBusinessRules:
    async def test_inactive_assignment_raises(
        self,
        mock_assignment_repo: AsyncMock,
        mock_time_log_repo: AsyncMock,
        a_completed_assignment: AssignmentEntity,
    ):
        mock_assignment_repo.find_by_id.return_value = a_completed_assignment

        use_case = _make_use_case(mock_assignment_repo, mock_time_log_repo)

        with pytest.raises(InactiveAssignmentException):
            await use_case.execute(_command())

    async def test_invalid_hours_raises(
        self,
        mock_assignment_repo: AsyncMock,
        mock_time_log_repo: AsyncMock,
        an_active_assignment: AssignmentEntity,
    ):
        mock_assignment_repo.find_by_id.return_value = an_active_assignment

        use_case = _make_use_case(mock_assignment_repo, mock_time_log_repo)

        with pytest.raises(InvalidHoursException):
            await use_case.execute(_command(hours="0.3"))

    async def test_happy_path_logs_hours(
        self,
        mock_assignment_repo: AsyncMock,
        mock_time_log_repo: AsyncMock,
        an_active_assignment: AssignmentEntity,
    ):
        expected_log = TimeLogEntity(
            assignment_id=100,
            logged_date=date.today(),
            hours=Decimal("8"),
        )
        mock_assignment_repo.find_by_id.return_value = an_active_assignment
        mock_time_log_repo.create.return_value = expected_log

        use_case = _make_use_case(mock_assignment_repo, mock_time_log_repo)
        result = await use_case.execute(_command())

        mock_time_log_repo.create.assert_called_once()
        assert result.hours == Decimal("8")
