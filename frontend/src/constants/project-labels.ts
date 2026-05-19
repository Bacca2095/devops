import type { ProjectStatus, ProjectPriority } from '@/types/project';
import type { AssignmentStatus } from '@/types/assignment';

export const PROJECT_STATUS_LABEL: Record<ProjectStatus, string> = {
  ACTIVE: 'Activo', ON_HOLD: 'En espera', COMPLETED: 'Completado', CANCELLED: 'Cancelado',
};

export const PROJECT_PRIORITY_LABEL: Record<ProjectPriority, string> = {
  LOW: 'Baja', MEDIUM: 'Media', HIGH: 'Alta', CRITICAL: 'Crítica',
};

export const PROJECT_STATUS_VARIANT: Record<ProjectStatus, 'default' | 'secondary' | 'outline' | 'destructive'> = {
  ACTIVE: 'default', ON_HOLD: 'secondary', COMPLETED: 'outline', CANCELLED: 'destructive',
};

export const PROJECT_PRIORITY_VARIANT: Record<ProjectPriority, 'default' | 'secondary' | 'outline' | 'destructive'> = {
  LOW: 'outline', MEDIUM: 'secondary', HIGH: 'default', CRITICAL: 'destructive',
};

export const ASSIGNMENT_STATUS_LABEL: Record<AssignmentStatus, string> = {
  ACTIVE: 'Activa', COMPLETED: 'Completada', CANCELLED: 'Cancelada',
};

export const ASSIGNMENT_STATUS_VARIANT: Record<AssignmentStatus, 'default' | 'secondary' | 'outline' | 'destructive'> = {
  ACTIVE: 'default', COMPLETED: 'secondary', CANCELLED: 'destructive',
};
