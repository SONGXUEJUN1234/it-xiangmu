import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, FolderKanban, Users, Settings, Archive } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';
import { Avatar } from '../ui/Avatar';

interface SidebarProps {
  isOpen: boolean;
}

interface NavItem {
  label: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navItems: NavItem[] = [
  { label: '看板列表', href: '/boards', icon: LayoutDashboard },
];

export function Sidebar({ isOpen }: SidebarProps) {
  const location = useLocation();
  const { user } = useAuthStore();

  return (
    <aside
      className={`fixed left-0 top-14 h-[calc(100vh-3.5rem)] bg-gray-50 dark:bg-gray-900 border-r dark:border-gray-800 transition-all duration-300 z-30 ${
        isOpen ? 'w-64' : 'w-16'
      }`}
    >
      <nav className="p-2 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.href || (item.href !== '/boards' && location.pathname.startsWith(item.href));
          return (
            <Link
              key={item.href}
              to={item.href}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive
                  ? 'bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-400'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-800'
              }`}
              title={!isOpen ? item.label : ''}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {isOpen && <span className="font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      {isOpen && (
        <div className="absolute bottom-4 left-4 right-4">
          <div className="p-3 bg-white dark:bg-gray-800 rounded-lg border dark:border-gray-700">
            <div className="flex items-center gap-3">
              <Avatar src={user?.avatar_url} name={user?.username || ''} size="sm" />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                  {user?.username}
                </p>
                <p className="text-xs text-gray-500 truncate">{user?.email}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </aside>
  );
}
