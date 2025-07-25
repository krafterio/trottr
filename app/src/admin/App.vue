<template>
    <div class="min-h-screen bg-gray-50">
        <AppNavbar v-if="authStore.isAuthenticated" />

        <main class="flex-1">
            <router-view/>
        </main>

        <WebSocketNotificationsHandler v-if="authStore.isAuthenticated" />
    </div>
</template>

<script setup>
import {onMounted} from "vue";
import {useAuthStore} from "@/common/stores/auth";
import AppNavbar from "@/admin/components/AppNavbar.vue";
import WebSocketNotificationsHandler from "@/common/components/WebSocketNotificationsHandler.vue";
import {initializeLogger} from "@/common/utils/logger";
import {initializeFeatures} from "@/common/utils/features";
import {useAdminStore} from "@/admin/stores/admin";

const authStore = useAuthStore();

useAdminStore();
initializeLogger(import.meta.env.VITE_LOG_LEVEL);
initializeFeatures(import.meta.env.VITE_FEATURES_MODE);

onMounted(async () => {
    await authStore.fetchUser();
});
</script>
