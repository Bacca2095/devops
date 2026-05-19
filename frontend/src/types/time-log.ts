export interface TimeLog {
  id: number;
  assignment_id: number;
  logged_date: string;
  hours: number;
  description: string | null;
  created_at: string;
}

export interface CreateTimeLogDto {
  logged_date: string;
  hours: number;
  description?: string;
}
