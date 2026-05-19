import { useQuery, useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { assignmentsApi } from '@/api/assignments/assignments.api';
import type { NormalizedError } from '@/api/client';
import type { CreateAssignmentDto, UpdateAssignmentStatusDto } from '@/types/assignment';

const assignmentKeys = {
  all: ['assignments'],
  byProject: (projectId: number) => ['assignments', 'project', projectId],
};

const onMutationError = (error: unknown) => {
  const { message } = error as NormalizedError;
  toast.error('Error', { description: message });
};

const useAssignments = (projectId: number) =>
  useQuery({
    queryKey: assignmentKeys.byProject(projectId),
    queryFn: () => assignmentsApi.findByProject(projectId),
  });

const useCreateAssignment = () =>
  useMutation({
    mutationFn: ({ projectId, data }: { projectId: number; data: CreateAssignmentDto }) =>
      assignmentsApi.create(projectId, data),
    onError: onMutationError,
  });

const useUpdateAssignmentStatus = () =>
  useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateAssignmentStatusDto }) =>
      assignmentsApi.updateStatus(id, data),
    onError: onMutationError,
  });

export { assignmentKeys, useAssignments, useCreateAssignment, useUpdateAssignmentStatus };
