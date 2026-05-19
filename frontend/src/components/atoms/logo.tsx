import type { FC } from 'react';
import { useTheme } from 'next-themes';

interface LogoProps {
  size?: number;
}

const Logo: FC<LogoProps> = ({ size = 28 }) => {
  const { resolvedTheme } = useTheme();
  const isDark = resolvedTheme === 'dark';
  const fg = isDark ? '#ffffff' : '#000000';
  const bg = isDark ? '#000000' : '#ffffff';

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      xmlns="http://www.w3.org/2000/svg"
      style={{ fillRule: 'evenodd', clipRule: 'evenodd' }}
    >
      <path
        d="M24,6L24,18C24,21.311 21.311,24 18,24L6,24C2.689,24 0,21.311 0,18L0,6C0,2.689 2.689,0 6,0L18,0C21.311,0 24,2.689 24,6Z"
        fill={fg}
      />
      <g transform="matrix(0.8,0,0,0.764706,2.4,2.823529)">
        <path
          d="M4,20.5L20,20.5C21.097,20.5 22,19.597 22,18.5L22,8.5C22,7.403 21.097,6.5 20,6.5L12.07,6.5C11.402,6.497 10.778,6.158 10.41,5.6L9.59,4.4C9.222,3.842 8.598,3.503 7.93,3.5L4,3.5C2.903,3.5 2,4.403 2,5.5L2,18.5C2,19.6 2.9,20.5 4,20.5Z"
          fill="none"
          stroke={bg}
          strokeWidth={2}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path d="M8,10.5L8,14.5" fill="none" stroke={bg} strokeWidth={2} strokeLinecap="round" />
        <path d="M12,10.5L12,12.5" fill="none" stroke={bg} strokeWidth={2} strokeLinecap="round" />
        <path d="M16,10.5L16,16.5" fill="none" stroke={bg} strokeWidth={2} strokeLinecap="round" />
      </g>
    </svg>
  );
};

export { Logo };
