import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  cardModalOpen: boolean;
  selectedCardId: string | null;
  selectedListId: string | null;
  theme: 'light' | 'dark';
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  openCardModal: (cardId: string, listId: string) => void;
  closeCardModal: () => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  cardModalOpen: false,
  selectedCardId: null,
  selectedListId: null,
  theme: 'light',

  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),

  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  openCardModal: (cardId, listId) =>
    set({
      cardModalOpen: true,
      selectedCardId: cardId,
      selectedListId: listId,
    }),

  closeCardModal: () =>
    set({
      cardModalOpen: false,
      selectedCardId: null,
      selectedListId: null,
    }),

  setTheme: (theme) => set({ theme }),
}));
