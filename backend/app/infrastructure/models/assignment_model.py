from __future__ import annotations
from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy import String, Enum, Date, DateTime, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base
from app.domain.entity.assignment_entity import AssignmentStatus

if TYPE_CHECKING:
    from app.infrastructure.models import ProjectModel, TeamMemberModel, TimeLogModel


class AssignmentModel(Base):
    __tablename__ = "assignments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    team_member_id: Mapped[int] = mapped_column(
        ForeignKey("team_members.id"), nullable=False
    )
    assignment_role: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[AssignmentStatus] = mapped_column(
        Enum(AssignmentStatus), default=AssignmentStatus.ACTIVE
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    project: Mapped[ProjectModel] = relationship(
        "ProjectModel", back_populates="assignments"
    )
    team_member: Mapped[TeamMemberModel] = relationship(
        "TeamMemberModel", back_populates="assignments"
    )
    time_logs: Mapped[list[TimeLogModel]] = relationship(
        "TimeLogModel", back_populates="assignment", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_assignments_project_status", "project_id", "status"),)
