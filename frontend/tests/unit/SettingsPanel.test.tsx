import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { SettingsPanel } from '../../src/components/SettingsPanel';

describe('SettingsPanel', () => {
  it('renders without crashing', () => {
    const { container } = render(<SettingsPanel />);
    expect(container.querySelector('.settings-panel')).toBeInTheDocument();
  });

  it('has correct class name', () => {
    const { container } = render(<SettingsPanel />);
    const element = container.querySelector('.settings-panel');
    expect(element).toBeInTheDocument();
    expect(element?.tagName.toLowerCase()).toBe('div');
  });
});
