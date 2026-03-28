import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/Button';

export function NotFoundPage() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center px-4">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-6">
          <span className="text-4xl font-bold text-primary-600 dark:text-primary-400">404</span>
        </div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">页面不存在</h1>
        <p className="text-gray-600 dark:text-gray-400 mb-8">抱歉，您访问的页面不存在或已被删除。</p>
        <div className="flex items-center justify-center gap-4">
          <Button variant="secondary" onClick={() => window.history.back()}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            返回上一页
          </Button>
          <Link to="/boards" className="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
            <Home className="w-4 h-4" />
            回到首页
          </Link>
        </div>
      </div>
    </div>
  );
}
