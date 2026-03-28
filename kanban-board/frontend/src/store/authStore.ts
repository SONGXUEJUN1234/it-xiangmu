import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { User, AuthTokens } from '../types';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  initialized: boolean;
  setAuth: (user: User, tokens: AuthTokens) => void;
  setUser: (user: User) => void;
  setTokens: (tokens: AuthTokens) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      initialized: true,
      get isAuthenticated() {
        return get().user !== null;
      },
      setAuth: (user, tokens) => {
        localStorage.setItem('access_token', tokens.access.token);
        localStorage.setItem('refresh_token', tokens.refresh.token);
        set({
          user,
          accessToken: tokens.access.token,
          refreshToken: tokens.refresh.token,
        });
      },
      setUser: (user) => set({ user }),
      setTokens: (tokens) => {
        localStorage.setItem('access_token', tokens.access.token);
        localStorage.setItem('refresh_token', tokens.refresh.token);
        set({
          accessToken: tokens.access.token,
          refreshToken: tokens.refresh.token,
        });
      },
      logout: () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
        });
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({ user: state.user }),
    }
  )
);
