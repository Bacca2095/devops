import type { FC } from 'react';
import { RouterProvider } from 'react-router-dom';
import { Toaster } from '@/components/ui/sonner';
import { router } from '@/router';

const App: FC = () => (
  <>
    <RouterProvider router={router} />
    <Toaster richColors position="top-right" />
  </>
);

export { App };
