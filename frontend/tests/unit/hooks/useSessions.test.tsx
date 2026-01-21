import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useSessions } from '../../../src/hooks/useSessions';
import * as sessionsService from '../../../src/services/sessions';

vi.mock('../../../src/services/sessions');

describe('useSessions', () => {
  beforeEach(() => {
    vi.mocked(sessionsService.getSessions).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('fetches sessions on mount', async () => {
    const mockSessions = [
      { id: '1', name: 'Session 1', createdAt: new Date(), updatedAt: new Date() },
      { id: '2', name: 'Session 2', createdAt: new Date(), updatedAt: new Date() },
    ];
    vi.mocked(sessionsService.getSessions).mockResolvedValue(mockSessions);

    const { result } = renderHook(() => useSessions());

    // Initially loading
    expect(result.current.loading).toBe(true);
    expect(result.current.sessions).toEqual([]);

    // Wait for fetch to complete
    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.sessions).toEqual(mockSessions);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    const error = new Error('Failed to fetch');
    vi.mocked(sessionsService.getSessions).mockRejectedValue(error);

    const { result } = renderHook(() => useSessions());

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.sessions).toEqual([]);
    expect(result.current.error).toEqual(error);
  });

  it('provides refetch function', async () => {
    vi.mocked(sessionsService.getSessions).mockResolvedValue([]);

    const { result } = renderHook(() => useSessions());

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(sessionsService.getSessions).toHaveBeenCalledTimes(1);

    // Call refetch
    result.current.refetch();

    await waitFor(() => expect(sessionsService.getSessions).toHaveBeenCalledTimes(2));
  });
});
