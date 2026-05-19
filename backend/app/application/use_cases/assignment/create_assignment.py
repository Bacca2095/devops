from dataclasses import dataclass
from datetime import date
from typing import Optional

from app.domain.entity.assignment_entity import AssignmentEntity
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.exceptions.not_found import (
    ProjectNotFoundException,
    TeamMemberNotFoundException,
)
from app.domain.exceptions.conflict import DuplicateAssignmentException
from app.domain.exceptions.business_rules import InactiveTeamMemberException


@dataclass
class CreateAssignmentCommand:
    project_id: int
    team_member_id: int
    assignment_role: str
    start_date: date
    end_date: Optional[date] = None


class CreateAssignmentUseCase:
    def __init__(
        self,
        project_repository: ProjectRepository,
        team_member_repository: TeamMemberRepository,
        assignment_repository: AssignmentRepository,
    ) -> None:
        self._project_repository = project_repository
        self._team_member_repository = team_member_repository
        self._assignment_repository = assignment_repository

    async def execute(self, command: CreateAssignmentCommand) -> AssignmentEntity:
        project = await self._project_repository.find_by_id(command.project_id)
        if not project:
            raise ProjectNotFoundException(command.project_id)

        team_member = await self._team_member_repository.find_by_id(
            command.team_member_id
        )
        if not team_member:
            raise TeamMemberNotFoundException(command.team_member_id)

        if not team_member.is_active():
            raise InactiveTeamMemberException(command.team_member_id)

        existing = await self._assignment_repository.find_by_project_and_member(
            command.project_id, command.team_member_id
        )
        if existing:
            raise DuplicateAssignmentException(
                command.team_member_id, command.project_id
            )

        assignment = AssignmentEntity(
            project_id=command.project_id,
            team_member_id=command.team_member_id,
            assignment_role=command.assignment_role,
            start_date=command.start_date,
            end_date=command.end_date,
        )
        return await self._assignment_repository.create(assignment)
