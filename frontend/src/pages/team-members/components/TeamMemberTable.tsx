import type { FC } from 'react';
import { Eye, Pencil } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { TableSkeleton } from '@/components/molecules/TableSkeleton';
import { EmptyTableRow } from '@/components/molecules/EmptyTableRow';
import { ROLE_LABEL, SENIORITY_LABEL, MEMBER_STATUS_LABEL, MEMBER_STATUS_VARIANT } from '@/constants/team-member-labels';
import type { TeamMember } from '@/types/team-member';

interface TeamMemberTableProps {
  data: TeamMember[] | undefined;
  isLoading: boolean;
  onView: (id: number) => void;
  onEdit: (member: TeamMember) => void;
}

const TeamMemberTable: FC<TeamMemberTableProps> = ({ data, isLoading, onView, onEdit }) => (
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead>Nombre</TableHead>
        <TableHead>Rol</TableHead>
        <TableHead>Seniority</TableHead>
        <TableHead>Estado</TableHead>
        <TableHead className="w-px whitespace-nowrap" />
      </TableRow>
    </TableHeader>
    <TableBody>
      {isLoading ? (
        <TableSkeleton rows={5} cols={5} />
      ) : !data?.length ? (
        <EmptyTableRow colSpan={5} message="No hay miembros del equipo" />
      ) : data.map(member => (
        <TableRow key={member.id} className="cursor-pointer hover:bg-muted/50">
          <TableCell>{member.full_name}</TableCell>
          <TableCell>
            <Badge variant="outline">{ROLE_LABEL[member.role]}</Badge>
          </TableCell>
          <TableCell className="text-muted-foreground">{SENIORITY_LABEL[member.seniority]}</TableCell>
          <TableCell>
            <Badge variant={MEMBER_STATUS_VARIANT[member.status]}>
              {MEMBER_STATUS_LABEL[member.status]}
            </Badge>
          </TableCell>
          <TableCell className="text-right">
            <div className="flex items-center justify-end gap-1">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" className="text-blue-500 hover:text-blue-600" onClick={() => onEdit(member)}>
                    <Pencil className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Editar</TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" className="text-green-500 hover:text-green-600" onClick={() => onView(member.id)}>
                    <Eye className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Ver miembro</TooltipContent>
              </Tooltip>
            </div>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);

export { TeamMemberTable };
