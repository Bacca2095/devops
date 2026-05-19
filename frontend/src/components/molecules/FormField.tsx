import type { FC, ReactNode } from 'react';
import { Label } from '@/components/ui/label';

interface FormFieldProps {
  label: string;
  children: ReactNode;
}

const FormField: FC<FormFieldProps> = ({ label, children }) => {
  const required = label.endsWith(' *');
  const text = required ? label.slice(0, -2) : label;

  return (
    <div className="space-y-1">
      <Label>
        {text}
        {required && <span className="text-red-500 ml-0.5">*</span>}
      </Label>
      {children}
    </div>
  );
};

export { FormField };
