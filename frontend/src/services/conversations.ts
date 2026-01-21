// Conversations API service

import type { Conversation } from '../types';
import type { ApiConversation, ApiPaginatedResponse } from '../types/api';
import { fetchApi } from './api';
import { transformConversation } from './transforms';

export async function getConversations(sessionId: string): Promise<Conversation[]> {
  const response = await fetchApi<ApiPaginatedResponse<ApiConversation>>(`/conversations/by-session/${sessionId}`);
  return response.items.map(transformConversation);
}

export async function getConversation(id: string): Promise<Conversation> {
  const response = await fetchApi<ApiConversation>(`/conversations/${id}`);
  return transformConversation(response);
}
