import { axiosClient } from '@/api/client';
import type { Project, ProjectFilters, ProjectSummary, CreateProjectDto, UpdateProjectDto, UpdateProjectStatusDto } from '@/types/project';
import type { PaginatedResponse } from '@/types/common';

const projectsApi = {
  findAll: (filters?: ProjectFilters) =>
    axiosClient.get<PaginatedResponse<Project>>('/api/projects/', { params: filters }).then(r => r.data),

  findById: (id: number) =>
    axiosClient.get<Project>(`/api/projects/${id}`).then(r => r.data),

  getSummary: (id: number) =>
    axiosClient.get<ProjectSummary>(`/api/projects/${id}/summary`).then(r => r.data),

  create: (data: CreateProjectDto) =>
    axiosClient.post<Project>('/api/projects/', data).then(r => r.data),

  update: (id: number, data: UpdateProjectDto) =>
    axiosClient.put<Project>(`/api/projects/${id}`, data).then(r => r.data),

  updateStatus: (id: number, data: UpdateProjectStatusDto) =>
    axiosClient.patch<Project>(`/api/projects/${id}/status`, data).then(r => r.data),
};

export { projectsApi };
