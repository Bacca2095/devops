from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, Enum, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base
from app.domain.entity.team_member_entity import (
    MemberRole,
    MemberSeniority,
    MemberStatus,
)

if TYPE_CHECKING:
    from app.infrastructure.models import AssignmentModel


class TeamMemberModel(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    document_number: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    role: Mapped[MemberRole] = mapped_column(Enum(MemberRole))
    seniority: Mapped[MemberSeniority] = mapped_column(Enum(MemberSeniority))
    status: Mapped[MemberStatus] = mapped_column(
        Enum(MemberStatus), default=MemberStatus.ACTIVE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    assignments: Mapped[list[AssignmentModel]] = relationship(
        "AssignmentModel", back_populates="team_member"
    )

    __table_args__ = (
        Index("ix_team_members_role_seniority", "role", "seniority"),
        Index("ix_team_members_status", "status"),
        Index("ix_team_members_seniority", "seniority"),
    )
