import type { FC } from 'react';
import { Clock, Users, CalendarDays } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import type { ProjectSummary } from '@/types/project';

interface ProjectSummaryCardsProps {
  summary: ProjectSummary | undefined;
  isLoading: boolean;
}

const STATS = [
  { key: 'total_logged_hours' as const, icon: Clock, label: 'Total horas' },
  { key: 'active_assignments' as const, icon: Users, label: 'Asignaciones activas' },
  { key: 'last_activity_date' as const, icon: CalendarDays, label: 'Última actividad' },
];

const ProjectSummaryCards: FC<ProjectSummaryCardsProps> = ({ summary, isLoading }) => (
  <div className="grid grid-cols-3 gap-3">
    {STATS.map(({ key, icon: Icon, label }) => (
      <Card key={label}>
        <CardContent className="pt-3 pb-3 sm:pt-5 sm:pb-5">
          <div className="flex items-center gap-1.5 text-xs text-muted-foreground mb-1.5">
            <Icon className="h-3.5 w-3.5 shrink-0" />
            <span className="truncate">{label}</span>
          </div>
          {isLoading
            ? <Skeleton className="h-6 w-16" />
            : <p className="text-xl font-semibold truncate">{summary?.[key] ?? '—'}</p>}
        </CardContent>
      </Card>
    ))}
  </div>
);

export { ProjectSummaryCards };
