import {defineStore} from 'pinia';
import {ref, watch} from 'vue';
import {useAuthStore} from '@/common/stores/auth';
import {useFetcher} from "@/common/composables/fetcher.js";

export const useAdminStore = defineStore('admin', () => {
    const loading = ref(false);
    const error = ref(null);
    const authStore = useAuthStore();
    const fetcher = useFetcher({abortOnUnmounted: false});

    async function fetchAdmin() {
        if (!authStore.isAuthenticated || loading.value) {
            return;
        }

        loading.value = true;
        error.value = null;

        try {
            await fetcher.get(`/admin/info`);
        } catch (err) {
            if (err.response.status === 403) {
                await authStore.logout();
            }

            error.value = err;
        } finally {
            loading.value = false;
        }
    }

    watch(() => authStore.user, async (user) => {
        if (user) {
            await fetchAdmin();
        }
    })

    return {
        loading,
        error,
        fetchAdmin,
    };
});
