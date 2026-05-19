from app.domain.exceptions.base import BusinessRuleException


class InactiveTeamMemberException(BusinessRuleException):
    code = "TEAM_MEMBER_INACTIVE"

    def __init__(self, team_member_id: int) -> None:
        super().__init__(
            f"Team member {team_member_id} is inactive and cannot be assigned"
        )


class InactiveAssignmentException(BusinessRuleException):
    code = "ASSIGNMENT_INACTIVE"

    def __init__(self, assignment_id: int) -> None:
        super().__init__(
            f"Assignment {assignment_id} is not active and cannot log hours"
        )


class InvalidHoursException(BusinessRuleException):
    code = "INVALID_HOURS"

    def __init__(self, hours: float) -> None:
        super().__init__(f"Hours {hours} is invalid, must be between 0.5 and 24")


class InvalidProjectStatusTransitionException(BusinessRuleException):
    code = "INVALID_PROJECT_STATUS_TRANSITION"

    def __init__(self, current_status: str, new_status: str) -> None:
        super().__init__(
            f"Cannot transition project from {current_status} to {new_status}"
        )


class InvalidAssignmentStatusTransitionException(BusinessRuleException):
    code = "INVALID_ASSIGNMENT_STATUS_TRANSITION"

    def __init__(self, current_status: str, new_status: str) -> None:
        super().__init__(
            f"Cannot transition assignment from {current_status} to {new_status}"
        )
