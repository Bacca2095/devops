import pytest
from unittest.mock import AsyncMock

from app.application.use_cases.assignment.update_assignment_status import (
    UpdateAssignmentStatusCommand,
    UpdateAssignmentStatusUseCase,
)
from app.domain.entity.assignment_entity import AssignmentEntity, AssignmentStatus
from app.domain.exceptions.business_rules import InvalidAssignmentStatusTransitionException
from app.domain.exceptions.not_found import AssignmentNotFoundException


def _make_use_case(assignment_repo: AsyncMock) -> UpdateAssignmentStatusUseCase:
    return UpdateAssignmentStatusUseCase(assignment_repository=assignment_repo)


class TestUpdateAssignmentStatusNotFound:
    async def test_assignment_not_found_raises(self, mock_assignment_repo: AsyncMock):
        mock_assignment_repo.find_by_id.return_value = None

        use_case = _make_use_case(mock_assignment_repo)

        with pytest.raises(AssignmentNotFoundException):
            await use_case.execute(
                UpdateAssignmentStatusCommand(assignment_id=999, status=AssignmentStatus.COMPLETED)
            )


class TestUpdateAssignmentStatusTransitions:
    async def test_complete_active_assignment(
        self,
        mock_assignment_repo: AsyncMock,
        an_active_assignment: AssignmentEntity,
    ):
        mock_assignment_repo.find_by_id.return_value = an_active_assignment
        mock_assignment_repo.update.return_value = an_active_assignment

        use_case = _make_use_case(mock_assignment_repo)
        await use_case.execute(
            UpdateAssignmentStatusCommand(
                assignment_id=an_active_assignment.id,
                status=AssignmentStatus.COMPLETED,
            )
        )

        assert an_active_assignment.status == AssignmentStatus.COMPLETED
        mock_assignment_repo.update.assert_called_once_with(an_active_assignment)

    async def test_cancel_completed_raises(
        self,
        mock_assignment_repo: AsyncMock,
        a_completed_assignment: AssignmentEntity,
    ):
        mock_assignment_repo.find_by_id.return_value = a_completed_assignment

        use_case = _make_use_case(mock_assignment_repo)

        with pytest.raises(InvalidAssignmentStatusTransitionException):
            await use_case.execute(
                UpdateAssignmentStatusCommand(
                    assignment_id=a_completed_assignment.id,
                    status=AssignmentStatus.CANCELLED,
                )
            )
