import { useQuery, useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { teamMembersApi } from '@/api/team-members/team-members.api';
import type { NormalizedError } from '@/api/client';
import type { TeamMemberFilters, CreateTeamMemberDto, UpdateTeamMemberDto, UpdateTeamMemberStatusDto } from '@/types/team-member';

const teamMemberKeys = {
  all: ['team-members'] as const,
  list: (filters: TeamMemberFilters) => ['team-members', 'list', filters] as const,
  detail: (id: number) => ['team-members', 'detail', id] as const,
};

const onMutationError = (error: unknown) => {
  const { message } = error as NormalizedError;
  toast.error('Error', { description: message });
};

const useTeamMembers = (filters: TeamMemberFilters = {}) =>
  useQuery({
    queryKey: teamMemberKeys.list(filters),
    queryFn: () => teamMembersApi.findAll(filters),
  });

const useTeamMember = (id: number) =>
  useQuery({
    queryKey: teamMemberKeys.detail(id),
    queryFn: () => teamMembersApi.findById(id),
  });

const useCreateTeamMember = () =>
  useMutation({
    mutationFn: (data: CreateTeamMemberDto) => teamMembersApi.create(data),
    onError: onMutationError,
  });

const useUpdateTeamMember = () =>
  useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateTeamMemberDto }) =>
      teamMembersApi.update(id, data),
    onError: onMutationError,
  });

const useUpdateTeamMemberStatus = () =>
  useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateTeamMemberStatusDto }) =>
      teamMembersApi.updateStatus(id, data),
    onError: onMutationError,
  });

export { teamMemberKeys, useTeamMembers, useTeamMember, useCreateTeamMember, useUpdateTeamMember, useUpdateTeamMemberStatus };
