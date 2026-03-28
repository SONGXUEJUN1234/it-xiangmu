import { create } from 'zustand';
import { Board, List, Card } from '../types';

interface BoardState {
  currentBoard: Board | null;
  lists: List[];
  isLoading: boolean;
  error: string | null;
  setCurrentBoard: (board: Board | null) => void;
  setLists: (lists: List[]) => void;
  updateList: (listId: string, updates: Partial<List>) => void;
  addList: (list: List) => void;
  removeList: (listId: string) => void;
  updateCard: (cardId: string, updates: Partial<Card>) => void;
  moveCard: (cardId: string, fromListId: string, toListId: string, newPosition: number) => void;
  addCard: (listId: string, card: Card) => void;
  removeCard: (cardId: string, listId: string) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useBoardStore = create<BoardState>((set) => ({
  currentBoard: null,
  lists: [],
  isLoading: false,
  error: null,

  setCurrentBoard: (board) => set({ currentBoard: board }),

  setLists: (lists) => set({ lists }),

  updateList: (listId, updates) =>
    set((state) => ({
      lists: state.lists.map((list) =>
        list.id === listId ? { ...list, ...updates } : list
      ),
    })),

  addList: (list) =>
    set((state) => ({
      lists: [...state.lists, list].sort((a, b) => a.position - b.position),
    })),

  removeList: (listId) =>
    set((state) => ({
      lists: state.lists.filter((list) => list.id !== listId),
    })),

  updateCard: (cardId, updates) =>
    set((state) => ({
      lists: state.lists.map((list) => ({
        ...list,
        cards: list.cards?.map((card) =>
          card.id === cardId ? { ...card, ...updates } : card
        ),
      })),
    })),

  moveCard: (cardId, fromListId, toListId, newPosition) =>
    set((state) => {
      let cardToMove: Card | null = null;

      const newLists = state.lists.map((list) => {
        if (list.id === fromListId) {
          const filteredCards = list.cards?.filter((card) => card.id !== cardId) || [];
          if (list.id === toListId) {
            cardToMove = list.cards?.find((card) => card.id === cardId) || null;
            const updatedCards = [...filteredCards];
            if (cardToMove) {
              updatedCards.splice(newPosition, 0, cardToMove);
            }
            return { ...list, cards: updatedCards };
          }
          return { ...list, cards: filteredCards };
        } else if (list.id === toListId) {
          const fromList = state.lists.find((l) => l.id === fromListId);
          cardToMove = fromList?.cards?.find((card) => card.id === cardId) || null;
          const updatedCards = [...(list.cards || [])];
          if (cardToMove) {
            updatedCards.splice(newPosition, 0, { ...cardToMove, list_id: toListId });
          }
          return { ...list, cards: updatedCards };
        }
        return list;
      });

      return { lists: newLists };
    }),

  addCard: (listId, card) =>
    set((state) => ({
      lists: state.lists.map((list) =>
        list.id === listId
          ? { ...list, cards: [...(list.cards || []), card] }
          : list
      ),
    })),

  removeCard: (cardId, listId) =>
    set((state) => ({
      lists: state.lists.map((list) =>
        list.id === listId
          ? { ...list, cards: list.cards?.filter((card) => card.id !== cardId) || [] }
          : list
      ),
    })),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),
}));
