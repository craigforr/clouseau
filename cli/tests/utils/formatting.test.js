import { describe, it, expect } from 'vitest';
import { formatTokenCount, formatDuration } from '../../src/utils/formatting.js';
describe('formatTokenCount', () => {
    it('formats small numbers as-is', () => {
        expect(formatTokenCount(500)).toBe('500');
        expect(formatTokenCount(999)).toBe('999');
    });
    it('formats thousands with K suffix', () => {
        expect(formatTokenCount(1000)).toBe('1.0K');
        expect(formatTokenCount(5500)).toBe('5.5K');
        expect(formatTokenCount(999999)).toBe('1000.0K');
    });
    it('formats millions with M suffix', () => {
        expect(formatTokenCount(1000000)).toBe('1.0M');
        expect(formatTokenCount(2500000)).toBe('2.5M');
    });
});
describe('formatDuration', () => {
    it('formats milliseconds', () => {
        expect(formatDuration(100)).toBe('100ms');
        expect(formatDuration(999)).toBe('999ms');
    });
    it('formats seconds', () => {
        expect(formatDuration(1000)).toBe('1.00s');
        expect(formatDuration(2500)).toBe('2.50s');
        expect(formatDuration(10000)).toBe('10.00s');
    });
});
