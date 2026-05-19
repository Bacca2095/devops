export type MemberRole = 'DEVELOPER' | 'ANALYST' | 'ARCHITECT' | 'QA' | 'DEVOPS';
export type MemberSeniority = 'JUNIOR' | 'MIDDLE' | 'SENIOR';
export type MemberStatus = 'ACTIVE' | 'INACTIVE';

export interface TeamMember {
  id: number;
  full_name: string;
  email: string;
  document_number: string;
  role: MemberRole;
  seniority: MemberSeniority;
  status: MemberStatus;
  created_at: string;
  updated_at: string;
}

export interface TeamMemberFilters {
  status?: MemberStatus;
  role?: MemberRole;
  seniority?: MemberSeniority;
  page?: number;
  page_size?: number;
}

export interface CreateTeamMemberDto {
  full_name: string;
  email: string;
  document_number: string;
  role: MemberRole;
  seniority: MemberSeniority;
  status?: MemberStatus;
}

export type UpdateTeamMemberDto = CreateTeamMemberDto;

export interface UpdateTeamMemberStatusDto {
  status: MemberStatus;
}
