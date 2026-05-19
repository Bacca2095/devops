import type { FC } from 'react';
import { Eye, Pencil } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { TableSkeleton } from '@/components/molecules/TableSkeleton';
import { EmptyTableRow } from '@/components/molecules/EmptyTableRow';
import {
  PROJECT_STATUS_LABEL,
  PROJECT_PRIORITY_LABEL,
  PROJECT_STATUS_VARIANT,
  PROJECT_PRIORITY_VARIANT,
} from '@/constants/project-labels';
import type { Project } from '@/types/project';

interface ProjectTableProps {
  data: Project[] | undefined;
  isLoading: boolean;
  onView: (id: number) => void;
  onEdit: (project: Project) => void;
}

const ProjectTable: FC<ProjectTableProps> = ({ data, isLoading, onView, onEdit }) => (
  <Table>
    <TableHeader>
      <TableRow>
        <TableHead>Nombre</TableHead>
        <TableHead>Estado</TableHead>
        <TableHead>Prioridad</TableHead>
        <TableHead>Fecha inicio</TableHead>
        <TableHead className="w-px whitespace-nowrap" />
      </TableRow>
    </TableHeader>
    <TableBody>
      {isLoading ? (
        <TableSkeleton rows={5} cols={5} />
      ) : !data?.length ? (
        <EmptyTableRow colSpan={5} message="No hay proyectos" />
      ) : data.map(project => (
        <TableRow key={project.id} className="cursor-pointer hover:bg-muted/50">
          <TableCell>{project.name}</TableCell>
          <TableCell>
            <Badge variant={PROJECT_STATUS_VARIANT[project.status]}>
              {PROJECT_STATUS_LABEL[project.status]}
            </Badge>
          </TableCell>
          <TableCell>
            <Badge variant={PROJECT_PRIORITY_VARIANT[project.priority]}>
              {PROJECT_PRIORITY_LABEL[project.priority]}
            </Badge>
          </TableCell>
          <TableCell className="text-muted-foreground">{project.start_date}</TableCell>
          <TableCell className="text-right">
            <div className="flex items-center justify-end gap-1">
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" className="text-blue-500 hover:text-blue-600" onClick={() => onEdit(project)}>
                    <Pencil className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Editar</TooltipContent>
              </Tooltip>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button variant="ghost" size="icon" className="text-green-500 hover:text-green-600" onClick={() => onView(project.id)}>
                    <Eye className="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Ver proyecto</TooltipContent>
              </Tooltip>
            </div>
          </TableCell>
        </TableRow>
      ))}
    </TableBody>
  </Table>
);

export { ProjectTable };
