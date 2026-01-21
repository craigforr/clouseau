import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import Chat from '../../../src/components/Chat/Chat';
import { AppProvider, useAppContext } from '../../../src/context/AppContext';
import * as exchangesHook from '../../../src/hooks/useExchanges';
import { ReactNode, useEffect } from 'react';

vi.mock('../../../src/hooks/useExchanges');

// Helper to set initial context state
function TestWrapper({ children, conversationId }: { children: ReactNode; conversationId: string | null }) {
  return (
    <AppProvider>
      <ConversationSelector conversationId={conversationId} />
      {children}
    </AppProvider>
  );
}

function ConversationSelector({ conversationId }: { conversationId: string | null }) {
  const { selectConversation, selectSession } = useAppContext();
  useEffect(() => {
    if (conversationId) {
      selectSession('1'); // Need a session to have a conversation
      selectConversation(conversationId);
    }
  }, [conversationId, selectConversation, selectSession]);
  return null;
}

describe('Chat', () => {
  beforeEach(() => {
    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders without crashing', () => {
    const { container } = render(
      <AppProvider>
        <Chat />
      </AppProvider>
    );
    expect(container.querySelector('.chat-container')).toBeInTheDocument();
  });

  it('renders empty state when no conversation selected', () => {
    render(
      <AppProvider>
        <Chat />
      </AppProvider>
    );
    expect(screen.getByText('No conversation selected')).toBeInTheDocument();
    expect(screen.getByText('Select a conversation from the sidebar to view exchanges')).toBeInTheDocument();
  });

  it('renders loading state', () => {
    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges: [],
      loading: true,
      error: null,
      refetch: vi.fn(),
    });

    render(
      <TestWrapper conversationId="10">
        <Chat />
      </TestWrapper>
    );

    expect(screen.getByText('Loading exchanges...')).toBeInTheDocument();
  });

  it('renders error state', () => {
    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges: [],
      loading: false,
      error: new Error('Network error'),
      refetch: vi.fn(),
    });

    render(
      <TestWrapper conversationId="10">
        <Chat />
      </TestWrapper>
    );

    expect(screen.getByText('Error: Network error')).toBeInTheDocument();
  });

  it('renders empty exchanges state', () => {
    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    render(
      <TestWrapper conversationId="10">
        <Chat />
      </TestWrapper>
    );

    expect(screen.getByText('No exchanges in this conversation')).toBeInTheDocument();
  });

  it('renders exchanges as chat bubbles', () => {
    const exchanges = [
      {
        id: '100',
        conversationId: '10',
        userMessage: 'Hello there',
        assistantMessage: 'Hi! How can I help?',
        model: 'gpt-4',
        inputTokens: 10,
        outputTokens: 15,
        createdAt: new Date('2024-01-15T10:00:00Z'),
      },
    ];

    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    render(
      <TestWrapper conversationId="10">
        <Chat />
      </TestWrapper>
    );

    expect(screen.getByText('Hello there')).toBeInTheDocument();
    expect(screen.getByText('Hi! How can I help?')).toBeInTheDocument();
    expect(screen.getByText('gpt-4')).toBeInTheDocument();
    expect(screen.getByText('10 in / 15 out tokens')).toBeInTheDocument();
  });

  it('renders exchange without token metadata when not available', () => {
    const exchanges = [
      {
        id: '100',
        conversationId: '10',
        userMessage: 'Test',
        assistantMessage: 'Response',
        createdAt: new Date('2024-01-15T10:00:00Z'),
      },
    ];

    vi.mocked(exchangesHook.useExchanges).mockReturnValue({
      exchanges,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    render(
      <TestWrapper conversationId="10">
        <Chat />
      </TestWrapper>
    );

    expect(screen.getByText('Test')).toBeInTheDocument();
    expect(screen.getByText('Response')).toBeInTheDocument();
    expect(screen.queryByText(/tokens/)).not.toBeInTheDocument();
  });
});
