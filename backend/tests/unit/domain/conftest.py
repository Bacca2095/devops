import pytest
from datetime import date

from app.domain.entity.assignment_entity import AssignmentEntity, AssignmentStatus
from app.domain.entity.project_entity import ProjectEntity, ProjectPriority, ProjectStatus
from app.domain.entity.team_member_entity import (
    TeamMemberEntity,
    MemberRole,
    MemberSeniority,
    MemberStatus,
)


@pytest.fixture
def active_assignment() -> AssignmentEntity:
    return AssignmentEntity(
        id=1,
        project_id=1,
        team_member_id=1,
        assignment_role="DEVELOPER",
        start_date=date(2026, 1, 1),
        status=AssignmentStatus.ACTIVE,
    )


@pytest.fixture
def completed_assignment() -> AssignmentEntity:
    return AssignmentEntity(
        id=2,
        project_id=1,
        team_member_id=2,
        assignment_role="QA",
        start_date=date(2026, 1, 1),
        status=AssignmentStatus.COMPLETED,
    )


@pytest.fixture
def active_project() -> ProjectEntity:
    return ProjectEntity(
        id=1,
        name="Test Project",
        priority=ProjectPriority.HIGH,
        start_date=date(2026, 1, 1),
        status=ProjectStatus.ACTIVE,
    )


@pytest.fixture
def active_member() -> TeamMemberEntity:
    return TeamMemberEntity(
        id=1,
        full_name="Ana García",
        email="ana@example.com",
        document_number="12345678",
        role=MemberRole.DEVELOPER,
        seniority=MemberSeniority.SENIOR,
        status=MemberStatus.ACTIVE,
    )


@pytest.fixture
def inactive_member() -> TeamMemberEntity:
    return TeamMemberEntity(
        id=2,
        full_name="Luis Pérez",
        email="luis@example.com",
        document_number="87654321",
        role=MemberRole.QA,
        seniority=MemberSeniority.JUNIOR,
        status=MemberStatus.INACTIVE,
    )
