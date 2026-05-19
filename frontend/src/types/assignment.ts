export type AssignmentStatus = 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export interface Assignment {
  id: number;
  project_id: number;
  team_member_id: number;
  assignment_role: string;
  start_date: string;
  end_date: string | null;
  status: AssignmentStatus;
  total_hours: number;
  created_at: string;
  updated_at: string;
}

export interface CreateAssignmentDto {
  team_member_id: number;
  assignment_role: string;
  start_date: string;
  end_date?: string;
}

export interface UpdateAssignmentStatusDto {
  status: AssignmentStatus;
}
