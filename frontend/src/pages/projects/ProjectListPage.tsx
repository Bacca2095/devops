import type { FC } from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import { useProjectStore } from '@/store/useProjectStore';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { useProjects, useCreateProject, useUpdateProject, projectKeys } from '@/hooks/projects/useProjects';
import { ProjectFilters } from './components/ProjectFilters';
import { ProjectTable } from './components/ProjectTable';
import { CreateProjectDialog } from './components/CreateProjectDialog';
import { EditProjectDialog } from './components/EditProjectDialog';
import { Pagination } from '@/components/molecules/Pagination';
import type { CreateProjectDto, UpdateProjectDto, Project } from '@/types/project';

const ProjectListPage: FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { status: filterStatus, priority: filterPriority, name: filterName, page, setStatus, setPriority, setName, setPage } = useProjectStore();
  const [createOpen, setCreateOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);

  const { data, isLoading } = useProjects({ status: filterStatus, priority: filterPriority, name: filterName || undefined, page });
  const create = useCreateProject();
  const update = useUpdateProject();

  const handleCreate = (form: CreateProjectDto) => {
    create.mutate(form, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: projectKeys.all });
        setCreateOpen(false);
      },
    });
  };

  const handleEdit = (form: UpdateProjectDto) => {
    if (!editingProject) return;
    update.mutate({ id: editingProject.id, data: form }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: projectKeys.all });
        setEditingProject(null);
      },
    });
  };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Proyectos</h1>
        <Button onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4 mr-1" />
          <span className="hidden sm:inline">Nuevo proyecto</span>
          <span className="sm:hidden">Nuevo</span>
        </Button>
      </div>

      <ProjectFilters
        status={filterStatus}
        priority={filterPriority}
        name={filterName}
        onStatusChange={setStatus}
        onPriorityChange={setPriority}
        onNameChange={setName}
      />

      <Card className="overflow-x-auto p-0">
        <ProjectTable
          data={data?.items}
          isLoading={isLoading}
          onView={(id) => navigate(`/projects/${id}`)}
          onEdit={setEditingProject}
        />
        <Pagination
          page={data?.page ?? page}
          pages={data?.pages ?? 1}
          total={data?.total ?? 0}
          onPageChange={setPage}
        />
      </Card>

      <CreateProjectDialog
        open={createOpen}
        onOpenChange={setCreateOpen}
        onSubmit={handleCreate}
        isPending={create.isPending}
      />

      {editingProject && (
        <EditProjectDialog
          key={editingProject.id}
          open={!!editingProject}
          onOpenChange={(open) => { if (!open) setEditingProject(null); }}
          onSubmit={handleEdit}
          isPending={update.isPending}
          project={editingProject}
        />
      )}
    </div>
  );
};

export { ProjectListPage };
