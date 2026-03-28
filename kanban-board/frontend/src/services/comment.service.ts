import { apiClient } from './api';
import { Comment, CreateCommentFormData } from '../types';

export const commentService = {
  async getComments(cardId: string, params?: { page?: number; page_size?: number }) {
    const response = await apiClient.get<{ success: boolean; data: Comment[]; pagination: any }>(`/api/cards/${cardId}/comments`, params);
    return response.data || [];
  },

  async createComment(cardId: string, data: CreateCommentFormData) {
    return apiClient.post<Comment>(`/api/cards/${cardId}/comments`, {
      ...data,
      card_id: cardId,
    });
  },

  async updateComment(commentId: string, data: { content: string }) {
    return apiClient.patch<Comment>(`/api/comments/${commentId}`, data);
  },

  async deleteComment(commentId: string) {
    return apiClient.delete<{ message: string }>(`/api/comments/${commentId}`);
  },
};
