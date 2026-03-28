import { apiClient } from './api';
import { List, CreateListFormData } from '../types';

export const listService = {
  async createList(boardId: string, data: CreateListFormData) {
    // Backend expects board_id in the request body
    return apiClient.post<List>('/api/lists', { ...data, board_id: boardId });
  },

  async updateList(listId: string, data: Partial<List>) {
    return apiClient.patch<List>(`/api/lists/${listId}`, data);
  },

  async deleteList(listId: string, moveToListId?: string) {
    const params = moveToListId ? { move_cards_to: moveToListId } : {};
    return apiClient.delete<{ message: string }>(`/api/lists/${listId}`, params);
  },
};
