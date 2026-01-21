// Sessions API service

import type { Session } from '../types';
import type { ApiSession } from '../types/api';
import { fetchApi } from './api';
import { transformSession } from './transforms';

export async function getSessions(): Promise<Session[]> {
  const response = await fetchApi<ApiSession[]>('/sessions');
  return response.map(transformSession);
}

export async function getSession(id: string): Promise<Session> {
  const response = await fetchApi<ApiSession>(`/sessions/${id}`);
  return transformSession(response);
}
