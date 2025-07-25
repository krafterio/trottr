import {defineConfig} from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import vuetify from 'vite-plugin-vuetify';
import {fileURLToPath, URL} from 'node:url';

export default defineConfig({
    plugins: [
        vue(),
        vuetify(),
    ],
    test: {
        globals: true,
        environment: 'jsdom',
        include: ['./tests/**/*.test.js'],
    },
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url)),
        },
    },
});
