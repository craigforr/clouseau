// Exchanges API service

import type { Exchange } from '../types';
import type { ApiExchange, ApiPaginatedResponse } from '../types/api';
import { fetchApi } from './api';
import { transformExchange } from './transforms';

export async function getExchanges(conversationId: string): Promise<Exchange[]> {
  const response = await fetchApi<ApiPaginatedResponse<ApiExchange>>(`/exchanges/by-conversation/${conversationId}`);
  return response.items.map(transformExchange);
}

export async function getExchange(id: string): Promise<Exchange> {
  const response = await fetchApi<ApiExchange>(`/exchanges/${id}`);
  return transformExchange(response);
}
