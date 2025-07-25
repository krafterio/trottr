import {describe, it, expect} from 'vitest';

// This is a simple test to demonstrate how to test Vue components
describe('Example Test', () => {
    it('should pass a basic test', () => {
        expect(1 + 1).toBe(2);
    });

    it('should handle string operations', () => {
        expect('hello ' + 'world').toBe('hello world');
    });
});
