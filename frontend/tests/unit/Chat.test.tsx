import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { Chat } from '../../src/components/Chat';

describe('Chat', () => {
  it('renders without crashing', () => {
    const { container } = render(<Chat />);
    expect(container.querySelector('.chat-container')).toBeInTheDocument();
  });

  it('renders with sessionId prop', () => {
    const { container } = render(<Chat sessionId="test-session-123" />);
    expect(container.querySelector('.chat-container')).toBeInTheDocument();
  });

  it('renders without sessionId prop', () => {
    const { container } = render(<Chat />);
    expect(container.querySelector('.chat-container')).toBeInTheDocument();
  });
});
