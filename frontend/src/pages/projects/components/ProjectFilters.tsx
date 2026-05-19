import type { FC } from 'react';
import { Search } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PROJECT_STATUS_LABEL, PROJECT_PRIORITY_LABEL } from '@/constants/project-labels';
import type { ProjectStatus, ProjectPriority } from '@/types/project';

interface ProjectFiltersProps {
  status: ProjectStatus | undefined;
  priority: ProjectPriority | undefined;
  name: string;
  onStatusChange: (v: ProjectStatus | undefined) => void;
  onPriorityChange: (v: ProjectPriority | undefined) => void;
  onNameChange: (v: string) => void;
}

const ProjectFilters: FC<ProjectFiltersProps> = ({
  status, priority, name, onStatusChange, onPriorityChange, onNameChange,
}) => (
  <div className="flex flex-col sm:flex-row gap-3">
    <div className="relative flex-1">
      <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
      <Input
        className="pl-8"
        placeholder="Buscar proyecto..."
        value={name}
        onChange={e => onNameChange(e.target.value)}
      />
    </div>
    <div className="grid grid-cols-2 sm:flex gap-3">
      <Select value={status ?? 'ALL'} onValueChange={v => onStatusChange(v === 'ALL' ? undefined : v as ProjectStatus)}>
        <SelectTrigger className="w-full sm:w-36"><SelectValue placeholder="Estado" /></SelectTrigger>
        <SelectContent>
          <SelectItem value="ALL">Todos</SelectItem>
          {(Object.keys(PROJECT_STATUS_LABEL) as ProjectStatus[]).map(s => (
            <SelectItem key={s} value={s}>{PROJECT_STATUS_LABEL[s]}</SelectItem>
          ))}
        </SelectContent>
      </Select>

      <Select value={priority ?? 'ALL'} onValueChange={v => onPriorityChange(v === 'ALL' ? undefined : v as ProjectPriority)}>
        <SelectTrigger className="w-full sm:w-36"><SelectValue placeholder="Prioridad" /></SelectTrigger>
        <SelectContent>
          <SelectItem value="ALL">Todas</SelectItem>
          {(Object.keys(PROJECT_PRIORITY_LABEL) as ProjectPriority[]).map(p => (
            <SelectItem key={p} value={p}>{PROJECT_PRIORITY_LABEL[p]}</SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  </div>
);

export { ProjectFilters };
