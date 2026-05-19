import { axiosClient } from '@/api/client';
import type { TeamMember, TeamMemberFilters, CreateTeamMemberDto, UpdateTeamMemberDto, UpdateTeamMemberStatusDto } from '@/types/team-member';
import type { PaginatedResponse } from '@/types/common';

const teamMembersApi = {
  findAll: (filters?: TeamMemberFilters) =>
    axiosClient.get<PaginatedResponse<TeamMember>>('/api/team-members/', { params: filters }).then(r => r.data),

  findById: (id: number) =>
    axiosClient.get<TeamMember>(`/api/team-members/${id}`).then(r => r.data),

  create: (data: CreateTeamMemberDto) =>
    axiosClient.post<TeamMember>('/api/team-members/', data).then(r => r.data),

  update: (id: number, data: UpdateTeamMemberDto) =>
    axiosClient.put<TeamMember>(`/api/team-members/${id}`, data).then(r => r.data),

  updateStatus: (id: number, data: UpdateTeamMemberStatusDto) =>
    axiosClient.patch<TeamMember>(`/api/team-members/${id}/status`, data).then(r => r.data),
};

export { teamMembersApi };
