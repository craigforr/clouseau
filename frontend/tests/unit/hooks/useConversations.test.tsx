import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useConversations } from '../../../src/hooks/useConversations';
import * as conversationsService from '../../../src/services/conversations';

vi.mock('../../../src/services/conversations');

describe('useConversations', () => {
  beforeEach(() => {
    vi.mocked(conversationsService.getConversations).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns empty when no sessionId', async () => {
    const { result } = renderHook(() => useConversations(null));

    expect(result.current.loading).toBe(false);
    expect(result.current.conversations).toEqual([]);
    expect(conversationsService.getConversations).not.toHaveBeenCalled();
  });

  it('fetches conversations when sessionId provided', async () => {
    const mockConversations = [
      { id: '10', sessionId: '1', title: 'Conv 1', createdAt: new Date(), updatedAt: new Date() },
      { id: '11', sessionId: '1', title: 'Conv 2', createdAt: new Date(), updatedAt: new Date() },
    ];
    vi.mocked(conversationsService.getConversations).mockResolvedValue(mockConversations);

    const { result } = renderHook(() => useConversations('1'));

    expect(result.current.loading).toBe(true);

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(conversationsService.getConversations).toHaveBeenCalledWith('1');
    expect(result.current.conversations).toEqual(mockConversations);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    const error = new Error('Failed to fetch');
    vi.mocked(conversationsService.getConversations).mockRejectedValue(error);

    const { result } = renderHook(() => useConversations('1'));

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.conversations).toEqual([]);
    expect(result.current.error).toEqual(error);
  });

  it('refetches when sessionId changes', async () => {
    vi.mocked(conversationsService.getConversations).mockResolvedValue([]);

    const { result, rerender } = renderHook(
      ({ sessionId }: { sessionId: string }) => useConversations(sessionId),
      { initialProps: { sessionId: '1' } }
    );

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(conversationsService.getConversations).toHaveBeenCalledWith('1');

    rerender({ sessionId: '2' });

    await waitFor(() => expect(conversationsService.getConversations).toHaveBeenCalledWith('2'));
  });
});
