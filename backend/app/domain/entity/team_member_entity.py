from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class MemberRole(str, Enum):
    DEVELOPER = "DEVELOPER"
    ANALYST = "ANALYST"
    ARCHITECT = "ARCHITECT"
    QA = "QA"
    DEVOPS = "DEVOPS"


class MemberSeniority(str, Enum):
    JUNIOR = "JUNIOR"
    MIDDLE = "MIDDLE"
    SENIOR = "SENIOR"


class MemberStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


@dataclass
class TeamMemberEntity:
    full_name: str
    email: str
    document_number: str
    role: MemberRole
    seniority: MemberSeniority
    status: MemberStatus = MemberStatus.ACTIVE
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update(
        self,
        full_name: str,
        email: str,
        document_number: str,
        role: MemberRole,
        seniority: MemberSeniority,
    ) -> None:
        self.full_name = full_name
        self.email = email
        self.document_number = document_number
        self.role = role
        self.seniority = seniority
        self.updated_at = datetime.now()

    def activate(self) -> None:
        self.status = MemberStatus.ACTIVE
        self.updated_at = datetime.now()

    def deactivate(self) -> None:
        self.status = MemberStatus.INACTIVE
        self.updated_at = datetime.now()

    def is_active(self) -> bool:
        return self.status == MemberStatus.ACTIVE
