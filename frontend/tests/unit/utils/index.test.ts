import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { formatDate, formatRelativeDate } from '../../../src/utils';

describe('formatDate', () => {
  it('formats date with full details', () => {
    const date = new Date('2024-01-15T14:30:00Z');
    const result = formatDate(date);

    // The exact format depends on locale, but it should contain these parts
    expect(result).toContain('2024');
    expect(result).toContain('Jan');
    expect(result).toContain('15');
  });
});

describe('formatRelativeDate', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('returns "just now" for recent times', () => {
    const now = new Date('2024-01-15T12:00:00Z');
    vi.setSystemTime(now);

    const date = new Date('2024-01-15T11:59:45Z'); // 15 seconds ago
    expect(formatRelativeDate(date)).toBe('just now');
  });

  it('returns minutes ago', () => {
    const now = new Date('2024-01-15T12:00:00Z');
    vi.setSystemTime(now);

    const date = new Date('2024-01-15T11:45:00Z'); // 15 minutes ago
    expect(formatRelativeDate(date)).toBe('15m ago');
  });

  it('returns hours ago', () => {
    const now = new Date('2024-01-15T12:00:00Z');
    vi.setSystemTime(now);

    const date = new Date('2024-01-15T09:00:00Z'); // 3 hours ago
    expect(formatRelativeDate(date)).toBe('3h ago');
  });

  it('returns days ago for less than a week', () => {
    const now = new Date('2024-01-15T12:00:00Z');
    vi.setSystemTime(now);

    const date = new Date('2024-01-13T12:00:00Z'); // 2 days ago
    expect(formatRelativeDate(date)).toBe('2d ago');
  });

  it('returns formatted date for older dates', () => {
    const now = new Date('2024-01-15T12:00:00Z');
    vi.setSystemTime(now);

    const date = new Date('2024-01-01T12:00:00Z'); // 14 days ago
    const result = formatRelativeDate(date);

    expect(result).toContain('2024');
    expect(result).toContain('Jan');
  });
});
