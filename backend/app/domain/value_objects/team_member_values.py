from dataclasses import dataclass
from typing import Optional

from app.domain.entity.team_member_entity import (
    MemberRole,
    MemberSeniority,
    MemberStatus,
)


@dataclass(frozen=True)
class TeamMemberFilters:
    status: Optional[MemberStatus] = None
    role: Optional[MemberRole] = None
    seniority: Optional[MemberSeniority] = None
