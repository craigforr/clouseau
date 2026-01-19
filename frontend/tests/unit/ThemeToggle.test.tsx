import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ThemeToggle } from '../../src/components/ThemeToggle';

describe('ThemeToggle', () => {
  it('renders without crashing', () => {
    const { container } = render(<ThemeToggle />);
    expect(container.querySelector('.theme-toggle')).toBeInTheDocument();
  });

  it('renders as a button', () => {
    const { container } = render(<ThemeToggle />);
    const button = container.querySelector('.theme-toggle');
    expect(button?.tagName.toLowerCase()).toBe('button');
  });
});
