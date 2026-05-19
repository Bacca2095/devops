from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.infrastructure.repositories.assignment_repository import (
    PostgresAssignmentRepository,
)
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.interfaces.project_repository import ProjectRepository
from app.domain.interfaces.team_member_repository import TeamMemberRepository
from app.api.dependencies.project import get_project_repository
from app.api.dependencies.team_member import get_team_member_repository
from app.application.use_cases.assignment.create_assignment import (
    CreateAssignmentUseCase,
)
from app.application.use_cases.assignment.find_assignments_by_project import (
    FindAssignmentsByProjectUseCase,
)
from app.application.use_cases.assignment.update_assignment_status import (
    UpdateAssignmentStatusUseCase,
)


def get_assignment_repository(
    db: AsyncSession = Depends(get_db),
) -> AssignmentRepository:
    return PostgresAssignmentRepository(db)


def get_create_assignment(
    project_repo: ProjectRepository = Depends(get_project_repository),
    team_member_repo: TeamMemberRepository = Depends(get_team_member_repository),
    assignment_repo: AssignmentRepository = Depends(get_assignment_repository),
) -> CreateAssignmentUseCase:
    return CreateAssignmentUseCase(project_repo, team_member_repo, assignment_repo)


def get_find_assignments_by_project(
    project_repo: ProjectRepository = Depends(get_project_repository),
    assignment_repo: AssignmentRepository = Depends(get_assignment_repository),
) -> FindAssignmentsByProjectUseCase:
    return FindAssignmentsByProjectUseCase(project_repo, assignment_repo)


def get_update_assignment_status(
    repo: AssignmentRepository = Depends(get_assignment_repository),
) -> UpdateAssignmentStatusUseCase:
    return UpdateAssignmentStatusUseCase(repo)
