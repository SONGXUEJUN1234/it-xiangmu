import { useState, useRef } from 'react';
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
  PointerSensor,
  useSensor,
  useSensors,
  closestCorners,
} from '@dnd-kit/core';
import { SortableContext, horizontalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { Plus, MoreHorizontal, GripVertical } from 'lucide-react';
import { List } from '../../types';
import { useBoardDetail } from '../../hooks/useBoardDetail';
import { KanbanList } from './KanbanList';
import { CreateListModal } from './CreateListModal';
import { Button } from '../ui/Button';

interface KanbanBoardProps {
  boardId: string;
}

export function KanbanBoard({ boardId }: KanbanBoardProps) {
  const { lists, createList, updateList, deleteList, moveCard } = useBoardDetail();
  const [isCreateListOpen, setIsCreateListOpen] = useState(false);
  const [activeCard, setActiveCard] = useState<any>(null);
  const [activeList, setActiveList] = useState<any>(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const handleDragStart = (event: DragStartEvent) => {
    const { active } = event;
    const [type, id, listId] = (active.id as string).split(':');

    if (type === 'card') {
      const list = lists.find((l) => l.id === listId);
      const card = list?.cards?.find((c) => c.id === id);
      setActiveCard(card);
    } else if (type === 'list') {
      const list = lists.find((l) => l.id === id);
      setActiveList(list);
    }
  };

  const handleDragEnd = async (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveCard(null);
    setActiveList(null);

    if (!over) return;

    const activeId = active.id as string;
    const overId = over.id as string;

    const [activeType, activeIdValue, activeListId] = activeId.split(':');
    const [overType, overIdValue, overListId] = overId.split(':');

    // Handle list reordering
    if (activeType === 'list' && overType === 'list') {
      const oldIndex = lists.findIndex((l) => l.id === activeIdValue);
      const newIndex = lists.findIndex((l) => l.id === overIdValue);

      if (oldIndex !== newIndex) {
        const newLists = [...lists];
        const [movedList] = newLists.splice(oldIndex, 1);
        newLists.splice(newIndex, 0, movedList);

        // Update positions
        for (let i = 0; i < newLists.length; i++) {
          if (newLists[i].position !== i) {
            updateList(newLists[i].id, { position: i });
          }
        }
      }
      return;
    }

    // Handle card moving
    if (activeType === 'card' && overType === 'card') {
      const sourceList = lists.find((l) => l.id === activeListId);
      const destList = lists.find((l) => l.id === overListId);

      if (!sourceList || !destList) return;

      const sourceCards = [...(sourceList.cards || [])];
      const destCards = sourceList.id === destList.id ? sourceCards : [...(destList.cards || [])];

      const oldIndex = sourceCards.findIndex((c) => c.id === activeIdValue);
      const newIndex = destCards.findIndex((c) => c.id === overIdValue);

      if (oldIndex === -1) return;

      const [movedCard] = sourceCards.splice(oldIndex, 1);
      destCards.splice(newIndex, 0, movedCard);

      // Update the card position via API
      await moveCard(activeIdValue, destList.id, newIndex);
    } else if (activeType === 'card' && overType === 'list') {
      // Moving card to an empty position in a list
      const destList = lists.find((l) => l.id === overIdValue);
      if (!destList) return;

      const newPosition = (destList.cards?.length || 0);
      await moveCard(activeIdValue, destList.id, newPosition);
    }
  };

  const handleCreateList = async (data: { title: string }) => {
    const position = lists.length;
    const result = await createList({ title: data.title, position });
    return result;
  };

  return (
    <div className="flex-1 overflow-x-auto overflow-y-hidden p-6">
      <DndContext
        sensors={sensors}
        collisionDetection={closestCorners}
        onDragStart={handleDragStart}
        onDragEnd={handleDragEnd}
      >
        <div className="flex gap-4 h-full items-start">
          <SortableContext items={lists.map((l) => `list:${l.id}`)} strategy={horizontalListSortingStrategy}>
            {lists.map((list) => (
              <KanbanList
                key={list.id}
                list={list}
                onUpdateList={updateList}
                onDeleteList={deleteList}
              />
            ))}
          </SortableContext>

          <div className="flex-shrink-0 w-80">
            <button
              onClick={() => setIsCreateListOpen(true)}
              className="w-full p-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-xl transition-colors text-left text-gray-600 dark:text-gray-400"
            >
              <span className="flex items-center gap-2">
                <Plus className="w-5 h-5" />
                添加列表
              </span>
            </button>
          </div>
        </div>

        <DragOverlay>
          {activeCard && (
            <div className="w-72 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-xl opacity-80">
              <p className="font-medium text-gray-900 dark:text-white">{activeCard.title}</p>
            </div>
          )}
          {activeList && (
            <div className="w-80 bg-gray-50 dark:bg-gray-800 p-4 rounded-lg shadow-xl opacity-80">
              <p className="font-medium text-gray-900 dark:text-white">{activeList.title}</p>
            </div>
          )}
        </DragOverlay>
      </DndContext>

      <CreateListModal
        isOpen={isCreateListOpen}
        onClose={() => setIsCreateListOpen(false)}
        onCreate={handleCreateList}
      />
    </div>
  );
}
