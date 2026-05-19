import type { FC } from 'react';
import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { ArrowLeft, Pencil } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useTeamMember, useUpdateTeamMember, useUpdateTeamMemberStatus, teamMemberKeys } from '@/hooks/team-members/useTeamMembers';
import { TeamMemberInfoCard } from './components/TeamMemberInfoCard';
import { EditTeamMemberDialog } from './components/EditTeamMemberDialog';
import type { MemberStatus, UpdateTeamMemberDto } from '@/types/team-member';

const TeamMemberDetailPage: FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const memberId = Number(id);

  const { data: member, isLoading } = useTeamMember(memberId);
  const updateMember = useUpdateTeamMember();
  const updateStatus = useUpdateTeamMemberStatus();

  const [editOpen, setEditOpen] = useState(false);

  const handleEdit = (form: UpdateTeamMemberDto) => {
    updateMember.mutate({ id: memberId, data: form }, {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: teamMemberKeys.detail(memberId) });
        queryClient.invalidateQueries({ queryKey: teamMemberKeys.all });
        setEditOpen(false);
      },
    });
  };

  const handleStatusChange = (status: MemberStatus) => {
    updateStatus.mutate({ id: memberId, data: { status } }, {
      onSuccess: () => queryClient.invalidateQueries({ queryKey: teamMemberKeys.detail(memberId) }),
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" size="sm" onClick={() => navigate('/team-members')}>
          <ArrowLeft className="h-4 w-4 mr-1" /> Volver
        </Button>
        {member && (
          <Button variant="outline" size="sm" onClick={() => setEditOpen(true)}>
            <Pencil className="h-4 w-4 mr-1" /> Editar
          </Button>
        )}
      </div>

      <TeamMemberInfoCard
        member={member}
        isLoading={isLoading}
        onStatusChange={handleStatusChange}
      />

      {member && (
        <EditTeamMemberDialog
          key={editOpen ? member.id : 'closed'}
          open={editOpen}
          onOpenChange={setEditOpen}
          onSubmit={handleEdit}
          isPending={updateMember.isPending}
          member={member}
        />
      )}
    </div>
  );
};

export { TeamMemberDetailPage };
