import type { FC } from 'react';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PROJECT_STATUS_LABEL, PROJECT_STATUS_VARIANT, PROJECT_PRIORITY_LABEL, PROJECT_PRIORITY_VARIANT } from '@/constants/project-labels';
import type { Project, ProjectStatus } from '@/types/project';

interface ProjectInfoCardProps {
  project: Project | undefined;
  isLoading: boolean;
  onStatusChange: (status: ProjectStatus) => void;
}

const ProjectInfoCard: FC<ProjectInfoCardProps> = ({ project, isLoading, onStatusChange }) => (
  <Card>
    <CardHeader className="flex flex-row items-center justify-between gap-3">
      <div className="min-w-0 space-y-2">
        {isLoading
          ? <Skeleton className="h-6 w-48" />
          : <CardTitle className="text-lg truncate">{project?.name}</CardTitle>}
        <div className="flex flex-wrap items-center gap-2">
          {project && (
            <>
              <Badge variant={PROJECT_STATUS_VARIANT[project.status]}>
                {PROJECT_STATUS_LABEL[project.status]}
              </Badge>
              <Badge variant={PROJECT_PRIORITY_VARIANT[project.priority]}>
                {PROJECT_PRIORITY_LABEL[project.priority]}
              </Badge>
              {project.start_date && (
                <span className="text-xs text-muted-foreground">{project.start_date}{project.end_date && ` → ${project.end_date}`}</span>
              )}
            </>
          )}
        </div>
      </div>
      <Select onValueChange={v => onStatusChange(v as ProjectStatus)}>
        <SelectTrigger className="w-36 shrink-0">
          <SelectValue placeholder="Cambiar estado" />
        </SelectTrigger>
        <SelectContent>
          {(Object.keys(PROJECT_STATUS_LABEL) as ProjectStatus[]).map(s => (
            <SelectItem key={s} value={s}>{PROJECT_STATUS_LABEL[s]}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </CardHeader>
  </Card>
);

export { ProjectInfoCard };
