import { useState, useEffect, useRef } from 'react';
import { boardService } from '../services/board.service';
import { Board } from '../types';

export function useBoards(params?: { page?: number; page_size?: number; archived?: boolean }) {
  const [boards, setBoards] = useState<Board[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [pagination, setPagination] = useState({
    page: 1,
    page_size: 20,
    total: 0,
    total_pages: 0,
  });

  const hasFetched = useRef(false);

  useEffect(() => {
    // Prevent duplicate calls
    if (hasFetched.current) {
      return;
    }
    hasFetched.current = true;

    let isMounted = true;

    const fetchBoards = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const response = await boardService.getBoards(params);
        if (isMounted) {
          setBoards(response.data);
          setPagination(response.pagination);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.response?.data?.error?.message || '获取看板列表失败');
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchBoards();

    return () => {
      isMounted = false;
    };
  }, []); // Empty deps - only run once on mount

  const createBoard = async (data: { title: string; description: string; background_color: string }) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await boardService.createBoard(data);
      setBoards((prev) => [response.data, ...prev]);
      return { success: true, board: response.data };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '创建看板失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const deleteBoard = async (boardId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await boardService.deleteBoard(boardId);
      setBoards((prev) => prev.filter((board) => board.id !== boardId));
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '删除看板失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const archiveBoard = async (boardId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await boardService.archiveBoard(boardId);
      setBoards((prev) => prev.map((board) =>
        board.id === boardId ? { ...board, is_archived: true } : board
      ));
      return { success: true, board: response.data };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '归档看板失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    boards,
    isLoading,
    error,
    pagination,
    createBoard,
    deleteBoard,
    archiveBoard,
  };
}
