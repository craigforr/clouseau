import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import App from '../../src/App';
import * as sessionsHook from '../../src/hooks/useSessions';
import * as conversationsHook from '../../src/hooks/useConversations';
import * as exchangesHook from '../../src/hooks/useExchanges';

vi.mock('../../src/hooks/useSessions');
vi.mock('../../src/hooks/useConversations');
vi.mock('../../src/hooks/useExchanges');

describe('App', () => {
  beforeEach(() => {
    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    vi.mocked(conversationsHook.useConversations).mockReturnValue({
      conversations: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
  });

  it('renders the app title', () => {
    render(<App />);
    expect(screen.getByText('Clouseau')).toBeInTheDocument();
  });

  it('renders the description', () => {
    render(<App />);
    expect(screen.getByText('LLM Interaction Inspector')).toBeInTheDocument();
  });

  it('has correct structure', () => {
    const { container } = render(<App />);
    expect(container.querySelector('header')).toBeInTheDocument();
    expect(container.querySelector('main')).toBeInTheDocument();
    expect(container.querySelector('aside')).toBeInTheDocument();
  });

  it('renders sidebar with Sessions heading', () => {
    render(<App />);
    expect(screen.getByText('Sessions')).toBeInTheDocument();
  });

  it('renders chat empty state by default', () => {
    render(<App />);
    expect(screen.getByText('No conversation selected')).toBeInTheDocument();
  });
});
