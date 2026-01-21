// Hook for fetching conversations for a session

import { useState, useEffect, useCallback } from 'react';
import type { Conversation } from '../types';
import { getConversations } from '../services';

interface UseConversationsResult {
  conversations: Conversation[];
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

export function useConversations(sessionId: string | null): UseConversationsResult {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchConversations = useCallback(async () => {
    if (!sessionId) {
      setConversations([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await getConversations(sessionId);
      setConversations(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch conversations'));
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    fetchConversations();
  }, [fetchConversations]);

  return { conversations, loading, error, refetch: fetchConversations };
}
