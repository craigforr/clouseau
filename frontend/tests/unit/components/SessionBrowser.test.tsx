import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SessionBrowser from '../../../src/components/SessionBrowser/SessionBrowser';
import { AppProvider } from '../../../src/context/AppContext';
import * as sessionsHook from '../../../src/hooks/useSessions';
import * as conversationsHook from '../../../src/hooks/useConversations';

vi.mock('../../../src/hooks/useSessions');
vi.mock('../../../src/hooks/useConversations');

function renderWithProvider() {
  return render(
    <AppProvider>
      <SessionBrowser />
    </AppProvider>
  );
}

describe('SessionBrowser', () => {
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
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders loading state', () => {
    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions: [],
      loading: true,
      error: null,
      refetch: vi.fn(),
    });

    renderWithProvider();

    expect(screen.getByText('Loading sessions...')).toBeInTheDocument();
  });

  it('renders error state', () => {
    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions: [],
      loading: false,
      error: new Error('Network error'),
      refetch: vi.fn(),
    });

    renderWithProvider();

    expect(screen.getByText('Error: Network error')).toBeInTheDocument();
  });

  it('renders empty state', () => {
    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions: [],
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    renderWithProvider();

    expect(screen.getByText('No sessions found')).toBeInTheDocument();
  });

  it('renders sessions list', () => {
    const sessions = [
      { id: '1', name: 'Session 1', description: 'First', createdAt: new Date(), updatedAt: new Date() },
      { id: '2', name: 'Session 2', createdAt: new Date(), updatedAt: new Date() },
    ];
    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    renderWithProvider();

    expect(screen.getByText('Session 1')).toBeInTheDocument();
    expect(screen.getByText('First')).toBeInTheDocument();
    expect(screen.getByText('Session 2')).toBeInTheDocument();
  });

  it('selects session on click and shows conversations', async () => {
    const user = userEvent.setup();
    const sessions = [
      { id: '1', name: 'Session 1', createdAt: new Date(), updatedAt: new Date() },
    ];
    const conversations = [
      { id: '10', sessionId: '1', title: 'Conv 1', createdAt: new Date(), updatedAt: new Date() },
    ];

    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    vi.mocked(conversationsHook.useConversations).mockReturnValue({
      conversations,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    renderWithProvider();

    await user.click(screen.getByText('Session 1'));

    expect(screen.getByText('Conv 1')).toBeInTheDocument();
  });

  it('shows loading state for conversations', async () => {
    const user = userEvent.setup();
    const sessions = [
      { id: '1', name: 'Session 1', createdAt: new Date(), updatedAt: new Date() },
    ];

    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    vi.mocked(conversationsHook.useConversations).mockReturnValue({
      conversations: [],
      loading: true,
      error: null,
      refetch: vi.fn(),
    });

    renderWithProvider();

    await user.click(screen.getByText('Session 1'));

    expect(screen.getByText('Loading conversations...')).toBeInTheDocument();
  });

  it('shows error state for conversations', async () => {
    const user = userEvent.setup();
    const sessions = [
      { id: '1', name: 'Session 1', createdAt: new Date(), updatedAt: new Date() },
    ];

    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    vi.mocked(conversationsHook.useConversations).mockReturnValue({
      conversations: [],
      loading: false,
      error: new Error('Conversation fetch error'),
      refetch: vi.fn(),
    });

    renderWithProvider();

    await user.click(screen.getByText('Session 1'));

    expect(screen.getByText('Error: Conversation fetch error')).toBeInTheDocument();
  });

  it('shows empty state for conversations', async () => {
    const user = userEvent.setup();
    const sessions = [
      { id: '1', name: 'Session 1', createdAt: new Date(), updatedAt: new Date() },
    ];

    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions,
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

    renderWithProvider();

    await user.click(screen.getByText('Session 1'));

    expect(screen.getByText('No conversations')).toBeInTheDocument();
  });

  it('selects a conversation when clicked', async () => {
    const user = userEvent.setup();
    const sessions = [
      { id: '1', name: 'Session 1', createdAt: new Date(), updatedAt: new Date() },
    ];
    const conversations = [
      { id: '10', sessionId: '1', title: 'Conv 1', createdAt: new Date(), updatedAt: new Date() },
    ];

    vi.mocked(sessionsHook.useSessions).mockReturnValue({
      sessions,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });
    vi.mocked(conversationsHook.useConversations).mockReturnValue({
      conversations,
      loading: false,
      error: null,
      refetch: vi.fn(),
    });

    renderWithProvider();

    // Select session first
    await user.click(screen.getByText('Session 1'));
    // Then select conversation
    await user.click(screen.getByText('Conv 1'));

    // The conversation item should have selection styling (green)
    const convButton = screen.getByText('Conv 1').closest('button');
    expect(convButton).toHaveClass('bg-green-100');
  });
});
