import type { FC } from 'react';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Separator } from '@/components/ui/separator';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { ROLE_LABEL, SENIORITY_LABEL, MEMBER_STATUS_LABEL, MEMBER_STATUS_VARIANT } from '@/constants/team-member-labels';
import type { TeamMember, MemberStatus } from '@/types/team-member';

function getInitials(name: string): string {
  return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase();
}

interface TeamMemberInfoCardProps {
  member: TeamMember | undefined;
  isLoading: boolean;
  onStatusChange: (status: MemberStatus) => void;
}

const TeamMemberInfoCard: FC<TeamMemberInfoCardProps> = ({ member, isLoading, onStatusChange }) => (
  <Card>
    <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
      <div className="flex items-center gap-3">
        <Avatar className="h-12 w-12">
          <AvatarFallback className="text-sm font-semibold">
            {member ? getInitials(member.full_name) : '??'}
          </AvatarFallback>
        </Avatar>
        <div>
          {isLoading
            ? <Skeleton className="h-6 w-48" />
            : <CardTitle className="text-xl">{member?.full_name}</CardTitle>}
          {member && (
            <p className="text-sm text-muted-foreground mt-0.5">{member.email}</p>
          )}
        </div>
      </div>
      <div className="flex items-center gap-2 shrink-0">
        {member && (
          <Badge variant={MEMBER_STATUS_VARIANT[member.status]}>
            {MEMBER_STATUS_LABEL[member.status]}
          </Badge>
        )}
        <Select onValueChange={v => onStatusChange(v as MemberStatus)}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder="Cambiar estado" />
          </SelectTrigger>
          <SelectContent>
            {(Object.keys(MEMBER_STATUS_LABEL) as MemberStatus[]).map(s => (
              <SelectItem key={s} value={s}>{MEMBER_STATUS_LABEL[s]}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </CardHeader>
    <Separator />
    <CardContent className="pt-4 grid grid-cols-1 sm:grid-cols-2 gap-6">
      <div>
        <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Número de documento</p>
        {isLoading
          ? <Skeleton className="h-4 w-32" />
          : <p className="font-medium">{member?.document_number}</p>}
      </div>
      <div>
        <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Rol</p>
        {isLoading
          ? <Skeleton className="h-5 w-24" />
          : <Badge variant="outline">{member && ROLE_LABEL[member.role]}</Badge>}
      </div>
      <div>
        <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">Seniority</p>
        {isLoading
          ? <Skeleton className="h-4 w-16" />
          : <p className="font-medium">{member && SENIORITY_LABEL[member.seniority]}</p>}
      </div>
    </CardContent>
  </Card>
);

export { TeamMemberInfoCard };
