import type { FC } from 'react';
import { Plus, Clock } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { TableSkeleton } from '@/components/molecules/TableSkeleton';
import { EmptyTableRow } from '@/components/molecules/EmptyTableRow';
import { ASSIGNMENT_STATUS_LABEL, ASSIGNMENT_STATUS_VARIANT } from '@/constants/project-labels';
import type { Assignment } from '@/types/assignment';
import type { TeamMember } from '@/types/team-member';

interface AssignmentsSectionProps {
  assignments: Assignment[] | undefined;
  isLoading: boolean;
  teamMemberMap: Record<number, TeamMember>;
  onAddAssignment: () => void;
  onLogHours: (assignmentId: number) => void;
}

const AssignmentsSection: FC<AssignmentsSectionProps> = ({
  assignments, isLoading, teamMemberMap, onAddAssignment, onLogHours,
}) => (
  <div className="space-y-3">
    <div className="flex items-center justify-between">
      <h2 className="text-base font-semibold">Asignaciones</h2>
      <Button size="sm" onClick={onAddAssignment}>
        <Plus className="h-4 w-4 mr-1" />
        <span className="hidden sm:inline">Agregar asignación</span>
        <span className="sm:hidden">Agregar</span>
      </Button>
    </div>
    <Separator />
    <div className="overflow-x-auto"><Table>
      <TableHeader>
        <TableRow>
          <TableHead>Miembro</TableHead>
          <TableHead>Rol</TableHead>
          <TableHead>Estado</TableHead>
          <TableHead>Fecha inicio</TableHead>
          <TableHead>Horas</TableHead>
          <TableHead />
        </TableRow>
      </TableHeader>
      <TableBody>
        {isLoading ? (
          <TableSkeleton rows={3} cols={5} />
        ) : !assignments?.length ? (
          <EmptyTableRow colSpan={6} message="Sin asignaciones" />
        ) : assignments.map(a => (
          <TableRow key={a.id}>
            <TableCell>
              {teamMemberMap[a.team_member_id]?.full_name ?? '—'}
            </TableCell>
            <TableCell className="text-muted-foreground">{a.assignment_role}</TableCell>
            <TableCell>
              <Badge variant={ASSIGNMENT_STATUS_VARIANT[a.status]}>
                {ASSIGNMENT_STATUS_LABEL[a.status]}
              </Badge>
            </TableCell>
            <TableCell className="text-muted-foreground">{a.start_date}</TableCell>
            <TableCell className="text-muted-foreground">{Number(a.total_hours).toFixed(1)} h</TableCell>
            <TableCell className="text-right">
              <Tooltip>
                <TooltipTrigger asChild>
                  <span>
                    <Button
                      variant="ghost"
                      size="icon"
                      disabled={a.status !== 'ACTIVE'}
                      onClick={() => onLogHours(a.id)}
                    >
                      <Clock className="h-4 w-4" />
                    </Button>
                  </span>
                </TooltipTrigger>
                <TooltipContent>
                  {a.status === 'ACTIVE' ? 'Registrar horas' : 'La asignación no está activa'}
                </TooltipContent>
              </Tooltip>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table></div>
  </div>
);

export { AssignmentsSection };
