import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ProjectStatus, ProjectPriority } from '@/types/project';

interface ProjectStore {
  status: ProjectStatus | undefined;
  priority: ProjectPriority | undefined;
  name: string;
  page: number;
  setStatus: (status: ProjectStatus | undefined) => void;
  setPriority: (priority: ProjectPriority | undefined) => void;
  setName: (name: string) => void;
  setPage: (page: number) => void;
}

const useProjectStore = create<ProjectStore>()(
  persist(
    (set) => ({
      status: undefined,
      priority: undefined,
      name: '',
      page: 1,
      setStatus: (status) => set({ status, page: 1 }),
      setPriority: (priority) => set({ priority, page: 1 }),
      setName: (name) => set({ name, page: 1 }),
      setPage: (page) => set({ page }),
    }),
    { name: 'project-filters' },
  ),
);

export { useProjectStore };
