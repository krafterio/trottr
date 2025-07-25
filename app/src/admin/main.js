import '@/style.css'
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from '@/admin/App.vue';
import router from '@/admin/router/router';
import {createFetcher} from "@/common/plugins/fetcher";

const app = createApp(App);
const pinia = createPinia();
const fetcher = createFetcher();

app.use(pinia);
app.use(fetcher);
app.use(router);

app.mount('#app');
