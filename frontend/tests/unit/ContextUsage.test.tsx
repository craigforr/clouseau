import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ContextUsage } from '../../src/components/ContextUsage';

describe('ContextUsage', () => {
  it('renders token count', () => {
    render(<ContextUsage used={5000} total={10000} />);
    expect(screen.getByText(/5,000/)).toBeInTheDocument();
    expect(screen.getByText(/10,000/)).toBeInTheDocument();
  });

  it('calculates percentage correctly', () => {
    render(<ContextUsage used={5000} total={10000} />);
    expect(screen.getByText(/50\.0%/)).toBeInTheDocument();
  });

  it('handles zero total gracefully', () => {
    render(<ContextUsage used={0} total={100} />);
    expect(screen.getByText(/0\.0%/)).toBeInTheDocument();
  });
});
