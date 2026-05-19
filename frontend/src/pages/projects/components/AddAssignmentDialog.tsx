import type { FC } from 'react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { FormField } from '@/components/molecules/FormField';
import type { TeamMember } from '@/types/team-member';
import type { CreateAssignmentDto } from '@/types/assignment';

const EMPTY: CreateAssignmentDto = { team_member_id: 0, assignment_role: '', start_date: '' };

interface AddAssignmentDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  teamMembers: TeamMember[];
  onSubmit: (form: CreateAssignmentDto) => void;
  isPending: boolean;
}

const AddAssignmentDialog: FC<AddAssignmentDialogProps> = ({ open, onOpenChange, teamMembers, onSubmit, isPending }) => {
  const [form, setForm] = useState<CreateAssignmentDto>(EMPTY);

  const handleSubmit = () => {
    if (!form.team_member_id || !form.assignment_role || !form.start_date) return;
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
          <DialogTitle>Agregar asignación</DialogTitle>
        </DialogHeader>
        <div className="space-y-3">
          <FormField label="Miembro *">
            <Select onValueChange={v => setForm(f => ({ ...f, team_member_id: Number(v) }))}>
              <SelectTrigger className="w-full"><SelectValue placeholder="Seleccionar miembro" /></SelectTrigger>
              <SelectContent>
                {teamMembers.map(m => (
                  <SelectItem key={m.id} value={String(m.id)}>{m.full_name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FormField>
          <FormField label="Rol en el proyecto *">
            <Input
              value={form.assignment_role}
              onChange={e => setForm(f => ({ ...f, assignment_role: e.target.value }))}
              placeholder="Ej: Tech Lead, Backend Dev..."
            />
          </FormField>
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
            {isPending ? 'Guardando...' : 'Asignar'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export { AddAssignmentDialog };
