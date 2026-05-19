import pytest
from datetime import date
from unittest.mock import AsyncMock

from app.domain.entity.assignment_entity import AssignmentEntity, AssignmentStatus
from app.domain.entity.project_entity import ProjectEntity, ProjectPriority, ProjectStatus
from app.domain.entity.team_member_entity import (
    TeamMemberEntity,
    MemberRole,
    MemberSeniority,
    MemberStatus,
)


@pytest.fixture
def mock_project_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_team_member_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_assignment_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def mock_time_log_repo() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def a_project() -> ProjectEntity:
    return ProjectEntity(
        id=1,
        name="Alpha",
        priority=ProjectPriority.HIGH,
        start_date=date(2026, 1, 1),
        status=ProjectStatus.ACTIVE,
    )


@pytest.fixture
def an_active_member() -> TeamMemberEntity:
    return TeamMemberEntity(
        id=10,
        full_name="Ana García",
        email="ana@example.com",
        document_number="12345678",
        role=MemberRole.DEVELOPER,
        seniority=MemberSeniority.SENIOR,
        status=MemberStatus.ACTIVE,
    )


@pytest.fixture
def an_inactive_member() -> TeamMemberEntity:
    return TeamMemberEntity(
        id=11,
        full_name="Luis Pérez",
        email="luis@example.com",
        document_number="87654321",
        role=MemberRole.QA,
        seniority=MemberSeniority.JUNIOR,
        status=MemberStatus.INACTIVE,
    )


@pytest.fixture
def an_active_assignment() -> AssignmentEntity:
    return AssignmentEntity(
        id=100,
        project_id=1,
        team_member_id=10,
        assignment_role="DEVELOPER",
        start_date=date(2026, 1, 1),
        status=AssignmentStatus.ACTIVE,
    )


@pytest.fixture
def a_completed_assignment() -> AssignmentEntity:
    return AssignmentEntity(
        id=101,
        project_id=1,
        team_member_id=10,
        assignment_role="DEVELOPER",
        start_date=date(2026, 1, 1),
        status=AssignmentStatus.COMPLETED,
    )
