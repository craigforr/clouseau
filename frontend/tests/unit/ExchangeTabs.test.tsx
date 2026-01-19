import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { ExchangeTabs } from '../../src/components/ExchangeTabs';

describe('ExchangeTabs', () => {
  it('renders without crashing', () => {
    const { container } = render(<ExchangeTabs exchangeId="test-exchange-123" />);
    expect(container.querySelector('.exchange-tabs')).toBeInTheDocument();
  });

  it('accepts exchangeId prop', () => {
    const { container } = render(<ExchangeTabs exchangeId="another-exchange" />);
    expect(container.querySelector('.exchange-tabs')).toBeInTheDocument();
  });
});
