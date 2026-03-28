import { apiClient } from './api';
import { Board, CreateBoardFormData, PaginatedResponse } from '../types';

export const boardService = {
  async getBoards(params?: { page?: number; page_size?: number; archived?: boolean }) {
    return apiClient.get<PaginatedResponse<Board>>('/api/boards', params);
  },

  async getBoard(boardId: string) {
    return apiClient.get<Board>(`/api/boards/${boardId}`);
  },

  async createBoard(data: CreateBoardFormData) {
    return apiClient.post<{ data: Board }>('/api/boards', data);
  },

  async updateBoard(boardId: string, data: Partial<Board>) {
    return apiClient.patch<{ data: Board }>(`/api/boards/${boardId}`, data);
  },

  async deleteBoard(boardId: string) {
    return apiClient.delete<{ message: string }>(`/api/boards/${boardId}`);
  },

  async archiveBoard(boardId: string) {
    return apiClient.post<{ data: Board }>(`/api/boards/${boardId}/archive`);
  },

  async unarchiveBoard(boardId: string) {
    return apiClient.post<{ data: Board }>(`/api/boards/${boardId}/unarchive`);
  },

  async addMember(boardId: string, data: { username: string; role: string }) {
    return apiClient.post<{ data: any }>(`/api/boards/${boardId}/members`, data);
  },

  async updateMember(boardId: string, userId: string, data: { role: string }) {
    return apiClient.patch<{ data: any }>(`/api/boards/${boardId}/members/${userId}`, data);
  },

  async removeMember(boardId: string, userId: string) {
    return apiClient.delete<{ message: string }>(`/api/boards/${boardId}/members/${userId}`);
  },

  async getActivities(boardId: string, params?: { page?: number; page_size?: number }) {
    return apiClient.get<any>(`/api/boards/${boardId}/activities`, params);
  },
};
