// Backend API response types (snake_case, integer IDs)

export interface ApiSession {
  id: number;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface ApiConversation {
  id: number;
  session_id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ApiExchange {
  id: number;
  conversation_id: number;
  user_message: string;
  assistant_message: string;
  model: string | null;
  input_tokens: number | null;
  output_tokens: number | null;
  created_at: string;
}

// Paginated response wrapper
export interface ApiPaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}
