import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getSessions, getSession } from '../../../src/services/sessions';
import * as api from '../../../src/services/api';

vi.mock('../../../src/services/api');

describe('sessions service', () => {
  beforeEach(() => {
    vi.mocked(api.fetchApi).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getSessions', () => {
    it('fetches and transforms sessions', async () => {
      vi.mocked(api.fetchApi).mockResolvedValue([
        {
          id: 1,
          name: 'Session 1',
          description: 'First session',
          created_at: '2024-01-15T10:00:00Z',
          updated_at: '2024-01-15T11:00:00Z',
        },
        {
          id: 2,
          name: 'Session 2',
          description: null,
          created_at: '2024-01-16T10:00:00Z',
          updated_at: '2024-01-16T11:00:00Z',
        },
      ]);

      const result = await getSessions();

      expect(api.fetchApi).toHaveBeenCalledWith('/sessions');
      expect(result).toHaveLength(2);
      expect(result[0].id).toBe('1');
      expect(result[0].name).toBe('Session 1');
      expect(result[0].description).toBe('First session');
      expect(result[1].description).toBeUndefined();
    });
  });

  describe('getSession', () => {
    it('fetches and transforms a single session', async () => {
      vi.mocked(api.fetchApi).mockResolvedValue({
        id: 1,
        name: 'Test Session',
        description: 'Description',
        created_at: '2024-01-15T10:00:00Z',
        updated_at: '2024-01-15T11:00:00Z',
      });

      const result = await getSession('1');

      expect(api.fetchApi).toHaveBeenCalledWith('/sessions/1');
      expect(result.id).toBe('1');
      expect(result.name).toBe('Test Session');
    });
  });
});
