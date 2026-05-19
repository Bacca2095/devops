import type { FC } from 'react';
import { Suspense } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import { useTheme } from 'next-themes';
import { Moon, Sun, FolderKanban, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { TooltipProvider } from '@/components/ui/tooltip';
import { Logo } from '@/components/atoms/logo';

const PageLoader: FC = () => (
  <div className="space-y-4">
    <Skeleton className="h-8 w-48" />
    <Skeleton className="h-4 w-full" />
    <Skeleton className="h-4 w-full" />
    <Skeleton className="h-4 w-3/4" />
  </div>
);

const NAV_LINKS = [
  { to: '/projects', label: 'Proyectos', icon: FolderKanban },
  { to: '/team-members', label: 'Equipo', icon: Users },
];

const ThemeToggle: FC = () => {
  const { resolvedTheme, setTheme } = useTheme();
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
    >
      {resolvedTheme === 'dark' ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
    </Button>
  );
};

const RootLayout: FC = () => (
  <TooltipProvider>
    <div className="min-h-screen bg-background">
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-14 items-center gap-4 px-6 max-w-7xl mx-auto">
          <Logo size={28} />
          <span className="font-semibold text-sm tracking-tight hidden sm:inline">Manager</span>
          <nav className="flex items-center gap-1 flex-1">
            {NAV_LINKS.map(({ to, label, icon: Icon }) => (
              <NavLink key={to} to={to}>
                {({ isActive }) => (
                  <Button variant={isActive ? 'secondary' : 'ghost'} size="sm" className="gap-1.5">
                    <Icon className="h-3.5 w-3.5" />
                    <span className="hidden sm:inline">{label}</span>
                  </Button>
                )}
              </NavLink>
            ))}
          </nav>
          <ThemeToggle />
        </div>
      </header>
      <main className="px-6 py-6 max-w-7xl mx-auto">
        <Suspense fallback={<PageLoader />}>
          <Outlet />
        </Suspense>
      </main>
    </div>
  </TooltipProvider>
);

export { RootLayout };
