import { createFetcher } from '@/common/plugins/fetcher'
import App from '@/main/App.vue'
import router from '@/main/router/router'
import '@/style.css'
import ganttastic from '@infectoone/vue-ganttastic'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

const app = createApp(App)
const pinia = createPinia()
const fetcher = createFetcher()

app.use(pinia)
app.use(fetcher)
app.use(router)
app.use(ganttastic)

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(() => console.log('ServiceWorker registered'))
            .catch(() => console.log('Error Service Worker'));
    });
}

app.mount('#app')
