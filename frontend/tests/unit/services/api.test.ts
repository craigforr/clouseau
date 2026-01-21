import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchApi, ApiError } from '../../../src/services/api';

describe('fetchApi', () => {
  const mockFetch = vi.fn();

  beforeEach(() => {
    vi.stubGlobal('fetch', mockFetch);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    mockFetch.mockReset();
  });

  it('fetches data successfully', async () => {
    const mockData = { id: 1, name: 'Test' };
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve(mockData),
    });

    const result = await fetchApi('/test');

    expect(mockFetch).toHaveBeenCalledWith('/api/test', {
      headers: { 'Content-Type': 'application/json' },
    });
    expect(result).toEqual(mockData);
  });

  it('throws ApiError on non-ok response', async () => {
    mockFetch.mockResolvedValue({
      ok: false,
      status: 404,
      statusText: 'Not Found',
    });

    await expect(fetchApi('/missing')).rejects.toThrow(ApiError);
    await expect(fetchApi('/missing')).rejects.toMatchObject({
      status: 404,
      statusText: 'Not Found',
    });
  });

  it('passes custom options', async () => {
    mockFetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });

    await fetchApi('/test', {
      method: 'POST',
      body: JSON.stringify({ data: 'test' }),
    });

    expect(mockFetch).toHaveBeenCalledWith('/api/test', {
      method: 'POST',
      body: JSON.stringify({ data: 'test' }),
      headers: { 'Content-Type': 'application/json' },
    });
  });
});

describe('ApiError', () => {
  it('has correct properties', () => {
    const error = new ApiError('Test error', 500, 'Internal Server Error');

    expect(error.message).toBe('Test error');
    expect(error.status).toBe(500);
    expect(error.statusText).toBe('Internal Server Error');
    expect(error.name).toBe('ApiError');
  });
});
