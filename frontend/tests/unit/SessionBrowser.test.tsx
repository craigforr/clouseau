import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { SessionBrowser } from '../../src/components/SessionBrowser';

describe('SessionBrowser', () => {
  it('renders without crashing', () => {
    const { container } = render(<SessionBrowser />);
    expect(container.querySelector('.session-browser')).toBeInTheDocument();
  });

  it('has correct class name', () => {
    const { container } = render(<SessionBrowser />);
    const element = container.querySelector('.session-browser');
    expect(element).toBeInTheDocument();
    expect(element?.tagName.toLowerCase()).toBe('div');
  });
});
