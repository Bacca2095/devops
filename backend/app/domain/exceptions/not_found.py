from app.domain.exceptions.base import NotFoundException


class ProjectNotFoundException(NotFoundException):
    code = "PROJECT_NOT_FOUND"

    def __init__(self, project_id: int) -> None:
        super().__init__(f"Project with id {project_id} not found")


class TeamMemberNotFoundException(NotFoundException):
    code = "TEAM_MEMBER_NOT_FOUND"

    def __init__(self, team_member_id: int) -> None:
        super().__init__(f"Team member with id {team_member_id} not found")


class AssignmentNotFoundException(NotFoundException):
    code = "ASSIGNMENT_NOT_FOUND"

    def __init__(self, assignment_id: int) -> None:
        super().__init__(f"Assignment with id {assignment_id} not found")
