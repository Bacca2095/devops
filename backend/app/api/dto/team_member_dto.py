from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.domain.entity.team_member_entity import (
    TeamMemberEntity,
    MemberRole,
    MemberSeniority,
    MemberStatus,
)


class TeamMemberCreateDto(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    document_number: str = Field(..., min_length=1, max_length=100)
    role: MemberRole
    seniority: MemberSeniority


class TeamMemberUpdateDto(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    document_number: str = Field(..., min_length=1, max_length=100)
    role: MemberRole
    seniority: MemberSeniority


class TeamMemberStatusUpdateDto(BaseModel):
    status: MemberStatus


class TeamMemberDto(BaseModel):
    id: int
    full_name: str
    email: str
    document_number: str
    role: MemberRole
    seniority: MemberSeniority
    status: MemberStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_entity(cls, entity: TeamMemberEntity) -> "TeamMemberDto":
        return cls.model_validate(entity.__dict__)
