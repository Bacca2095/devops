import pytest

from app.domain.entity.assignment_entity import AssignmentEntity, AssignmentStatus
from app.domain.exceptions.business_rules import InvalidAssignmentStatusTransitionException


class TestAssignmentEntityStatusTransitions:
    def test_complete_active_assignment(self, active_assignment: AssignmentEntity):
        active_assignment.complete()
        assert active_assignment.status == AssignmentStatus.COMPLETED

    def test_cancel_active_assignment(self, active_assignment: AssignmentEntity):
        active_assignment.cancel()
        assert active_assignment.status == AssignmentStatus.CANCELLED

    def test_complete_already_completed_raises(self, completed_assignment: AssignmentEntity):
        with pytest.raises(InvalidAssignmentStatusTransitionException):
            completed_assignment.complete()

    def test_cancel_completed_raises(self, completed_assignment: AssignmentEntity):
        with pytest.raises(InvalidAssignmentStatusTransitionException):
            completed_assignment.cancel()


class TestAssignmentEntityPredicates:
    def test_active_assignment_accepts_time_logs(self, active_assignment: AssignmentEntity):
        assert active_assignment.accepts_time_logs() is True

    def test_completed_assignment_rejects_time_logs(self, completed_assignment: AssignmentEntity):
        assert completed_assignment.accepts_time_logs() is False

    def test_active_assignment_is_active(self, active_assignment: AssignmentEntity):
        assert active_assignment.is_active() is True

    def test_completed_assignment_is_not_active(self, completed_assignment: AssignmentEntity):
        assert completed_assignment.is_active() is False
