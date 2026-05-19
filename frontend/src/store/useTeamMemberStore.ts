import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { MemberRole, MemberSeniority, MemberStatus } from '@/types/team-member';

interface TeamMemberStore {
  role: MemberRole | undefined;
  seniority: MemberSeniority | undefined;
  status: MemberStatus | undefined;
  page: number;
  setRole: (role: MemberRole | undefined) => void;
  setSeniority: (seniority: MemberSeniority | undefined) => void;
  setStatus: (status: MemberStatus | undefined) => void;
  setPage: (page: number) => void;
}

const useTeamMemberStore = create<TeamMemberStore>()(
  persist(
    (set) => ({
      role: undefined,
      seniority: undefined,
      status: undefined,
      page: 1,
      setRole: (role) => set({ role, page: 1 }),
      setSeniority: (seniority) => set({ seniority, page: 1 }),
      setStatus: (status) => set({ status, page: 1 }),
      setPage: (page) => set({ page }),
    }),
    { name: 'team-member-filters' },
  ),
);

export { useTeamMemberStore };
