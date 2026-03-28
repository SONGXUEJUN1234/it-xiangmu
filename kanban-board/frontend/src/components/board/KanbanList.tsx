import { useState } from 'react';
import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Plus, MoreHorizontal, Trash2, Edit2, GripVertical } from 'lucide-react';
import { List } from '../../types';
import { KanbanCard } from './KanbanCard';
import { CreateCardModal } from './CreateCardModal';
import { Button } from '../ui/Button';

interface KanbanListProps {
  list: List;
  onUpdateList: (listId: string, data: Partial<List>) => Promise<any>;
  onDeleteList: (listId: string, moveToListId?: string) => Promise<any>;
}

function SortableListHeader({ list, onEdit, onDelete }: { list: List; onEdit: () => void; onDelete: () => void }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: `list:${list.id}` });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-2 flex-1">
        <button {...attributes} {...listeners} className="cursor-grab active:cursor-grabbing text-gray-400 hover:text-gray-600">
          <GripVertical className="w-5 h-5" />
        </button>
        <h3 className="font-semibold text-gray-900 dark:text-white flex-1">{list.title}</h3>
        <span className="text-sm text-gray-500">{list.cards?.length || 0}</span>
      </div>
      <div className="relative">
        <button className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
          <MoreHorizontal className="w-5 h-5 text-gray-400" />
        </button>
      </div>
    </div>
  );
}

export function KanbanList({ list, onUpdateList, onDeleteList }: KanbanListProps) {
  const [isCreateCardOpen, setIsCreateCardOpen] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [title, setTitle] = useState(list.title);

  const { setNodeRef } = useDroppable({
    id: `list:${list.id}`,
    data: { list },
  });

  const cardIds = (list.cards || []).map((card) => `card:${card.id}:${list.id}`);

  const handleSaveTitle = async () => {
    if (title && title !== list.title) {
      await onUpdateList(list.id, { title });
    }
    setIsEditing(false);
  };

  const handleDeleteList = async () => {
    if (confirm(`确定要删除列表 "${list.title}" 吗？`)) {
      await onDeleteList(list.id);
    }
  };

  return (
    <div className="flex-shrink-0 w-80 bg-gray-100 dark:bg-gray-800 rounded-xl p-3 max-h-[calc(100vh-180px)] flex flex-col">
      <SortableListHeader
        list={list}
        onEdit={() => setIsEditing(true)}
        onDelete={handleDeleteList}
      />

      {isEditing ? (
        <div className="mb-3">
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onBlur={handleSaveTitle}
            onKeyDown={(e) => {
              if (e.key === 'Enter') handleSaveTitle();
              if (e.key === 'Escape') {
                setTitle(list.title);
                setIsEditing(false);
              }
            }}
            className="w-full px-2 py-1 text-sm border rounded focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700"
            autoFocus
          />
        </div>
      ) : null}

      <div ref={setNodeRef} className="flex-1 overflow-y-auto space-y-2 min-h-[50px]">
        <SortableContext items={cardIds} strategy={verticalListSortingStrategy}>
          {(list.cards || []).map((card) => (
            <KanbanCard key={card.id} card={card} listId={list.id} />
          ))}
        </SortableContext>
      </div>

      <button
        onClick={() => setIsCreateCardOpen(true)}
        className="mt-3 w-full p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg transition-colors text-left text-gray-600 dark:text-gray-400 flex items-center gap-2"
      >
        <Plus className="w-4 h-4" />
        <span>添加卡片</span>
      </button>

      <CreateCardModal
        isOpen={isCreateCardOpen}
        onClose={() => setIsCreateCardOpen(false)}
        listId={list.id}
      />
    </div>
  );
}
