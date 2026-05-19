from app.domain.exceptions.base import ConflictException


class DuplicateEmailException(ConflictException):
    code = "DUPLICATE_EMAIL"

    def __init__(self, email: str) -> None:
        super().__init__(f"Team member with email {email} already exists")


class DuplicateDocumentException(ConflictException):
    code = "DUPLICATE_DOCUMENT"

    def __init__(self, document_number: str) -> None:
        super().__init__(f"Team member with document {document_number} already exists")


class DuplicateAssignmentException(ConflictException):
    code = "DUPLICATE_ASSIGNMENT"

    def __init__(self, team_member_id: int, project_id: int) -> None:
        super().__init__(
            f"Team member {team_member_id} is already active in project {project_id}"
        )
