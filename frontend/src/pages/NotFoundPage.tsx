import type { FC } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const NotFoundPage: FC = () => {
  const navigate = useNavigate();
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
      <h1 className="text-5xl font-bold">404</h1>
      <p className="text-muted-foreground">Página no encontrada</p>
      <Button onClick={() => navigate('/projects')}>Ir a proyectos</Button>
    </div>
  );
};

export { NotFoundPage };
