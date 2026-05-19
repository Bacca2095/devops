import type { FC } from 'react';
import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { FormField } from '@/components/molecules/FormField';
import { ROLE_LABEL, SENIORITY_LABEL } from '@/constants/team-member-labels';
import type { TeamMember, MemberRole, MemberSeniority, UpdateTeamMemberDto } from '@/types/team-member';

interface EditTeamMemberDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (form: UpdateTeamMemberDto) => void;
  isPending: boolean;
  member: TeamMember;
}

const EditTeamMemberDialog: FC<EditTeamMemberDialogProps> = ({ open, onOpenChange, onSubmit, isPending, member }) => {
  const [form, setForm] = useState<UpdateTeamMemberDto>({
    full_name: member.full_name,
    email: member.email,
    document_number: member.document_number,
    role: member.role,
    seniority: member.seniority,
  });

  const handleSubmit = () => {
    if (!form.full_name || !form.email || !form.document_number) return;
    onSubmit(form);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Editar miembro</DialogTitle>
        </DialogHeader>
        <div className="space-y-3">
          <FormField label="Nombre completo *">
            <Input value={form.full_name} onChange={e => setForm(f => ({ ...f, full_name: e.target.value }))} />
          </FormField>
          <FormField label="Email *">
            <Input
              type="email"
              value={form.email}
              onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
            />
          </FormField>
          <FormField label="Número de documento *">
            <Input
              value={form.document_number}
              onChange={e => setForm(f => ({ ...f, document_number: e.target.value }))}
            />
          </FormField>
          <div className="grid grid-cols-2 gap-3">
            <FormField label="Rol">
              <Select value={form.role} onValueChange={v => setForm(f => ({ ...f, role: v as MemberRole }))}>
                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {(Object.keys(ROLE_LABEL) as MemberRole[]).map(r => (
                    <SelectItem key={r} value={r}>{ROLE_LABEL[r]}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </FormField>
            <FormField label="Seniority">
              <Select value={form.seniority} onValueChange={v => setForm(f => ({ ...f, seniority: v as MemberSeniority }))}>
                <SelectTrigger className="w-full"><SelectValue /></SelectTrigger>
                <SelectContent>
                  {(Object.keys(SENIORITY_LABEL) as MemberSeniority[]).map(s => (
                    <SelectItem key={s} value={s}>{SENIORITY_LABEL[s]}</SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </FormField>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>Cancelar</Button>
          <Button onClick={handleSubmit} disabled={isPending}>
            {isPending ? 'Guardando...' : 'Guardar'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export { EditTeamMemberDialog };
