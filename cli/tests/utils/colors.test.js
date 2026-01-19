import { describe, it, expect } from 'vitest';
import { colors } from '../../src/utils/colors.js';
describe('colors', () => {
    it('has primary color defined', () => {
        expect(colors.primary).toBeDefined();
        expect(colors.primary).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
    it('has success color defined', () => {
        expect(colors.success).toBeDefined();
        expect(colors.success).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
    it('has warning color defined', () => {
        expect(colors.warning).toBeDefined();
        expect(colors.warning).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
    it('has error color defined', () => {
        expect(colors.error).toBeDefined();
        expect(colors.error).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
    it('has muted color defined', () => {
        expect(colors.muted).toBeDefined();
        expect(colors.muted).toMatch(/^#[0-9A-Fa-f]{6}$/);
    });
});
