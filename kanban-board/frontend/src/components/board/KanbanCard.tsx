import { useRef } from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Card } from '../../types';
import { Calendar, AlertCircle, AlignLeft } from 'lucide-react';
import { useUIStore } from '../../store/uiStore';

interface KanbanCardProps {
  card: Card;
  listId: string;
}

const priorityColors = {
  low: 'text-gray-500',
  medium: 'text-yellow-600',
  high: 'text-orange-600',
  critical: 'text-red-600',
};

const priorityIcons = {
  low: null,
  medium: <AlertCircle className="w-3 h-3" />,
  high: <AlertCircle className="w-3 h-3" />,
  critical: <AlertCircle className="w-3 h-3" />,
};

export function KanbanCard({ card, listId }: KanbanCardProps) {
  const openCardModal = useUIStore((state) => state.openCardModal);
  const dragStartTime = useRef<number | null>(null);

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({
    id: `card:${card.id}:${listId}`,
    data: { type: 'card', card, listId },
  });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  const isOverdue = card.due_date && new Date(card.due_date) < new Date() && !card.is_completed;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
  };

  const handleClick = () => {
    if (dragStartTime.current) {
      const dragDuration = Date.now() - dragStartTime.current;
      if (dragDuration < 200) {
        openCardModal(card.id, listId);
      }
      dragStartTime.current = null;
    } else {
      openCardModal(card.id, listId);
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      {...listeners}
      onPointerDown={() => {
        dragStartTime.current = Date.now();
      }}
      onClick={handleClick}
      className="bg-white dark:bg-gray-700 p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
    >
      {card.priority && card.priority !== 'low' && (
        <div className={`flex items-center gap-1 text-xs mb-2 ${priorityColors[card.priority]}`}>
          {priorityIcons[card.priority]}
          <span className="capitalize">{card.priority === 'critical' ? '紧急' : card.priority === 'high' ? '高' : card.priority === 'medium' ? '中' : '低'}</span>
        </div>
      )}

      <h4 className="font-medium text-gray-900 dark:text-white mb-2">{card.title}</h4>

      {card.description && (
        <div className="flex items-center gap-1 text-gray-500 text-sm mb-2">
          <AlignLeft className="w-3 h-3" />
          <span className="truncate">{card.description}</span>
        </div>
      )}

      {card.labels && card.labels.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {card.labels.map((label) => (
            <span
              key={label.id}
              className="px-2 py-0.5 text-xs rounded-full text-white"
              style={{ backgroundColor: label.color }}
            >
              {label.name}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between mt-3">
        {card.due_date && (
          <div className={`flex items-center gap-1 text-xs ${isOverdue ? 'text-red-600' : 'text-gray-500'}`}>
            <Calendar className="w-3 h-3" />
            <span>{formatDate(card.due_date)}</span>
          </div>
        )}

        {card.assignee && (
          <div
            className="w-6 h-6 rounded-full bg-primary-500 text-white text-xs flex items-center justify-center"
            title={card.assignee.username}
          >
            {card.assignee.username[0].toUpperCase()}
          </div>
        )}
      </div>
    </div>
  );
}
