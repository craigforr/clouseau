// Hook for fetching exchanges for a conversation

import { useState, useEffect, useCallback } from 'react';
import type { Exchange } from '../types';
import { getExchanges } from '../services';

interface UseExchangesResult {
  exchanges: Exchange[];
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

export function useExchanges(conversationId: string | null): UseExchangesResult {
  const [exchanges, setExchanges] = useState<Exchange[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchExchanges = useCallback(async () => {
    if (!conversationId) {
      setExchanges([]);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = await getExchanges(conversationId);
      setExchanges(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch exchanges'));
    } finally {
      setLoading(false);
    }
  }, [conversationId]);

  useEffect(() => {
    fetchExchanges();
  }, [fetchExchanges]);

  return { exchanges, loading, error, refetch: fetchExchanges };
}
