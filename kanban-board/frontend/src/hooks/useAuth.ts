import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/auth.service';
import { useAuthStore } from '../store/authStore';
import { LoginFormData, RegisterFormData } from '../types';

export function useAuth() {
  const navigate = useNavigate();
  const { user, isAuthenticated, setAuth, logout: logoutStore } = useAuthStore();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = useCallback(async (data: LoginFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.login(data);
      // Store tokens first so getCurrentUser can use them
      const tokens = {
        access: { token: response.access_token, expires_in: response.expires_in },
        refresh: { token: response.refresh_token, expires_in: 604800 }, // 7 days
      };
      // Store tokens in localStorage immediately
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      // Now get user info with the token
      const userResponse = await authService.getCurrentUser();
      // Update auth store with user data
      setAuth(userResponse, tokens);
      navigate('/boards');
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '登录失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, [navigate, setAuth]);

  const register = useCallback(async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await authService.register(data);
      const tokens = {
        access: { token: response.access_token, expires_in: response.expires_in },
        refresh: { token: response.refresh_token, expires_in: 604800 },
      };
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('refresh_token', response.refresh_token);
      setAuth(response.user, tokens);
      navigate('/boards');
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '注册失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  }, [navigate, setAuth]);

  const logout = useCallback(async () => {
    try {
      await authService.logout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      logoutStore();
      navigate('/login');
    }
  }, [navigate, logoutStore]);

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
  };
}
