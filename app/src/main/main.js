import '@/style.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/main/App.vue'
import router from '@/main/router/router'
import {createFetcher} from '@/common/plugins/fetcher'

const app = createApp(App)
const pinia = createPinia()
const fetcher = createFetcher()

app.use(pinia)
app.use(fetcher)
app.use(router)

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(() => console.log('ServiceWorker registered'))
            .catch(() => console.log('Error Service Worker'));
    });
}

app.mount('#app')
