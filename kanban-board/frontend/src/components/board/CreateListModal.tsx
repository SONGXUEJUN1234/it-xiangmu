import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

interface CreateListModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (data: { title: string }) => Promise<any>;
}

export function CreateListModal({ isOpen, onClose, onCreate }: CreateListModalProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<{ title: string }>({
    defaultValues: { title: '' },
  });

  const onSubmit = async (data: { title: string }) => {
    setIsLoading(true);
    setError(null);
    const result = await onCreate(data);
    setIsLoading(false);

    if (result.success) {
      reset();
      onClose();
    } else {
      setError(result.error || '创建列表失败');
    }
  };

  const handleClose = () => {
    reset();
    setError(null);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="创建列表" size="sm">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        <Input
          label="列表标题"
          placeholder="例如：待办、进行中、已完成"
          error={errors.title?.message}
          {...register('title', {
            required: '请输入列表标题',
            minLength: {
              value: 1,
              message: '标题不能为空',
            },
          })}
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
