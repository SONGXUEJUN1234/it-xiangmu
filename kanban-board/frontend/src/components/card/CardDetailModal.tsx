import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import {
  Calendar,
  User,
  Tag,
  AlertCircle,
  AlignLeft,
  Check,
  X,
  Trash2,
  MessageSquare,
  Clock,
} from 'lucide-react';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { Select } from '../ui/Select';
import { Button } from '../ui/Button';
import { Badge } from '../ui/Badge';
import { Avatar } from '../ui/Avatar';
import { useCardDetail } from '../../hooks/useCardDetail';
import { useUIStore } from '../../store/uiStore';
import { Card } from '../../types';

const priorityOptions = [
  { value: 'low', label: '低' },
  { value: 'medium', label: '中' },
  { value: 'high', label: '高' },
  { value: 'critical', label: '紧急' },
];

const priorityColors = {
  low: 'text-gray-500 bg-gray-100',
  medium: 'text-yellow-600 bg-yellow-100',
  high: 'text-orange-600 bg-orange-100',
  critical: 'text-red-600 bg-red-100',
};

export function CardDetailModal() {
  const { cardModalOpen, selectedCardId, selectedListId, closeCardModal } = useUIStore();

  const { card, comments, updateCard, createComment, deleteComment } = useCardDetail(
    selectedCardId || ''
  );

  const [isEditing, setIsEditing] = useState(false);
  const [isEditingDescription, setIsEditingDescription] = useState(false);
  const [newComment, setNewComment] = useState('');
  const [commentLoading, setCommentLoading] = useState(false);

  const {
    register: registerTitle,
    handleSubmit: handleSubmitTitle,
    reset: resetTitle,
  } = useForm<{ title: string }>({
    defaultValues: { title: card?.title || '' },
  });

  const {
    register: registerDescription,
    handleSubmit: handleSubmitDescription,
    reset: resetDescription,
  } = useForm<{ description: string }>({
    defaultValues: { description: card?.description || '' },
  });

  useEffect(() => {
    if (card) {
      resetTitle({ title: card.title });
      resetDescription({ description: card.description || '' });
    }
  }, [card, resetTitle, resetDescription]);

  if (!selectedCardId) return null;

  const handleTitleSubmit = async (data: { title: string }) => {
    const result = await updateCard({ title: data.title });
    if (result.success) {
      setIsEditing(false);
    }
  };

  const handleDescriptionSubmit = async (data: { description: string }) => {
    const result = await updateCard({ description: data.description });
    if (result.success) {
      setIsEditingDescription(false);
    }
  };

  const handleToggleComplete = async () => {
    await updateCard({ is_completed: !card?.is_completed });
  };

  const handleSubmitComment = async () => {
    if (!newComment.trim()) return;
    setCommentLoading(true);
    const result = await createComment({ content: newComment });
    if (result.success) {
      setNewComment('');
    }
    setCommentLoading(false);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const isOverdue = card?.due_date && new Date(card.due_date) < new Date() && !card.is_completed;

  return (
    <Modal isOpen={cardModalOpen} onClose={closeCardModal} size="lg">
      {!card ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-start justify-between">
            {isEditing ? (
              <form onSubmit={handleSubmitTitle(handleTitleSubmit)} className="flex-1 flex gap-2">
                <Input
                  defaultValue={card.title}
                  {...registerTitle('title', { required: true })}
                  className="flex-1"
                />
                <Button type="submit" size="sm">
                  <Check className="w-4 h-4" />
                </Button>
                <Button type="button" variant="ghost" size="sm" onClick={() => setIsEditing(false)}>
                  <X className="w-4 h-4" />
                </Button>
              </form>
            ) : (
              <div className="flex items-center gap-2 flex-1">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white">{card.title}</h2>
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors"
                >
                  <MessageSquare className="w-4 h-4 text-gray-400" />
                </button>
              </div>
            )}
            <button
              onClick={closeCardModal}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>

          {/* Meta Info */}
          <div className="flex flex-wrap gap-4 text-sm">
            <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
              <AlignLeft className="w-4 h-4" />
              <span>列表：{card.list?.title || selectedListId}</span>
            </div>
            {card.board && (
              <div className="flex items-center gap-2 text-gray-600 dark:text-gray-400">
                <Tag className="w-4 h-4" />
                <span>看板：{card.board.title}</span>
              </div>
            )}
          </div>

          {/* Priority & Due Date */}
          <div className="flex items-center gap-4">
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${priorityColors[card.priority]}`}>
              <div className="flex items-center gap-1">
                <AlertCircle className="w-4 h-4" />
                <span className="capitalize">
                  {card.priority === 'critical' ? '紧急' : card.priority === 'high' ? '高' : card.priority === 'medium' ? '中' : '低'}
                </span>
              </div>
            </div>

            {card.due_date && (
              <div className={`flex items-center gap-1 text-sm ${isOverdue ? 'text-red-600' : 'text-gray-600 dark:text-gray-400'}`}>
                <Calendar className="w-4 h-4" />
                <span>{formatDate(card.due_date)}</span>
                {isOverdue && <span className="text-xs">(已逾期)</span>}
              </div>
            )}

            <button
              onClick={handleToggleComplete}
              className={`ml-auto px-3 py-1 rounded-lg text-sm font-medium flex items-center gap-1 transition-colors ${
                card.is_completed
                  ? 'bg-green-100 text-green-700'
                  : 'bg-gray-100 text-gray-700 hover:bg-green-100 hover:text-green-700'
              }`}
            >
              <Check className="w-4 h-4" />
              {card.is_completed ? '已完成' : '标记完成'}
            </button>
          </div>

          {/* Description */}
          <div>
            <div className="flex items-center gap-2 mb-2">
              <AlignLeft className="w-5 h-5 text-gray-500" />
              <h3 className="font-medium text-gray-900 dark:text-white">描述</h3>
              <button
                onClick={() => setIsEditingDescription(true)}
                className="ml-auto p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors"
              >
                <MessageSquare className="w-4 h-4 text-gray-400" />
              </button>
            </div>

            {isEditingDescription ? (
              <form onSubmit={handleSubmitDescription(handleDescriptionSubmit)}>
                <Textarea
                  defaultValue={card.description || ''}
                  {...registerDescription('description')}
                  rows={4}
                  className="mb-2"
                />
                <div className="flex gap-2">
                  <Button type="submit" size="sm">
                    保存
                  </Button>
                  <Button type="button" variant="ghost" size="sm" onClick={() => setIsEditingDescription(false)}>
                    取消
                  </Button>
                </div>
              </form>
            ) : (
              <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg min-h-[60px]">
                {card.description ? (
                  <p className="text-gray-700 dark:text-gray-300 whitespace-pre-wrap">{card.description}</p>
                ) : (
                  <button
                    onClick={() => setIsEditingDescription(true)}
                    className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 text-sm"
                  >
                    添加描述...
                  </button>
                )}
              </div>
            )}
          </div>

          {/* Labels */}
          {card.labels && card.labels.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Tag className="w-5 h-5 text-gray-500" />
                <h3 className="font-medium text-gray-900 dark:text-white">标签</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {card.labels.map((label) => (
                  <span
                    key={label.id}
                    className="px-3 py-1 rounded-full text-sm text-white"
                    style={{ backgroundColor: label.color }}
                  >
                    {label.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Assignee */}
          {card.assignee && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <User className="w-5 h-5 text-gray-500" />
                <h3 className="font-medium text-gray-900 dark:text-white">负责人</h3>
              </div>
              <div className="flex items-center gap-2">
                <Avatar src={card.assignee.avatar_url} name={card.assignee.username} size="sm" />
                <span className="text-gray-700 dark:text-gray-300">{card.assignee.username}</span>
              </div>
            </div>
          )}

          {/* Comments */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <MessageSquare className="w-5 h-5 text-gray-500" />
              <h3 className="font-medium text-gray-900 dark:text-white">评论 ({comments.length})</h3>
            </div>

            <div className="space-y-3 mb-4 max-h-48 overflow-y-auto">
              {comments.map((comment) => (
                <div key={comment.id} className="flex gap-3">
                  <Avatar src={comment.author?.avatar_url} name={comment.author?.username || 'User'} size="sm" />
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-gray-900 dark:text-white text-sm">
                        {comment.author?.username || 'User'}
                      </span>
                      <span className="text-xs text-gray-500">
                        {formatDate(comment.created_at)}
                      </span>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300 text-sm mt-1">{comment.content}</p>
                  </div>
                  <button
                    onClick={() => deleteComment(comment.id)}
                    className="p-1 hover:bg-gray-100 dark:hover:bg-gray-800 rounded transition-colors opacity-0 group-hover:opacity-100"
                  >
                    <Trash2 className="w-3 h-3 text-gray-400" />
                  </button>
                </div>
              ))}
              {comments.length === 0 && (
                <p className="text-sm text-gray-500 text-center py-4">暂无评论</p>
              )}
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                placeholder="添加评论..."
                className="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-800 text-sm"
              />
              <button
                type="button"
                disabled={!newComment.trim() || commentLoading}
                onClick={() => {
                  if (!newComment.trim()) return;
                  setCommentLoading(true);
                  createComment({ content: newComment }).then(() => {
                    setNewComment('');
                    setCommentLoading(false);
                  }).catch(() => {
                    setCommentLoading(false);
                  });
                }}
                className="px-3 py-1.5 text-sm font-medium rounded-lg bg-primary-600 text-white hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {commentLoading ? '发送中...' : '发送'}
              </button>
            </div>
          </div>

          {/* Footer Info */}
          <div className="pt-4 border-t dark:border-gray-700 text-xs text-gray-500 flex items-center gap-2">
            <Clock className="w-3 h-3" />
            <span>创建于 {formatDate(card.created_at)}</span>
            {card.updated_at !== card.created_at && (
              <span>· 更新于 {formatDate(card.updated_at)}</span>
            )}
          </div>
        </div>
      )}
    </Modal>
  );
}
