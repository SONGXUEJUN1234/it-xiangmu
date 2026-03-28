import { apiClient } from './api';
import { AuthResponse, LoginFormData, RegisterFormData, User, ApiResponse } from '../types';

export const authService = {
  async login(data: LoginFormData) {
    // Backend expects 'username' field but can login with email
    return apiClient.post<{ access_token: string; refresh_token: string; token_type: string; expires_in: number }>('/api/auth/login', {
      username: data.email,
      password: data.password,
    });
  },

  async register(data: RegisterFormData) {
    return apiClient.post<AuthResponse>('/api/auth/register', data);
  },

  async logout() {
    return apiClient.post<ApiResponse<{ message: string }>>('/api/auth/logout');
  },

  async getCurrentUser() {
    return apiClient.get<User>('/api/auth/me');
  },

  async updateProfile(data: Partial<User>) {
    return apiClient.patch<ApiResponse<User>>('/api/auth/me', data);
  },

  async changePassword(data: { old_password: string; new_password: string }) {
    return apiClient.post<ApiResponse<{ message: string }>>('/api/users/me/change-password', data);
  },
};
