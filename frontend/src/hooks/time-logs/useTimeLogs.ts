import { useQuery, useMutation } from '@tanstack/react-query';
import { toast } from 'sonner';
import { timeLogsApi } from '@/api/time-logs/time-logs.api';
import type { NormalizedError } from '@/api/client';
import type { CreateTimeLogDto } from '@/types/time-log';

const timeLogKeys = {
  all: ['time-logs'] as const,
  byAssignment: (assignmentId: number) => ['time-logs', 'assignment', assignmentId] as const,
};

const onMutationError = (error: unknown) => {
  const { message } = error as NormalizedError;
  toast.error('Error', { description: message });
};

const useTimeLogs = (assignmentId: number) =>
  useQuery({
    queryKey: timeLogKeys.byAssignment(assignmentId),
    queryFn: () => timeLogsApi.findByAssignment(assignmentId),
  });

const useCreateTimeLog = () =>
  useMutation({
    mutationFn: ({ assignmentId, data }: { assignmentId: number; data: CreateTimeLogDto }) =>
      timeLogsApi.create(assignmentId, data),
    onError: onMutationError,
  });

export { timeLogKeys, useTimeLogs, useCreateTimeLog };
