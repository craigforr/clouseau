import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { getExchanges, getExchange } from '../../../src/services/exchanges';
import * as api from '../../../src/services/api';

vi.mock('../../../src/services/api');

describe('exchanges service', () => {
  beforeEach(() => {
    vi.mocked(api.fetchApi).mockReset();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  describe('getExchanges', () => {
    it('fetches and transforms exchanges for a conversation from paginated response', async () => {
      vi.mocked(api.fetchApi).mockResolvedValue({
        items: [
          {
            id: 100,
            conversation_id: 10,
            user_message: 'Hello',
            assistant_message: 'Hi there',
            model: 'gpt-4',
            input_tokens: 50,
            output_tokens: 30,
            created_at: '2024-01-15T10:00:00Z',
          },
          {
            id: 101,
            conversation_id: 10,
            user_message: 'How are you?',
            assistant_message: 'I am doing well',
            model: null,
            input_tokens: null,
            output_tokens: null,
            created_at: '2024-01-15T10:01:00Z',
          },
        ],
        total: 2,
        page: 1,
        page_size: 50,
      });

      const result = await getExchanges('10');

      expect(api.fetchApi).toHaveBeenCalledWith('/exchanges/by-conversation/10');
      expect(result).toHaveLength(2);
      expect(result[0].id).toBe('100');
      expect(result[0].conversationId).toBe('10');
      expect(result[0].userMessage).toBe('Hello');
      expect(result[0].model).toBe('gpt-4');
      expect(result[1].model).toBeUndefined();
    });
  });

  describe('getExchange', () => {
    it('fetches and transforms a single exchange', async () => {
      vi.mocked(api.fetchApi).mockResolvedValue({
        id: 100,
        conversation_id: 10,
        user_message: 'Test message',
        assistant_message: 'Test response',
        model: 'gpt-4',
        input_tokens: 25,
        output_tokens: 15,
        created_at: '2024-01-15T10:00:00Z',
      });

      const result = await getExchange('100');

      expect(api.fetchApi).toHaveBeenCalledWith('/exchanges/100');
      expect(result.id).toBe('100');
      expect(result.userMessage).toBe('Test message');
    });
  });
});
