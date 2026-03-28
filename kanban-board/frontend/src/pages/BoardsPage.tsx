import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Archive } from 'lucide-react';
import { Header } from '../components/layout/Header';
import { Sidebar } from '../components/layout/Sidebar';
import { BoardCard } from '../components/board/BoardCard';
import { CreateBoardModal } from '../components/board/CreateBoardModal';
import { Input } from '../components/ui/Input';
import { Button } from '../components/ui/Button';
import { useBoards } from '../hooks/useBoards';
import { useUIStore } from '../store/uiStore';
import { CreateBoardFormData } from '../types';

export function BoardsPage() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [showArchived, setShowArchived] = useState(false);

  const { boards, isLoading, createBoard, archiveBoard, deleteBoard } = useBoards({
    archived: showArchived,
  });

  const { sidebarOpen } = useUIStore();

  const handleCreateBoard = async (data: CreateBoardFormData) => {
    return await createBoard(data);
  };

  const handleArchiveBoard = async (boardId: string) => {
    await archiveBoard(boardId);
  };

  const handleDeleteBoard = async (boardId: string) => {
    if (confirm('确定要删除这个看板吗？此操作无法撤销。')) {
      await deleteBoard(boardId);
    }
  };

  const filteredBoards = boards.filter((board) => {
    if (!board) return false;
    const matchesSearch = board.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (board.description && board.description.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesArchived = showArchived ? board.is_archived : !board.is_archived;
    return matchesSearch && matchesArchived;
  });

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <Header onCreateBoard={() => setIsCreateModalOpen(true)} />
      <Sidebar isOpen={sidebarOpen} />

      <main
        className={`transition-all duration-300 ${
          sidebarOpen ? 'ml-64' : 'ml-16'
        }`}
      >
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">我的看板</h1>
              <p className="text-gray-600 dark:text-gray-400 mt-1">管理和组织你的任务</p>
            </div>
          </div>

          <div className="flex items-center gap-4 mb-6">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <Input
                placeholder="搜索看板..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button
              variant={showArchived ? 'secondary' : 'ghost'}
              onClick={() => setShowArchived(!showArchived)}
            >
              <Archive className="w-4 h-4 mr-2" />
              {showArchived ? '显示活跃' : '显示归档'}
            </Button>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
            </div>
          ) : filteredBoards.length === 0 ? (
            <div className="text-center py-16">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 dark:bg-gray-800 rounded-2xl mb-4">
                <Archive className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                {searchQuery ? '没有找到匹配的看板' : '还没有看板'}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-6">
                {searchQuery ? '尝试其他关键词' : '创建你的第一个看板来开始管理任务'}
              </p>
              {!searchQuery && (
                <Button onClick={() => setIsCreateModalOpen(true)}>
                  创建看板
                </Button>
              )}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {filteredBoards.map((board) => (
                <div key={board.id} className="relative group">
                  <BoardCard board={board} />
                  <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Link
                      to={`/boards/${board.id}/settings`}
                      className="p-2 bg-white/90 dark:bg-gray-800/90 rounded-lg shadow hover:bg-gray-100 dark:hover:bg-gray-700"
                    >
                      ⋮
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      <CreateBoardModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreate={handleCreateBoard}
      />
    </div>
  );
}
