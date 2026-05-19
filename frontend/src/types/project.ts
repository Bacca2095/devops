export type ProjectStatus = 'ACTIVE' | 'ON_HOLD' | 'COMPLETED' | 'CANCELLED';
export type ProjectPriority = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface Project {
  id: number;
  name: string;
  description: string | null;
  status: ProjectStatus;
  priority: ProjectPriority;
  start_date: string;
  end_date: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectSummary {
  project: Pick<Project, 'name' | 'status' | 'priority'>;
  total_assignments: number;
  active_assignments: number;
  total_logged_hours: number;
  last_activity_date: string | null;
}

export interface ProjectFilters {
  status?: ProjectStatus;
  priority?: ProjectPriority;
  name?: string;
  page?: number;
  page_size?: number;
}

export interface CreateProjectDto {
  name: string;
  description?: string;
  status?: ProjectStatus;
  priority: ProjectPriority;
  start_date: string;
  end_date?: string;
}

export type UpdateProjectDto = CreateProjectDto;

export interface UpdateProjectStatusDto {
  status: ProjectStatus;
}
