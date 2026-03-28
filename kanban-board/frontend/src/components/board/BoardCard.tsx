import { Board } from '../../types';
import { Card as UICard } from '../ui/Card';
import { Users, Star, Archive } from 'lucide-react';
import { Link } from 'react-router-dom';

interface BoardCardProps {
  board: Board;
  onArchive?: (boardId: string) => void;
  onDelete?: (boardId: string) => void;
  onFavorite?: (boardId: string) => void;
}

export function BoardCard({ board, onArchive, onDelete }: BoardCardProps) {
  const getBackgroundStyle = () => {
    if (board.background_url) {
      return { backgroundImage: `url(${board.background_url})`, backgroundSize: 'cover' };
    }
    return { backgroundColor: board.background_color || '#0079BF' };
  };

  return (
    <Link to={`/boards/${board.id}`}>
      <UICard hover className="overflow-hidden h-40">
        <div
          className="h-24 w-full relative"
          style={getBackgroundStyle()}
        >
          {board.is_archived && (
            <div className="absolute top-2 right-2">
              <span className="px-2 py-1 bg-black/50 text-white text-xs rounded-lg flex items-center gap-1">
                <Archive className="w-3 h-3" />
                已归档
              </span>
            </div>
          )}
        </div>
        <div className="p-3">
          <h3 className="font-semibold text-gray-900 dark:text-white truncate">{board.title}</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 truncate mt-1">
            {board.description}
          </p>
          <div className="flex items-center gap-3 mt-3 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              <Users className="w-4 h-4" />
              {board.member_count || board.members?.length || 1}
            </span>
          </div>
        </div>
      </UICard>
    </Link>
  );
}
