import { apiClient } from './api';
import { Label } from '../types';

export const labelService = {
  async createLabel(boardId: string, data: { name: string; color: string }) {
    return apiClient.post<{ data: Label }>(`/api/boards/${boardId}/labels`, data);
  },

  async updateLabel(labelId: string, data: Partial<Label>) {
    return apiClient.patch<{ data: Label }>(`/api/labels/${labelId}`, data);
  },

  async deleteLabel(labelId: string) {
    return apiClient.delete<{ message: string }>(`/api/labels/${labelId}`);
  },

  async addLabelToCard(cardId: string, labelId: string) {
    return apiClient.post<{ data: any }>(`/api/cards/${cardId}/labels`, { label_id: labelId });
  },

  async removeLabelFromCard(cardId: string, labelId: string) {
    return apiClient.delete<{ message: string }>(`/api/cards/${cardId}/labels/${labelId}`);
  },
};
