import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { X } from 'lucide-react';
import { Modal } from '../ui/Modal';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { CreateBoardFormData } from '../../types';

const BOARD_COLORS = [
  { name: '蓝色', value: '#0079BF' },
  { name: '绿色', value: '#61BD4F' },
  { name: '橙色', value: '#FF9F1A' },
  { name: '红色', value: '#EB5A46' },
  { name: '紫色', value: '#C377E0' },
  { name: '粉色', value: '#FF80CE' },
  { name: '青色', value: '#51E898' },
  { name: '灰色', value: '#838C91' },
];

interface CreateBoardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (data: CreateBoardFormData) => Promise<{ success: boolean; error?: string }>;
}

export function CreateBoardModal({ isOpen, onClose, onCreate }: CreateBoardModalProps) {
  const [selectedColor, setSelectedColor] = useState('#0079BF');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<CreateBoardFormData>({
    defaultValues: {
      title: '',
      description: '',
      background_color: '#0079BF',
    },
  });

  const onSubmit = async (data: CreateBoardFormData) => {
    setIsLoading(true);
    setError(null);
    const result = await onCreate({ ...data, background_color: selectedColor });
    setIsLoading(false);

    if (result.success) {
      reset();
      setSelectedColor('#0079BF');
      onClose();
    } else {
      setError(result.error || '创建看板失败');
    }
  };

  const handleClose = () => {
    reset();
    setSelectedColor('#0079BF');
    setError(null);
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="创建新看板" size="sm">
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        <Input
          label="看板标题"
          placeholder="例如：产品开发看板"
          error={errors.title?.message}
          {...register('title', {
            required: '请输入看板标题',
            minLength: {
              value: 2,
              message: '标题至少2个字符',
            },
          })}
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            背景颜色
          </label>
          <div className="flex flex-wrap gap-2">
            {BOARD_COLORS.map((color) => (
              <button
                key={color.value}
                type="button"
                onClick={() => setSelectedColor(color.value)}
                className={`w-10 h-10 rounded-lg transition-transform ${
                  selectedColor === color.value ? 'ring-2 ring-offset-2 ring-primary-500 scale-110' : ''
                }`}
                style={{ backgroundColor: color.value }}
                title={color.name}
              />
            ))}
          </div>
        </div>

        <div className="h-20 rounded-lg" style={{ backgroundColor: selectedColor }} />

        <Input
          label="描述（可选）"
          placeholder="简要描述这个看板的用途"
          {...register('description')}
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
