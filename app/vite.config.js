import fs from 'node:fs'
import { dirname, resolve } from 'node:path'
import { fileURLToPath, URL } from 'node:url'

import tailwindcss from '@tailwindcss/vite'
import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'

const cwd = dirname(fileURLToPath(import.meta.url))

const swPlugin = () => {
  function generateSW(cacheName = undefined) {
    cacheName = cacheName ? cacheName : `v${Date.now()}`
    const swSource = fs.readFileSync('./src/common/sw.js', 'utf8')

    return swSource.replace('__CACHE_NAME__', `app-${cacheName}`)
  }

  return {
    name: 'sw-plugin',
    configureServer(server) {
      server.middlewares.use('/sw.js', (req, res, next) => {
        res.setHeader('Content-Type', 'application/javascript')
        res.end(generateSW('dev'))
      })
    },
    generateBundle() {
      this.emitFile({
        type: 'asset',
        fileName: 'sw.js',
        source: generateSW(),
      })
    }
  }
};

const adminPlugin = () => {
  return {
    name: 'configure-server',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url === '/admin' || req.url?.startsWith('/admin/')) {
          const adminHtml = fs.readFileSync(
            resolve(cwd, 'admin.html'),
            'utf-8'
          )
          res.setHeader('Content-Type', 'text/html')
          res.end(adminHtml)
          return
        }
        next()
      })
    }
  };
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss(),
    swPlugin(),
    adminPlugin(),
  ],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: resolve(cwd, 'index.html'),
        admin: resolve(cwd, 'admin.html')
      }
    }
  },
  server: {
    port: 5175,
    strictPort: true
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
})
