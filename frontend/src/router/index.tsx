import { lazy } from 'react';
import { createBrowserRouter, Navigate } from 'react-router-dom';
import { RootLayout } from '@/layouts/RootLayout';

const ProjectListPage = lazy(() =>
  import('@/pages/projects/ProjectListPage').then(m => ({ default: m.ProjectListPage })),
);
const ProjectDetailPage = lazy(() =>
  import('@/pages/projects/ProjectDetailPage').then(m => ({ default: m.ProjectDetailPage })),
);
const TeamMemberListPage = lazy(() =>
  import('@/pages/team-members/TeamMemberListPage').then(m => ({ default: m.TeamMemberListPage })),
);
const TeamMemberDetailPage = lazy(() =>
  import('@/pages/team-members/TeamMemberDetailPage').then(m => ({ default: m.TeamMemberDetailPage })),
);
const NotFoundPage = lazy(() =>
  import('@/pages/NotFoundPage').then(m => ({ default: m.NotFoundPage })),
);

export const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      { index: true, element: <Navigate to="/projects" replace /> },
      { path: 'projects', element: <ProjectListPage /> },
      { path: 'projects/:id', element: <ProjectDetailPage /> },
      { path: 'team-members', element: <TeamMemberListPage /> },
      { path: 'team-members/:id', element: <TeamMemberDetailPage /> },
    ],
  },
  { path: '*', element: <NotFoundPage /> },
]);
