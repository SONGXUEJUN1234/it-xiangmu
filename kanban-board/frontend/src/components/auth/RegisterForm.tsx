import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { UserPlus, Mail, Lock, User, AlertCircle } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { RegisterFormData } from '../../types';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

interface RegisterFormWithConfirm extends RegisterFormData {
  confirmPassword: string;
}

export function RegisterForm() {
  const navigate = useNavigate();
  const { register: registerUser, isLoading } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormWithConfirm>({
    defaultValues: {
      email: '',
      username: '',
      full_name: '',
      password: '',
      confirmPassword: '',
    },
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormWithConfirm) => {
    setError(null);
    const { confirmPassword, ...registerData } = data;
    const result = await registerUser(registerData);
    if (!result.success) {
      setError(result.error || '注册失败');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-blue-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-2xl mb-4">
              <UserPlus className="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">创建账号</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">加入任务看板系统</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
              <span className="text-sm text-red-800 dark:text-red-300">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              label="用户名"
              placeholder="johndoe"
              leftIcon={<User className="w-5 h-5 text-gray-400" />}
              error={errors.username?.message}
              {...register('username', {
                required: '请输入用户名',
                minLength: {
                  value: 3,
                  message: '用户名至少3位',
                },
                pattern: {
                  value: /^[a-zA-Z0-9_]+$/,
                  message: '用户名只能包含字母、数字和下划线',
                },
              })}
            />

            <Input
              label="姓名"
              placeholder="John Doe"
              error={errors.full_name?.message}
              {...register('full_name', {
                required: '请输入姓名',
              })}
            />

            <Input
              label="邮箱"
              type="email"
              placeholder="your@email.com"
              leftIcon={<Mail className="w-5 h-5 text-gray-400" />}
              error={errors.email?.message}
              {...register('email', {
                required: '请输入邮箱',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: '邮箱格式不正确',
                },
              })}
            />

            <Input
              label="密码"
              type="password"
              placeholder="••••••••"
              leftIcon={<Lock className="w-5 h-5 text-gray-400" />}
              error={errors.password?.message}
              {...register('password', {
                required: '请输入密码',
                minLength: {
                  value: 8,
                  message: '密码至少8位',
                },
              })}
            />

            <Input
              label="确认密码"
              type="password"
              placeholder="••••••••"
              leftIcon={<Lock className="w-5 h-5 text-gray-400" />}
              error={errors.confirmPassword?.message}
              {...register('confirmPassword', {
                required: '请确认密码',
                validate: (value) => value === password || '两次密码不一致',
              })}
            />

            <Button type="submit" className="w-full" isLoading={isLoading}>
              注册
            </Button>
          </form>

          <div className="mt-6 text-center">
            <span className="text-gray-600 dark:text-gray-400">已有账号? </span>
            <Link to="/login" className="text-primary-600 hover:text-primary-700 font-medium">
              立即登录
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
