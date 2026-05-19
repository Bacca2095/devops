import { axiosClient } from '@/api/client';
import type { Assignment, CreateAssignmentDto, UpdateAssignmentStatusDto } from '@/types/assignment';
import type { PaginatedResponse } from '@/types/common';

const assignmentsApi = {
  findByProject: (projectId: number, page = 1, pageSize = 20) =>
    axiosClient
      .get<PaginatedResponse<Assignment>>(`/api/projects/${projectId}/assignments`, {
        params: { page, page_size: pageSize },
      })
      .then(r => r.data),

  create: (projectId: number, data: CreateAssignmentDto) =>
    axiosClient.post<Assignment>(`/api/projects/${projectId}/assignments`, data).then(r => r.data),

  updateStatus: (id: number, data: UpdateAssignmentStatusDto) =>
    axiosClient.patch<Assignment>(`/api/assignments/${id}/status`, data).then(r => r.data),
};

export { assignmentsApi };
