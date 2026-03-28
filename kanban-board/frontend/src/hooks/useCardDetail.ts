import { useState, useEffect, useRef } from 'react';
import { cardService } from '../services/card.service';
import { commentService } from '../services/comment.service';
import { Card, Comment, CreateCommentFormData } from '../types';

export function useCardDetail(cardId: string) {
  const [card, setCard] = useState<Card | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const cardIdRef = useRef(cardId);
  cardIdRef.current = cardId;

  useEffect(() => {
    if (!cardId) return;

    let isMounted = true;

    const fetchData = async () => {
      setIsLoading(true);
      setError(null);
      try {
        const [cardResponse, commentsResponse] = await Promise.all([
          cardService.getCard(cardId),
          commentService.getComments(cardId),
        ]);
        if (isMounted) {
          setCard(cardResponse);
          setComments(commentsResponse || []);
        }
      } catch (err: any) {
        if (isMounted) {
          const errorMessage = err.response?.data?.error?.message || '获取卡片详情失败';
          setError(errorMessage);
        }
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    };

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [cardId]);

  const updateCard = async (data: Partial<Card>) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await cardService.updateCard(cardIdRef.current, data);
      setCard(response);
      return { success: true, card: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '更新卡片失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const createComment = async (data: CreateCommentFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await commentService.createComment(cardIdRef.current, data);
      setComments((prev) => [...prev, response]);
      return { success: true, comment: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '创建评论失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const updateComment = async (commentId: string, content: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await commentService.updateComment(commentId, { content });
      setComments((prev) => prev.map((comment) =>
        comment.id === commentId ? response : comment
      ));
      return { success: true, comment: response };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '更新评论失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  const deleteComment = async (commentId: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await commentService.deleteComment(commentId);
      setComments((prev) => prev.filter((comment) => comment.id !== commentId));
      return { success: true };
    } catch (err: any) {
      const errorMessage = err.response?.data?.error?.message || '删除评论失败';
      setError(errorMessage);
      return { success: false, error: errorMessage };
    } finally {
      setIsLoading(false);
    }
  };

  return {
    card,
    comments,
    isLoading,
    error,
    updateCard,
    createComment,
    updateComment,
    deleteComment,
  };
}
