// Conversations API service

import type { Conversation } from '../types';
import type { ApiConversation } from '../types/api';
import { fetchApi } from './api';
import { transformConversation } from './transforms';

export async function getConversations(sessionId: string): Promise<Conversation[]> {
  const response = await fetchApi<ApiConversation[]>(`/sessions/${sessionId}/conversations`);
  return response.map(transformConversation);
}

export async function getConversation(id: string): Promise<Conversation> {
  const response = await fetchApi<ApiConversation>(`/conversations/${id}`);
  return transformConversation(response);
}
