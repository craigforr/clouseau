// Type definitions for Clouseau frontend

export interface Session {
  id: string;
  name: string;
  description?: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Conversation {
  id: string;
  sessionId: string;
  title: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Exchange {
  id: string;
  conversationId: string;
  userMessage: string;
  assistantMessage: string;
  model?: string;
  inputTokens?: number;
  outputTokens?: number;
  createdAt: Date;
}
