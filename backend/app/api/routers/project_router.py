from typing import Optional
from fastapi import APIRouter, Depends, Query

from app.api.dependencies.project import (
    get_create_project,
    get_find_projects,
    get_find_project_by_id,
    get_update_project,
    get_update_project_status,
    get_find_project_summary,
)
from app.api.dto.project_dto import (
    ProjectCreateDto,
    ProjectUpdateDto,
    ProjectStatusUpdateDto,
    ProjectDto,
    ProjectSummaryDto,
)
from app.api.dto.common_dto import PaginatedDto
from app.application.use_cases.project.create_project import (
    CreateProjectUseCase,
    CreateProjectCommand,
)
from app.application.use_cases.project.find_projects import (
    FindProjectsUseCase,
    FindProjectsQuery,
)
from app.application.use_cases.project.find_project_by_id import FindProjectByIdUseCase
from app.application.use_cases.project.update_project import (
    UpdateProjectUseCase,
    UpdateProjectCommand,
)
from app.application.use_cases.project.update_project_status import (
    UpdateProjectStatusUseCase,
    UpdateProjectStatusCommand,
)
from app.application.use_cases.project.find_project_summary import (
    FindProjectSummaryUseCase,
)
from app.domain.entity.project_entity import ProjectStatus, ProjectPriority
from app.domain.value_objects.project_values import ProjectFilters

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectDto, status_code=201)
async def create_project(
    body: ProjectCreateDto,
    use_case: CreateProjectUseCase = Depends(get_create_project),
) -> ProjectDto:
    project = await use_case.execute(
        CreateProjectCommand(
            name=body.name,
            priority=body.priority,
            start_date=body.start_date,
            description=body.description,
            end_date=body.end_date,
        )
    )
    return ProjectDto.from_entity(project)


@router.get("/", response_model=PaginatedDto[ProjectDto])
async def get_projects(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    status: Optional[ProjectStatus] = Query(default=None),
    priority: Optional[ProjectPriority] = Query(default=None),
    name: Optional[str] = Query(default=None),
    use_case: FindProjectsUseCase = Depends(get_find_projects),
) -> PaginatedDto[ProjectDto]:
    result = await use_case.execute(
        FindProjectsQuery(
            page=page,
            page_size=page_size,
            filters=ProjectFilters(status=status, priority=priority, name=name),
        )
    )
    return PaginatedDto.from_result(result, ProjectDto.from_entity)


@router.get("/{project_id}", response_model=ProjectDto)
async def get_project(
    project_id: int,
    use_case: FindProjectByIdUseCase = Depends(get_find_project_by_id),
) -> ProjectDto:
    project = await use_case.execute(project_id)
    return ProjectDto.from_entity(project)


@router.put("/{project_id}", response_model=ProjectDto)
async def update_project(
    project_id: int,
    body: ProjectUpdateDto,
    use_case: UpdateProjectUseCase = Depends(get_update_project),
) -> ProjectDto:
    project = await use_case.execute(
        UpdateProjectCommand(
            project_id=project_id,
            name=body.name,
            priority=body.priority,
            start_date=body.start_date,
            description=body.description,
            end_date=body.end_date,
        )
    )
    return ProjectDto.from_entity(project)


@router.patch("/{project_id}/status", response_model=ProjectDto)
async def update_project_status(
    project_id: int,
    body: ProjectStatusUpdateDto,
    use_case: UpdateProjectStatusUseCase = Depends(get_update_project_status),
) -> ProjectDto:
    project = await use_case.execute(
        UpdateProjectStatusCommand(project_id=project_id, status=body.status)
    )
    return ProjectDto.from_entity(project)


@router.get("/{project_id}/summary", response_model=ProjectSummaryDto)
async def get_project_summary(
    project_id: int,
    use_case: FindProjectSummaryUseCase = Depends(get_find_project_summary),
) -> ProjectSummaryDto:
    summary = await use_case.execute(project_id)
    return ProjectSummaryDto.from_summary(summary)
