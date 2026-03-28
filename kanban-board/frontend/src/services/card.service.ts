import { apiClient } from './api';
import { Card, CreateCardFormData } from '../types';

export const cardService = {
  async createCard(listId: string, data: CreateCardFormData) {
    return apiClient.post<Card>(`/api/cards/lists/${listId}/cards`, { ...data, list_id: listId });
  },

  async getCard(cardId: string) {
    return apiClient.get<Card>(`/api/cards/${cardId}`);
  },

  async updateCard(cardId: string, data: Partial<Card>) {
    return apiClient.patch<Card>(`/api/cards/${cardId}`, data);
  },

  async moveCard(cardId: string, data: { list_id: string; position: number }) {
    return apiClient.post<Card>(`/api/cards/${cardId}/move`, data);
  },

  async deleteCard(cardId: string) {
    return apiClient.delete<{ message: string }>(`/api/cards/${cardId}`);
  },

  async searchCards(boardId: string, params: any) {
    return apiClient.get<Card[]>(`/api/cards/boards/${boardId}/cards/search`, params);
  },
};
