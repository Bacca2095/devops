import type { MemberRole, MemberSeniority, MemberStatus } from '@/types/team-member';

export const ROLE_LABEL: Record<MemberRole, string> = {
  DEVELOPER: 'Desarrollador', ANALYST: 'Analista', ARCHITECT: 'Arquitecto', QA: 'QA', DEVOPS: 'DevOps',
};

export const SENIORITY_LABEL: Record<MemberSeniority, string> = {
  JUNIOR: 'Junior', MIDDLE: 'Middle', SENIOR: 'Senior',
};

export const MEMBER_STATUS_LABEL: Record<MemberStatus, string> = {
  ACTIVE: 'Activo', INACTIVE: 'Inactivo',
};

export const MEMBER_STATUS_VARIANT: Record<MemberStatus, 'default' | 'secondary' | 'outline' | 'destructive'> = {
  ACTIVE: 'default', INACTIVE: 'secondary',
};
