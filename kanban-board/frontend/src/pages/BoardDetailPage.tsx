import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { Star, Settings, Users, RefreshCw } from 'lucide-react';
import { Header } from '../components/layout/Header';
import { Sidebar } from '../components/layout/Sidebar';
import { KanbanBoard } from '../components/board/KanbanBoard';
import { Button } from '../components/ui/Button';
import { boardService } from '../services/board.service';
import { useUIStore } from '../store/uiStore';
import { Board, List } from '../types';

export function BoardDetailPage() {
  const { boardId } = useParams<{ boardId: string }>();
  const { sidebarOpen } = useUIStore();
  
  const [board, setBoard] = useState<Board | null>(null);
  const [lists, setLists] = useState<List[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBoard = async () => {
    if (!boardId) return;
    
    setIsLoading(true);
    setError(null);
    try {
      const response = await boardService.getBoard(boardId);
      setBoard(response);
      setLists(response.lists || []);
    } catch (err: any) {
      setError(err.response?.data?.error?.message || '获取看板详情失败');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBoard();
  }, [boardId]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!board) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">看板不存在</h2>
          <Button onClick={() => window.history.back()}>返回</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-950">
      <Header showCreateButton={false} />
      <Sidebar isOpen={sidebarOpen} />

      <div
        className={`flex-1 flex flex-col overflow-hidden transition-all duration-300 ${
          sidebarOpen ? 'ml-64' : 'ml-16'
        }`}
      >
        {/* Board Header */}
        <div className="flex-shrink-0 p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div
              className="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold"
              style={{ backgroundColor: board.background_color }}
            >
              {board.title[0].toUpperCase()}
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">{board.title}</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400">{board.description}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="ghost" size="sm" onClick={fetchBoard}>
              <RefreshCw className="w-4 h-4" />
            </Button>

            <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-100 dark:bg-gray-800 rounded-lg">
              <Users className="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <span className="text-sm text-gray-700 dark:text-gray-300">
                {board.members?.length || board.member_count || 1}
              </span>
            </div>

            <Button variant="ghost" size="sm">
              <Star className="w-4 h-4" />
            </Button>

            <Button variant="ghost" size="sm">
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        </div>

        {/* Kanban Board */}
        {boardId && <KanbanBoard boardId={boardId} />}
      </div>
    </div>
  );
}
