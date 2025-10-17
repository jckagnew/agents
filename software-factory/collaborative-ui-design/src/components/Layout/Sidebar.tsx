import React from 'react';

interface SidebarProps {
  children: React.ReactNode;
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ children, className = '' }) => {
  return (
    <aside className={`w-80 bg-white border-r border-gray-200 flex flex-col ${className}`}>
      {children}
    </aside>
  );
};

export default Sidebar;
