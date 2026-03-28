import { Link, useNavigate } from 'react-router-dom';
import { Plus, Settings, LogOut, Search, Bell, Moon, Sun } from 'lucide-react';
import { Button } from '../ui/Button';
import { Avatar } from '../ui/Avatar';
import { useAuthStore } from '../../store/authStore';
import { useUIStore } from '../../store/uiStore';

interface HeaderProps {
  onCreateBoard?: () => void;
  showCreateButton?: boolean;
}

export function Header({ onCreateBoard, showCreateButton = true }: HeaderProps) {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { theme, setTheme, toggleSidebar } = useUIStore();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  return (
    <header className="h-14 bg-white dark:bg-gray-900 border-b dark:border-gray-800 flex items-center justify-between px-4 sticky top-0 z-40">
      <div className="flex items-center gap-4">
        <Link to="/boards" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">K</span>
          </div>
          <span className="font-semibold text-gray-900 dark:text-white hidden sm:block">任务看板</span>
        </Link>
      </div>

      <div className="flex items-center gap-2">
        {showCreateButton && onCreateBoard && (
          <Button size="sm" onClick={onCreateBoard}>
            <Plus className="w-4 h-4 mr-1" />
            <span className="hidden sm:inline">新建看板</span>
          </Button>
        )}

        <button
          onClick={toggleTheme}
          className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
          title={theme === 'light' ? '切换到深色模式' : '切换到浅色模式'}
        >
          {theme === 'light' ? <Moon className="w-5 h-5 text-gray-600" /> : <Sun className="w-5 h-5 text-gray-400" />}
        </button>

        <button className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors relative">
          <Bell className="w-5 h-5 text-gray-600 dark:text-gray-400" />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        <div className="relative group">
          <button className="flex items-center gap-2 p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors">
            <Avatar src={user?.avatar_url} name={user?.username || ''} size="sm" />
            <span className="hidden md:block text-sm font-medium text-gray-700 dark:text-gray-300">
              {user?.username}
            </span>
          </button>

          <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
            <Link
              to="/settings"
              className="flex items-center gap-2 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 first:rounded-t-lg"
            >
              <Settings className="w-4 h-4" />
              设置
            </Link>
            <hr className="border-gray-200 dark:border-gray-700" />
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 w-full last:rounded-b-lg"
            >
              <LogOut className="w-4 h-4" />
              退出登录
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
