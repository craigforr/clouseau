// Hook for fetching sessions list

import { useState, useEffect, useCallback } from 'react';
import type { Session } from '../types';
import { getSessions } from '../services';

interface UseSessionsResult {
  sessions: Session[];
  loading: boolean;
  error: Error | null;
  refetch: () => void;
}

export function useSessions(): UseSessionsResult {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchSessions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getSessions();
      setSessions(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch sessions'));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  return { sessions, loading, error, refetch: fetchSessions };
}
