import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getConversations, getConversation } from '../../../src/services/conversations';
import * as api from '../../../src/services/api';

vi.mock('../../../src/services/api');

describe('conversations service', () => {
  beforeEach(() => {
    vi.mocked(api.fetchApi).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getConversations', () => {
    it('fetches and transforms conversations for a session from paginated response', async () => {
      vi.mocked(api.fetchApi).mockResolvedValue({
        items: [
          {
            id: 10,
            session_id: 1,
            title: 'Conversation 1',
            created_at: '2024-01-15T10:00:00Z',
            updated_at: '2024-01-15T11:00:00Z',
          },
          {
            id: 11,
            session_id: 1,
            title: 'Conversation 2',
            created_at: '2024-01-16T10:00:00Z',
            updated_at: '2024-01-16T11:00:00Z',
          },
        ],
        total: 2,
        page: 1,
        page_size: 20,
      });

      const result = await getConversations('1');

      expect(api.fetchApi).toHaveBeenCalledWith('/conversations/by-session/1');
      expect(result).toHaveLength(2);
      expect(result[0].id).toBe('10');
      expect(result[0].sessionId).toBe('1');
      expect(result[0].title).toBe('Conversation 1');
    });
  });

  describe('getConversation', () => {
    it('fetches and transforms a single conversation', async () => {
      vi.mocked(api.fetchApi).mockResolvedValue({
        id: 10,
        session_id: 1,
        title: 'Test Conversation',
        created_at: '2024-01-15T10:00:00Z',
        updated_at: '2024-01-15T11:00:00Z',
      });

      const result = await getConversation('10');

      expect(api.fetchApi).toHaveBeenCalledWith('/conversations/10');
      expect(result.id).toBe('10');
      expect(result.title).toBe('Test Conversation');
    });
  });
});
