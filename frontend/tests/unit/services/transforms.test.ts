import { describe, it, expect } from 'vitest';
import {
  transformSession,
  transformConversation,
  transformExchange,
} from '../../../src/services/transforms';
import type { ApiSession, ApiConversation, ApiExchange } from '../../../src/types/api';

describe('transformSession', () => {
  it('transforms API session to frontend session', () => {
    const apiSession: ApiSession = {
      id: 1,
      name: 'Test Session',
      description: 'A test session',
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-16T14:45:00Z',
    };

    const result = transformSession(apiSession);

    expect(result).toEqual({
      id: '1',
      name: 'Test Session',
      description: 'A test session',
      createdAt: new Date('2024-01-15T10:30:00Z'),
      updatedAt: new Date('2024-01-16T14:45:00Z'),
    });
  });

  it('transforms null description to undefined', () => {
    const apiSession: ApiSession = {
      id: 2,
      name: 'No Description',
      description: null,
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-16T14:45:00Z',
    };

    const result = transformSession(apiSession);

    expect(result.description).toBeUndefined();
  });
});

describe('transformConversation', () => {
  it('transforms API conversation to frontend conversation', () => {
    const apiConversation: ApiConversation = {
      id: 10,
      session_id: 1,
      title: 'Test Conversation',
      created_at: '2024-01-15T11:00:00Z',
      updated_at: '2024-01-15T12:00:00Z',
    };

    const result = transformConversation(apiConversation);

    expect(result).toEqual({
      id: '10',
      sessionId: '1',
      title: 'Test Conversation',
      createdAt: new Date('2024-01-15T11:00:00Z'),
      updatedAt: new Date('2024-01-15T12:00:00Z'),
    });
  });
});

describe('transformExchange', () => {
  it('transforms API exchange to frontend exchange with all fields', () => {
    const apiExchange: ApiExchange = {
      id: 100,
      conversation_id: 10,
      user_message: 'Hello, world!',
      assistant_message: 'Hi there!',
      model: 'gpt-4',
      input_tokens: 50,
      output_tokens: 25,
      created_at: '2024-01-15T11:30:00Z',
    };

    const result = transformExchange(apiExchange);

    expect(result).toEqual({
      id: '100',
      conversationId: '10',
      userMessage: 'Hello, world!',
      assistantMessage: 'Hi there!',
      model: 'gpt-4',
      inputTokens: 50,
      outputTokens: 25,
      createdAt: new Date('2024-01-15T11:30:00Z'),
    });
  });

  it('transforms null optional fields to undefined', () => {
    const apiExchange: ApiExchange = {
      id: 101,
      conversation_id: 10,
      user_message: 'Test',
      assistant_message: 'Response',
      model: null,
      input_tokens: null,
      output_tokens: null,
      created_at: '2024-01-15T11:30:00Z',
    };

    const result = transformExchange(apiExchange);

    expect(result.model).toBeUndefined();
    expect(result.inputTokens).toBeUndefined();
    expect(result.outputTokens).toBeUndefined();
  });
});
