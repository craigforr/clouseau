// Type definitions for Clouseau frontend

export interface Session {
  id: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
}

export interface Conversation {
  id: string;
  sessionId: string;
  title: string;
  createdAt: Date;
}

export interface Exchange {
  id: string;
  conversationId: string;
  userMessage: string;
  assistantMessage: string;
  createdAt: Date;
}
