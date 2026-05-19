import type { FC } from 'react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { Plus } from 'lucide-react';
import { useTeamMemberStore } from '@/store/useTeamMemberStore';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { useTeamMembers, useCreateTeamMember, useUpdateTeamMember, teamMemberKeys } from '@/hooks/team-members/useTeamMembers';
import { TeamMemberFilters } from './components/TeamMemberFilters';
import { TeamMemberTable } from './components/TeamMemberTable';
import { CreateTeamMemberDialog } from './components/CreateTeamMemberDialog';
import { EditTeamMemberDialog } from './components/EditTeamMemberDialog';
import { Pagination } from '@/components/molecules/Pagination';
import type { CreateTeamMemberDto, UpdateTeamMemberDto, TeamMember } from '@/types/team-member';

const TeamMemberListPage: FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { role: filterRole, seniority: filterSeniority, status: filterStatus, page, setRole, setSeniority, setStatus, setPage } = useTeamMemberStore();
  const [createOpen, setCreateOpen] = useState(false);
  const [editingMember, setEditingMember] = useState<TeamMember | null>(null);

  const { data, isLoading } = useTeamMembers({ role: filterRole, seniority: filterSeniority, status: filterStatus, page });
  const create = useCreateTeamMember();
  const update = useUpdateTeamMember();

  const handleCreate = (form: CreateTeamMemberDto) => {
    create.mutate(form, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: teamMemberKeys.all });
        setCreateOpen(false);
      },
    });
  };

  const handleEdit = (form: UpdateTeamMemberDto) => {
    if (!editingMember) return;
    update.mutate({ id: editingMember.id, data: form }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: teamMemberKeys.all });
        setEditingMember(null);
      },
    });
  };

  return (
    <div className="space-y-5">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Equipo</h1>
        <Button onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4 mr-1" />
          <span className="hidden sm:inline">Nuevo miembro</span>
          <span className="sm:hidden">Nuevo</span>
        </Button>
      </div>

      <TeamMemberFilters
        role={filterRole}
        seniority={filterSeniority}
        status={filterStatus}
        onRoleChange={setRole}
        onSeniorityChange={setSeniority}
        onStatusChange={setStatus}
      />

      <Card className="overflow-x-auto p-0">
        <TeamMemberTable
          data={data?.items}
          isLoading={isLoading}
          onView={(id) => navigate(`/team-members/${id}`)}
          onEdit={setEditingMember}
        />
        <Pagination
          page={data?.page ?? page}
          pages={data?.pages ?? 1}
          total={data?.total ?? 0}
          onPageChange={setPage}
        />
      </Card>

      <CreateTeamMemberDialog
        open={createOpen}
        onOpenChange={setCreateOpen}
        onSubmit={handleCreate}
        isPending={create.isPending}
      />

      {editingMember && (
        <EditTeamMemberDialog
          key={editingMember.id}
          open={!!editingMember}
          onOpenChange={(open) => { if (!open) setEditingMember(null); }}
          onSubmit={handleEdit}
          isPending={update.isPending}
          member={editingMember}
        />
      )}
    </div>
  );
};

export { TeamMemberListPage };
