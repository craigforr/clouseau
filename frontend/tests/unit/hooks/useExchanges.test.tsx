import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useExchanges } from '../../../src/hooks/useExchanges';
import * as exchangesService from '../../../src/services/exchanges';

vi.mock('../../../src/services/exchanges');

describe('useExchanges', () => {
  beforeEach(() => {
    vi.mocked(exchangesService.getExchanges).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('returns empty when no conversationId', async () => {
    const { result } = renderHook(() => useExchanges(null));

    expect(result.current.loading).toBe(false);
    expect(result.current.exchanges).toEqual([]);
    expect(exchangesService.getExchanges).not.toHaveBeenCalled();
  });

  it('fetches exchanges when conversationId provided', async () => {
    const mockExchanges = [
      {
        id: '100',
        conversationId: '10',
        userMessage: 'Hello',
        assistantMessage: 'Hi',
        createdAt: new Date(),
      },
    ];
    vi.mocked(exchangesService.getExchanges).mockResolvedValue(mockExchanges);

    const { result } = renderHook(() => useExchanges('10'));

    expect(result.current.loading).toBe(true);

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(exchangesService.getExchanges).toHaveBeenCalledWith('10');
    expect(result.current.exchanges).toEqual(mockExchanges);
    expect(result.current.error).toBeNull();
  });

  it('handles fetch error', async () => {
    const error = new Error('Failed to fetch');
    vi.mocked(exchangesService.getExchanges).mockRejectedValue(error);

    const { result } = renderHook(() => useExchanges('10'));

    await waitFor(() => expect(result.current.loading).toBe(false));

    expect(result.current.exchanges).toEqual([]);
    expect(result.current.error).toEqual(error);
  });

  it('refetches when conversationId changes', async () => {
    vi.mocked(exchangesService.getExchanges).mockResolvedValue([]);

    const { result, rerender } = renderHook(
      ({ conversationId }: { conversationId: string }) => useExchanges(conversationId),
      { initialProps: { conversationId: '10' } }
    );

    await waitFor(() => expect(result.current.loading).toBe(false));
    expect(exchangesService.getExchanges).toHaveBeenCalledWith('10');

    rerender({ conversationId: '11' });

    await waitFor(() => expect(exchangesService.getExchanges).toHaveBeenCalledWith('11'));
  });
});
