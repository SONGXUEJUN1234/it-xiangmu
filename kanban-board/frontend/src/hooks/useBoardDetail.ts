import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { boardService } from '../services/board.service';
import { listService } from '../services/list.service';
import { cardService } from '../services/card.service';
import { useBoardStore } from '../store/boardStore';
import { Board, List, Card, CreateListFormData, CreateCardFormData } from '../types';

export function useBoardDetail() {
  const { boardId } = useParams<{ boardId: string }>();
  const navigate = useNavigate();
  const {
    currentBoard,
    lists,
    isLoading,
    error,
    setCurrentBoard,
    setLists,
    addList,
    removeList,
    addCard,
    removeCard,
    moveCard,
    setLoading,
    setError,
  } = useBoardStore();

  const boardIdRef = useRef(boardId);
  boardIdRef.current = boardId;

  useEffect(() => {
    if (!boardId) return;

    let isMounted = true;

    const fetchData = async () => {
      console.log('[useBoardDetail] Starting fetch for boardId:', boardId);
      setLoading(true);
      setError(null);
      try {
        const response = await boardService.getBoard(boardId);
        console.log('[useBoardDetail] Got response:', response);
        if (isMounted) {
          console.log('[useBoardDetail] Setting current board and lists');
          setCurrentBoard(response);
          setLists(response.lists || []);
          console.log('[useBoardDetail] Done setting state');
        }
      } catch (err: any) {
        console.error('[useBoardDetail] Error:', err);
        if (isMounted) {
          const errorMessage = err.response?.data?.error?.message || '获取看板详情失败';
          setError(errorMessage);
          if (err.response?.status === 404) {
            navigate('/boards');
          }
        }
      } finally {
        console.log('[useBoardDetail] Finally block, isMounted:', isMounted);
        if (isMounted) {
          setLoading(false);
          console.log('[useBoardDetail] Set loading to false');
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [boardId]); // Only re-fetch when boardId changes

  const createList = async (data: CreateListFormData) => {
    if (!boardIdRef.current) return { success: false, error: '看板ID不存在' };

    setLoading(true);
    setError(null);
    try {
      const response = await listService.createList(boardIdRef.current, data);
      addList(response);
      return { success: true, list: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '创建列表失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const updateList = async (listId: string, data: Partial<List>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await listService.updateList(listId, data);
      setLists(lists.map((list) =>
        list.id === listId ? response : list
      ));
      return { success: true, list: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '更新列表失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const deleteList = async (listId: string, moveToListId?: string) => {
    setLoading(true);
    setError(null);
    try {
      await listService.deleteList(listId, moveToListId);
      removeList(listId);
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '删除列表失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const createCard = async (listId: string, data: CreateCardFormData) => {
    setLoading(true);
    setError(null);
    try {
      const response = await cardService.createCard(listId, data);
      addCard(listId, response);
      return { success: true, card: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '创建卡片失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const updateCard = async (cardId: string, data: Partial<Card>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await cardService.updateCard(cardId, data);
      return { success: true, card: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '更新卡片失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const deleteCard = async (cardId: string, listId: string) => {
    setLoading(true);
    setError(null);
    try {
      await cardService.deleteCard(cardId);
      removeCard(cardId, listId);
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '删除卡片失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setLoading(false);
    }
  };

  const handleMoveCard = async (cardId: string, listId: string, position: number) => {
    try {
      await cardService.moveCard(cardId, { list_id: listId, position });
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '移动卡片失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    }
  };

  const fetchBoard = async () => {
    if (boardIdRef.current) {
      setLoading(true);
      setError(null);
      try {
        const response = await boardService.getBoard(boardIdRef.current);
        setCurrentBoard(response);
        setLists(response.lists || []);
      } catch (err: any) {
        const errorMessage = err.response?.data?.error?.message || '获取看板详情失败';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    }
  };

  return {
    board: currentBoard,
    lists,
    isLoading,
    error,
    fetchBoard,
    createList,
    updateList,
    deleteList,
    createCard,
    updateCard,
    deleteCard,
    moveCard: handleMoveCard,
  };
}
