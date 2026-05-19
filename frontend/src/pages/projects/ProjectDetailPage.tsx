import type { FC } from 'react';
import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, Pencil } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { useProject, useProjectSummary, useUpdateProject, useUpdateProjectStatus, projectKeys } from '@/hooks/projects/useProjects';
import { useAssignments, useCreateAssignment, assignmentKeys } from '@/hooks/assignments/useAssignments';
import { useCreateTimeLog, timeLogKeys } from '@/hooks/time-logs/useTimeLogs';
import { useTeamMembers } from '@/hooks/team-members/useTeamMembers';
import { ProjectInfoCard } from './components/ProjectInfoCard';
import { ProjectSummaryCards } from './components/ProjectSummaryCards';
import { AssignmentsSection } from './components/AssignmentsSection';
import { AddAssignmentDialog } from './components/AddAssignmentDialog';
import { EditProjectDialog } from './components/EditProjectDialog';
import { LogHoursDialog } from './components/LogHoursDialog';
import type { ProjectStatus, UpdateProjectDto } from '@/types/project';
import type { CreateAssignmentDto } from '@/types/assignment';
import type { CreateTimeLogDto } from '@/types/time-log';

const ProjectDetailPage: FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const projectId = Number(id);

  const { data: project, isLoading: loadingProject } = useProject(projectId);
  const { data: summary, isLoading: loadingSummary } = useProjectSummary(projectId);
  const { data: assignments, isLoading: loadingAssignments } = useAssignments(projectId);
  const { data: teamMembers } = useTeamMembers();

  const updateProject = useUpdateProject();
  const updateStatus = useUpdateProjectStatus();
  const createAssignment = useCreateAssignment();
  const createTimeLog = useCreateTimeLog();

  const [editOpen, setEditOpen] = useState(false);
  const [assignmentOpen, setAssignmentOpen] = useState(false);
  const [timelogOpen, setTimelogOpen] = useState(false);
  const [selectedAssignmentId, setSelectedAssignmentId] = useState<number | null>(null);

  const teamMemberMap = Object.fromEntries(
    (teamMembers?.items ?? []).map(m => [m.id, m]),
  );

  const handleEdit = (form: UpdateProjectDto) => {
    updateProject.mutate({ id: projectId, data: form }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: projectKeys.detail(projectId) });
        queryClient.invalidateQueries({ queryKey: projectKeys.list({}) });
        setEditOpen(false);
      },
    });
  };

  const handleStatusChange = (status: ProjectStatus) => {
    updateStatus.mutate({ id: projectId, data: { status } }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: projectKeys.detail(projectId) });
        queryClient.invalidateQueries({ queryKey: projectKeys.summary(projectId) });
      },
    });
  };

  const handleAddAssignment = (form: CreateAssignmentDto) => {
    createAssignment.mutate({ projectId, data: form }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: assignmentKeys.byProject(projectId) });
        queryClient.invalidateQueries({ queryKey: projectKeys.summary(projectId) });
        setAssignmentOpen(false);
      },
    });
  };

  const handleLogHours = (form: CreateTimeLogDto) => {
    if (!selectedAssignmentId) return;
    createTimeLog.mutate({ assignmentId: selectedAssignmentId, data: form }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: timeLogKeys.byAssignment(selectedAssignmentId) });
        queryClient.invalidateQueries({ queryKey: projectKeys.summary(projectId) });
        queryClient.invalidateQueries({ queryKey: assignmentKeys.byProject(projectId) });
        setTimelogOpen(false);
        setSelectedAssignmentId(null);
      },
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" size="sm" onClick={() => navigate('/projects')}>
          <ArrowLeft className="h-4 w-4 mr-1" /> Volver
        </Button>
        {project && (
          <Button variant="outline" size="sm" onClick={() => setEditOpen(true)}>
            <Pencil className="h-4 w-4 mr-1" /> Editar
          </Button>
        )}
      </div>

      <ProjectInfoCard
        project={project}
        isLoading={loadingProject}
        onStatusChange={handleStatusChange}
      />

      <ProjectSummaryCards summary={summary} isLoading={loadingSummary} />

      <Card className="p-6">
        <AssignmentsSection
          assignments={assignments?.items}
          isLoading={loadingAssignments}
          teamMemberMap={teamMemberMap}
          onAddAssignment={() => setAssignmentOpen(true)}
          onLogHours={(assignmentId) => {
            setSelectedAssignmentId(assignmentId);
            setTimelogOpen(true);
          }}
        />
      </Card>

      {project && (
        <EditProjectDialog
          key={editOpen ? project.id : 'closed'}
          open={editOpen}
          onOpenChange={setEditOpen}
          onSubmit={handleEdit}
          isPending={updateProject.isPending}
          project={project}
        />
      )}

      <AddAssignmentDialog
        open={assignmentOpen}
        onOpenChange={setAssignmentOpen}
        teamMembers={teamMembers?.items ?? []}
        onSubmit={handleAddAssignment}
        isPending={createAssignment.isPending}
      />

      <LogHoursDialog
        open={timelogOpen}
        onOpenChange={setTimelogOpen}
        onSubmit={handleLogHours}
        isPending={createTimeLog.isPending}
      />
    </div>
  );
};

export { ProjectDetailPage };
