import pytest

from app.domain.entity.project_entity import ProjectEntity, ProjectStatus
from app.domain.exceptions.business_rules import InvalidProjectStatusTransitionException


class TestProjectEntityStatusTransitions:
    def test_active_to_completed(self, active_project: ProjectEntity):
        active_project.change_status(ProjectStatus.COMPLETED)
        assert active_project.status == ProjectStatus.COMPLETED

    def test_active_to_on_hold(self, active_project: ProjectEntity):
        active_project.change_status(ProjectStatus.ON_HOLD)
        assert active_project.status == ProjectStatus.ON_HOLD

    def test_active_to_cancelled(self, active_project: ProjectEntity):
        active_project.change_status(ProjectStatus.CANCELLED)
        assert active_project.status == ProjectStatus.CANCELLED

    def test_cancelled_to_any_raises(self, active_project: ProjectEntity):
        active_project.change_status(ProjectStatus.CANCELLED)
        with pytest.raises(InvalidProjectStatusTransitionException):
            active_project.change_status(ProjectStatus.ACTIVE)

    def test_completed_to_active_raises(self, active_project: ProjectEntity):
        active_project.change_status(ProjectStatus.COMPLETED)
        with pytest.raises(InvalidProjectStatusTransitionException):
            active_project.change_status(ProjectStatus.ACTIVE)


class TestProjectEntityPredicates:
    def test_active_project_is_active(self, active_project: ProjectEntity):
        assert active_project.is_active() is True

    def test_completed_project_is_not_active(self, active_project: ProjectEntity):
        active_project.change_status(ProjectStatus.COMPLETED)
        assert active_project.is_active() is False
