import pytest
from datetime import date
from unittest.mock import AsyncMock

from app.application.use_cases.assignment.create_assignment import (
    CreateAssignmentCommand,
    CreateAssignmentUseCase,
)
from app.domain.entity.assignment_entity import AssignmentEntity
from app.domain.entity.project_entity import ProjectEntity
from app.domain.entity.team_member_entity import TeamMemberEntity
from app.domain.exceptions.business_rules import InactiveTeamMemberException
from app.domain.exceptions.conflict import DuplicateAssignmentException
from app.domain.exceptions.not_found import ProjectNotFoundException, TeamMemberNotFoundException


def _make_use_case(
    project_repo: AsyncMock,
    member_repo: AsyncMock,
    assignment_repo: AsyncMock,
) -> CreateAssignmentUseCase:
    return CreateAssignmentUseCase(
        project_repository=project_repo,
        team_member_repository=member_repo,
        assignment_repository=assignment_repo,
    )


def _command(project_id: int = 1, team_member_id: int = 10) -> CreateAssignmentCommand:
    return CreateAssignmentCommand(
        project_id=project_id,
        team_member_id=team_member_id,
        assignment_role="DEVELOPER",
        start_date=date(2026, 1, 1),
    )


class TestCreateAssignmentNotFound:
    async def test_project_not_found_raises(
        self,
        mock_project_repo: AsyncMock,
        mock_team_member_repo: AsyncMock,
        mock_assignment_repo: AsyncMock,
    ):
        mock_project_repo.find_by_id.return_value = None

        use_case = _make_use_case(mock_project_repo, mock_team_member_repo, mock_assignment_repo)

        with pytest.raises(ProjectNotFoundException):
            await use_case.execute(_command())

    async def test_team_member_not_found_raises(
        self,
        mock_project_repo: AsyncMock,
        mock_team_member_repo: AsyncMock,
        mock_assignment_repo: AsyncMock,
        a_project: ProjectEntity,
    ):
        mock_project_repo.find_by_id.return_value = a_project
        mock_team_member_repo.find_by_id.return_value = None

        use_case = _make_use_case(mock_project_repo, mock_team_member_repo, mock_assignment_repo)

        with pytest.raises(TeamMemberNotFoundException):
            await use_case.execute(_command())


class TestCreateAssignmentBusinessRules:
    async def test_inactive_member_raises(
        self,
        mock_project_repo: AsyncMock,
        mock_team_member_repo: AsyncMock,
        mock_assignment_repo: AsyncMock,
        a_project: ProjectEntity,
        an_inactive_member: TeamMemberEntity,
    ):
        mock_project_repo.find_by_id.return_value = a_project
        mock_team_member_repo.find_by_id.return_value = an_inactive_member

        use_case = _make_use_case(mock_project_repo, mock_team_member_repo, mock_assignment_repo)

        with pytest.raises(InactiveTeamMemberException):
            await use_case.execute(_command())

    async def test_duplicate_assignment_raises(
        self,
        mock_project_repo: AsyncMock,
        mock_team_member_repo: AsyncMock,
        mock_assignment_repo: AsyncMock,
        a_project: ProjectEntity,
        an_active_member: TeamMemberEntity,
        an_active_assignment: AssignmentEntity,
    ):
        mock_project_repo.find_by_id.return_value = a_project
        mock_team_member_repo.find_by_id.return_value = an_active_member
        mock_assignment_repo.find_by_project_and_member.return_value = an_active_assignment

        use_case = _make_use_case(mock_project_repo, mock_team_member_repo, mock_assignment_repo)

        with pytest.raises(DuplicateAssignmentException):
            await use_case.execute(_command())

    async def test_happy_path_creates_assignment(
        self,
        mock_project_repo: AsyncMock,
        mock_team_member_repo: AsyncMock,
        mock_assignment_repo: AsyncMock,
        a_project: ProjectEntity,
        an_active_member: TeamMemberEntity,
        an_active_assignment: AssignmentEntity,
    ):
        mock_project_repo.find_by_id.return_value = a_project
        mock_team_member_repo.find_by_id.return_value = an_active_member
        mock_assignment_repo.find_by_project_and_member.return_value = None
        mock_assignment_repo.create.return_value = an_active_assignment

        use_case = _make_use_case(mock_project_repo, mock_team_member_repo, mock_assignment_repo)
        result = await use_case.execute(_command())

        mock_assignment_repo.create.assert_called_once()
        assert result == an_active_assignment
