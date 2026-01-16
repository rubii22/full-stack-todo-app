import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
}

export default function Card({ children, className = '', header, footer }: CardProps) {
  return (
    <div className={`bg-white shadow overflow-hidden sm:rounded-lg ${className}`}>
      {header && <div className="px-4 py-5 sm:px-6 border-b border-gray-200">{header}</div>}
      <div className="px-4 py-5 sm:p-6">{children}</div>
      {footer && <div className="px-4 py-5 sm:px-6 border-t border-gray-200">{footer}</div>}
    </div>
  );
}