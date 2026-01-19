import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { SearchInterface } from '../../src/components/SearchInterface';

describe('SearchInterface', () => {
  it('renders without crashing', () => {
    const { container } = render(<SearchInterface />);
    expect(container.querySelector('.search-interface')).toBeInTheDocument();
  });

  it('has correct class name', () => {
    const { container } = render(<SearchInterface />);
    const element = container.querySelector('.search-interface');
    expect(element).toBeInTheDocument();
    expect(element?.tagName.toLowerCase()).toBe('div');
  });
});
