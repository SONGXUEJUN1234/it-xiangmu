import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Textarea } from '../ui/Textarea';
import { Select } from '../ui/Select';
import { Button } from '../ui/Button';
import { useBoardDetail } from '../../hooks/useBoardDetail';
import { CreateCardFormData } from '../../types';

const priorityOptions = [
  { value: 'low', label: '低' },
  { value: 'medium', label: '中' },
  { value: 'high', label: '高' },
  { value: 'critical', label: '紧急' },
];

interface CreateCardModalProps {
  isOpen: boolean;
  onClose: () => void;
  listId: string;
}

export function CreateCardModal({ isOpen, onClose, listId }: CreateCardModalProps) {
  const { createCard } = useBoardDetail();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateCardFormData>({
    defaultValues: {
      title: '',
      description: '',
      priority: 'medium',
    },
  });

  const onSubmit = async (data: CreateCardFormData) => {
    setIsLoading(true);
    setError(null);
    const result = await createCard(listId, data);
    setIsLoading(false);

    if (result.success) {
      reset();
      onClose();
    } else {
      setError(result.error || '创建卡片失败');
    }
  };

  const handleClose = () => {
    reset();
    setError(null);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="创建卡片" size="sm">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        <Input
          label="卡片标题"
          placeholder="输入任务标题"
          error={errors.title?.message}
          {...register('title', {
            required: '请输入卡片标题',
          })}
        />

        <Textarea
          label="描述"
          placeholder="添加详细描述..."
          rows={4}
          {...register('description')}
        />

        <Select
          label="优先级"
          options={priorityOptions}
          {...register('priority')}
        />

        <Input
          label="截止日期"
          type="datetime-local"
          {...register('due_date')}
        />

        {error && (
          <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-sm text-red-600 dark:text-red-400">
            {error}
          </div>
        )}

        <div className="flex gap-3 pt-2">
          <Button type="button" variant="ghost" onClick={handleClose} className="flex-1">
            取消
          </Button>
          <Button type="submit" isLoading={isLoading} className="flex-1">
            创建
          </Button>
        </div>
      </form>
    </Modal>
  );
}
