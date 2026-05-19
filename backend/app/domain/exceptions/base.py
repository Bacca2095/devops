from datetime import datetime, timezone


class DomainException(Exception):
    code: str = "INTERNAL_ERROR"

    def __init__(self, message: str) -> None:
        self.message = message
        self.timestamp = datetime.now(timezone.utc)
        super().__init__(message)


class NotFoundException(DomainException):
    pass


class ConflictException(DomainException):
    pass


class BusinessRuleException(DomainException):
    pass
