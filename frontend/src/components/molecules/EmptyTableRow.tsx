import type { FC } from 'react';
import { TableRow, TableCell } from '@/components/ui/table';

interface EmptyTableRowProps {
  colSpan: number;
  message: string;
}

const EmptyTableRow: FC<EmptyTableRowProps> = ({ colSpan, message }) => (
  <TableRow>
    <TableCell colSpan={colSpan} className="text-center text-muted-foreground py-12">
      {message}
    </TableCell>
  </TableRow>
);

export { EmptyTableRow };
