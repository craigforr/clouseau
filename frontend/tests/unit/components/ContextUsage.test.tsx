import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ContextUsage from '../../../src/components/ContextUsage/ContextUsage';

describe('ContextUsage', () => {
  it('renders context usage with correct values', () => {
    render(<ContextUsage used={5000} total={10000} />);

    expect(screen.getByText(/Context:/)).toBeInTheDocument();
    expect(screen.getByText(/5,000/)).toBeInTheDocument();
    expect(screen.getByText(/10,000/)).toBeInTheDocument();
    expect(screen.getByText(/50\.0%/)).toBeInTheDocument();
  });

  it('calculates percentage correctly', () => {
    render(<ContextUsage used={2500} total={10000} />);

    expect(screen.getByText(/25\.0%/)).toBeInTheDocument();
  });

  it('formats large numbers with locale separators', () => {
    render(<ContextUsage used={128000} total={200000} />);

    expect(screen.getByText(/128,000/)).toBeInTheDocument();
    expect(screen.getByText(/200,000/)).toBeInTheDocument();
  });

  it('has correct container class', () => {
    const { container } = render(<ContextUsage used={100} total={1000} />);

    expect(container.querySelector('.context-usage')).toBeInTheDocument();
  });
});
