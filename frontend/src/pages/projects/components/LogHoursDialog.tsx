import type { FC } from 'react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { FormField } from '@/components/molecules/FormField';
import type { CreateTimeLogDto } from '@/types/time-log';

const EMPTY: CreateTimeLogDto = { logged_date: '', hours: 0 };

interface LogHoursDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (form: CreateTimeLogDto) => void;
  isPending: boolean;
}

const LogHoursDialog: FC<LogHoursDialogProps> = ({ open, onOpenChange, onSubmit, isPending }) => {
  const [form, setForm] = useState<CreateTimeLogDto>(EMPTY);

  const handleSubmit = () => {
    if (!form.logged_date || !form.hours) return;
    onSubmit(form);
  };

  const handleOpenChange = (value: boolean) => {
    if (!value) setForm(EMPTY);
    onOpenChange(value);
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Registrar horas</DialogTitle>
        </DialogHeader>
        <div className="space-y-3">
          <FormField label="Fecha *">
            <Input
              type="date"
              value={form.logged_date}
              onChange={e => setForm(f => ({ ...f, logged_date: e.target.value }))}
            />
          </FormField>
          <FormField label="Horas * (0.5 – 24)">
            <Input
              type="number"
              min={0.5}
              max={24}
              step={0.5}
              value={form.hours || ''}
              onChange={e => setForm(f => ({ ...f, hours: Number(e.target.value) }))}
            />
          </FormField>
          <FormField label="Descripción">
            <Input
              value={form.description ?? ''}
              onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
              placeholder="Opcional"
            />
          </FormField>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => handleOpenChange(false)}>Cancelar</Button>
          <Button onClick={handleSubmit} disabled={isPending}>
            {isPending ? 'Guardando...' : 'Registrar'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export { LogHoursDialog };
