import type { FC } from 'react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { FormField } from '@/components/molecules/FormField';
import { PROJECT_STATUS_LABEL, PROJECT_PRIORITY_LABEL } from '@/constants/project-labels';
import type { ProjectStatus, ProjectPriority, CreateProjectDto } from '@/types/project';

const EMPTY_FORM: CreateProjectDto = { name: '', priority: 'MEDIUM', start_date: '', status: 'ACTIVE' };

interface CreateProjectDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (form: CreateProjectDto) => void;
  isPending: boolean;
}

const CreateProjectDialog: FC<CreateProjectDialogProps> = ({ open, onOpenChange, onSubmit, isPending }) => {
  const [form, setForm] = useState<CreateProjectDto>(EMPTY_FORM);

  const handleSubmit = () => {
    if (!form.name || !form.start_date) return;
    onSubmit(form);
  };

  const handleOpenChange = (value: boolean) => {
    if (!value) setForm(EMPTY_FORM);
    onOpenChange(value);
  };

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nuevo proyecto</DialogTitle>
        </DialogHeader>
        <div className="space-y-3">
          <FormField label="Nombre *">
            <Input value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} />
          </FormField>
          <FormField label="Descripción">
            <Textarea
              value={form.description ?? ''}
              onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
              className="resize-none"
              rows={3}
            />
          </FormField>
          <div className="grid grid-cols-2 gap-3">
            <FormField label="Estado">
              <Select value={form.status} onValueChange={v => setForm(f => ({ ...f, status: v as ProjectStatus }))}>
                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {(Object.keys(PROJECT_STATUS_LABEL) as ProjectStatus[]).map(s => (
                    <SelectItem key={s} value={s}>{PROJECT_STATUS_LABEL[s]}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </FormField>
            <FormField label="Prioridad">
              <Select value={form.priority} onValueChange={v => setForm(f => ({ ...f, priority: v as ProjectPriority }))}>
                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {(Object.keys(PROJECT_PRIORITY_LABEL) as ProjectPriority[]).map(p => (
                    <SelectItem key={p} value={p}>{PROJECT_PRIORITY_LABEL[p]}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </FormField>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <FormField label="Fecha inicio *">
              <Input type="date" value={form.start_date} onChange={e => setForm(f => ({ ...f, start_date: e.target.value }))} />
            </FormField>
            <FormField label="Fecha fin">
              <Input type="date" value={form.end_date ?? ''} onChange={e => setForm(f => ({ ...f, end_date: e.target.value }))} />
            </FormField>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => handleOpenChange(false)}>Cancelar</Button>
          <Button onClick={handleSubmit} disabled={isPending}>
            {isPending ? 'Guardando...' : 'Crear'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export { CreateProjectDialog };
