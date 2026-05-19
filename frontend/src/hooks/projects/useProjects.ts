import { useQuery, useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { projectsApi } from '@/api/projects/projects.api';
import type { NormalizedError } from '@/api/client';
import type { ProjectFilters, CreateProjectDto, UpdateProjectDto, UpdateProjectStatusDto } from '@/types/project';

const projectKeys = {
  all: ['projects'] as const,
  list: (filters: ProjectFilters) => ['projects', 'list', filters] as const,
  detail: (id: number) => ['projects', 'detail', id] as const,
  summary: (id: number) => ['projects', 'summary', id] as const,
};

const onMutationError = (error: unknown) => {
  const { message } = error as NormalizedError;
  toast.error('Error', { description: message });
};

const useProjects = (filters: ProjectFilters = {}) =>
  useQuery({
    queryKey: projectKeys.list(filters),
    queryFn: () => projectsApi.findAll(filters),
  });

const useProject = (id: number) =>
  useQuery({
    queryKey: projectKeys.detail(id),
    queryFn: () => projectsApi.findById(id),
  });

const useProjectSummary = (id: number) =>
  useQuery({
    queryKey: projectKeys.summary(id),
    queryFn: () => projectsApi.getSummary(id),
  });

const useCreateProject = () =>
  useMutation({
    mutationFn: (data: CreateProjectDto) => projectsApi.create(data),
    onError: onMutationError,
  });

const useUpdateProject = () =>
  useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateProjectDto }) =>
      projectsApi.update(id, data),
    onError: onMutationError,
  });

const useUpdateProjectStatus = () =>
  useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateProjectStatusDto }) =>
      projectsApi.updateStatus(id, data),
    onError: onMutationError,
  });

export { projectKeys, useProjects, useProject, useProjectSummary, useCreateProject, useUpdateProject, useUpdateProjectStatus };
