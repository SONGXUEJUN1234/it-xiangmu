import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { LogIn, Mail, Lock, AlertCircle } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';
import { LoginFormData } from '../../types';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';

export function LoginForm() {
  const navigate = useNavigate();
  const { login, isLoading } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginFormData) => {
    setError(null);
    const result = await login(data);
    if (!result.success) {
      setError(result.error || '登录失败');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-blue-100 dark:from-gray-900 dark:to-gray-800 px-4">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-2xl mb-4">
              <LogIn className="w-8 h-8 text-primary-600 dark:text-primary-400" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white">欢迎回来</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-2">登录到任务看板系统</p>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-center gap-3">
              <AlertCircle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0" />
              <span className="text-sm text-red-800 dark:text-red-300">{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
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
                  value: 6,
                  message: '密码至少6位',
                },
              })}
            />

            <div className="flex items-center justify-between">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                />
                <span className="ml-2 text-sm text-gray-600 dark:text-gray-400">记住我</span>
              </label>
              <Link to="/forgot-password" className="text-sm text-primary-600 hover:text-primary-700">
                忘记密码?
              </Link>
            </div>

            <Button type="submit" className="w-full" isLoading={isLoading}>
              登录
            </Button>
          </form>

          <div className="mt-6 text-center">
            <span className="text-gray-600 dark:text-gray-400">还没有账号? </span>
            <Link to="/register" className="text-primary-600 hover:text-primary-700 font-medium">
              立即注册
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
