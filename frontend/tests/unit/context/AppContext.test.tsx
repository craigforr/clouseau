import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { AppProvider, useAppContext } from '../../../src/context/AppContext';

function TestComponent() {
  const { selectedSessionId, selectedConversationId, selectSession, selectConversation } = useAppContext();

  return (
    <div>
      <span data-testid="session-id">{selectedSessionId ?? 'none'}</span>
      <span data-testid="conversation-id">{selectedConversationId ?? 'none'}</span>
      <button onClick={() => selectSession('session-1')}>Select Session</button>
      <button onClick={() => selectConversation('conversation-1')}>Select Conversation</button>
      <button onClick={() => selectSession(null)}>Clear Session</button>
    </div>
  );
}

describe('AppContext', () => {
  it('provides initial null values', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    expect(screen.getByTestId('session-id')).toHaveTextContent('none');
    expect(screen.getByTestId('conversation-id')).toHaveTextContent('none');
  });

  it('updates selected session', async () => {
    const user = userEvent.setup();
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await user.click(screen.getByText('Select Session'));

    expect(screen.getByTestId('session-id')).toHaveTextContent('session-1');
  });

  it('updates selected conversation', async () => {
    const user = userEvent.setup();
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    await user.click(screen.getByText('Select Conversation'));

    expect(screen.getByTestId('conversation-id')).toHaveTextContent('conversation-1');
  });

  it('clears conversation when session changes', async () => {
    const user = userEvent.setup();
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    // First select a conversation
    await user.click(screen.getByText('Select Conversation'));
    expect(screen.getByTestId('conversation-id')).toHaveTextContent('conversation-1');

    // Then select a session - conversation should be cleared
    await user.click(screen.getByText('Select Session'));
    expect(screen.getByTestId('session-id')).toHaveTextContent('session-1');
    expect(screen.getByTestId('conversation-id')).toHaveTextContent('none');
  });

  it('throws error when used outside provider', () => {
    // Suppress console.error for this test
    const consoleError = console.error;
    console.error = () => {};

    expect(() => render(<TestComponent />)).toThrow('useAppContext must be used within an AppProvider');

    console.error = consoleError;
  });
});
