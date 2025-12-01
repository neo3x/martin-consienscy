/**
 * Sidebar navigation component.
 */

import { Link, useLocation } from 'react-router-dom';
import clsx from 'clsx';

interface NavItem {
  path: string;
  label: string;
  icon: string;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Chat', icon: '💬' },
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/memory', label: 'Memory', icon: '🧠' },
  { path: '/timeline', label: 'Timeline', icon: '📅' },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 bg-surface border-r border-border flex flex-col">
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.path}
              to={item.path}
              className={clsx(
                'flex items-center gap-3 px-4 py-3 rounded-lg transition-colors',
                isActive
                  ? 'bg-accent text-white'
                  : 'text-text-secondary hover:bg-border hover:text-text-primary'
              )}
            >
              <span className="text-xl">{item.icon}</span>
              <span className="font-medium">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <button className="w-full px-4 py-2 text-sm text-text-secondary hover:text-text-primary hover:bg-border rounded-lg transition-colors">
          ⚙️ Settings
        </button>
      </div>
    </aside>
  );
}
