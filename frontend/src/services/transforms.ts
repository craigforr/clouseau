// Transform functions to convert backend API responses to frontend types

import type { ApiSession, ApiConversation, ApiExchange } from '../types/api';
import type { Session, Conversation, Exchange } from '../types';

export function transformSession(api: ApiSession): Session {
  return {
    id: String(api.id),
    name: api.name,
    description: api.description ?? undefined,
    createdAt: new Date(api.created_at),
    updatedAt: new Date(api.updated_at),
  };
}

export function transformConversation(api: ApiConversation): Conversation {
  return {
    id: String(api.id),
    sessionId: String(api.session_id),
    title: api.title,
    createdAt: new Date(api.created_at),
    updatedAt: new Date(api.updated_at),
  };
}

export function transformExchange(api: ApiExchange): Exchange {
  return {
    id: String(api.id),
    conversationId: String(api.conversation_id),
    userMessage: api.user_message,
    assistantMessage: api.assistant_message,
    model: api.model ?? undefined,
    inputTokens: api.input_tokens ?? undefined,
    outputTokens: api.output_tokens ?? undefined,
    createdAt: new Date(api.created_at),
  };
}
