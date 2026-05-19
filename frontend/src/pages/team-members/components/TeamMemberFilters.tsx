import type { FC } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ROLE_LABEL, SENIORITY_LABEL, MEMBER_STATUS_LABEL } from '@/constants/team-member-labels';
import type { MemberRole, MemberSeniority, MemberStatus } from '@/types/team-member';

interface TeamMemberFiltersProps {
  role: MemberRole | undefined;
  seniority: MemberSeniority | undefined;
  status: MemberStatus | undefined;
  onRoleChange: (v: MemberRole | undefined) => void;
  onSeniorityChange: (v: MemberSeniority | undefined) => void;
  onStatusChange: (v: MemberStatus | undefined) => void;
}

const TeamMemberFilters: FC<TeamMemberFiltersProps> = ({
  role, seniority, status, onRoleChange, onSeniorityChange, onStatusChange,
}) => (
  <div className="grid grid-cols-2 sm:flex sm:flex-wrap gap-3">
    <Select value={role ?? 'ALL'} onValueChange={v => onRoleChange(v === 'ALL' ? undefined : v as MemberRole)}>
      <SelectTrigger className="w-full sm:w-36"><SelectValue placeholder="Rol" /></SelectTrigger>
      <SelectContent>
        <SelectItem value="ALL">Todos</SelectItem>
        {(Object.keys(ROLE_LABEL) as MemberRole[]).map(r => (
          <SelectItem key={r} value={r}>{ROLE_LABEL[r]}</SelectItem>
        ))}
      </SelectContent>
    </Select>

    <Select value={seniority ?? 'ALL'} onValueChange={v => onSeniorityChange(v === 'ALL' ? undefined : v as MemberSeniority)}>
      <SelectTrigger className="w-full sm:w-36"><SelectValue placeholder="Seniority" /></SelectTrigger>
      <SelectContent>
        <SelectItem value="ALL">Todos</SelectItem>
        {(Object.keys(SENIORITY_LABEL) as MemberSeniority[]).map(s => (
          <SelectItem key={s} value={s}>{SENIORITY_LABEL[s]}</SelectItem>
        ))}
      </SelectContent>
    </Select>

    <Select value={status ?? 'ALL'} onValueChange={v => onStatusChange(v === 'ALL' ? undefined : v as MemberStatus)}>
      <SelectTrigger className="w-full sm:w-36"><SelectValue placeholder="Estado" /></SelectTrigger>
      <SelectContent>
        <SelectItem value="ALL">Todos</SelectItem>
        {(Object.keys(MEMBER_STATUS_LABEL) as MemberStatus[]).map(s => (
          <SelectItem key={s} value={s}>{MEMBER_STATUS_LABEL[s]}</SelectItem>
        ))}
      </SelectContent>
    </Select>
  </div>
);

export { TeamMemberFilters };
