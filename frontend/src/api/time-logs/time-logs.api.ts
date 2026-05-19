import { axiosClient } from '@/api/client';
import type { TimeLog, CreateTimeLogDto } from '@/types/time-log';
import type { PaginatedResponse } from '@/types/common';

const timeLogsApi = {
  findByAssignment: (assignmentId: number, page = 1, pageSize = 20) =>
    axiosClient
      .get<PaginatedResponse<TimeLog>>(`/api/assignments/${assignmentId}/timelogs`, {
        params: { page, page_size: pageSize },
      })
      .then(r => r.data),

  create: (assignmentId: number, data: CreateTimeLogDto) =>
    axiosClient.post<TimeLog>(`/api/assignments/${assignmentId}/timelogs`, data).then(r => r.data),
};

export { timeLogsApi };
