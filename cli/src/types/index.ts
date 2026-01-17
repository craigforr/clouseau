// CLI type definitions

export interface CLIConfig {
  apiUrl: string;
  theme: 'light' | 'dark' | 'auto';
}

export interface ChatState {
  sessionId: string;
  conversationId: string;
  messages: Message[];
}

export interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}
