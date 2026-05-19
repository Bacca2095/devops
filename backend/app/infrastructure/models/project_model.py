from __future__ import annotations
from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy import String, Text, Enum, Date, DateTime, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database import Base
from app.domain.entity.project_entity import ProjectStatus, ProjectPriority

if TYPE_CHECKING:
    from app.infrastructure.models import AssignmentModel


class ProjectModel(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.ACTIVE
    )
    priority: Mapped[ProjectPriority] = mapped_column(Enum(ProjectPriority))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    assignments: Mapped[list[AssignmentModel]] = relationship(
        "AssignmentModel", back_populates="project", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_projects_status_priority", "status", "priority"),
        Index("ix_projects_priority", "priority"),
        Index("ix_projects_name", "name"),
    )
