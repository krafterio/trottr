<template>
	<div id="app" class="h-screen flex flex-col">
		<template v-if="authStore.isAuthenticated">
			<AppNavbar />
			<div class="flex flex-1">
				<AppSidebar />
				<main class="flex-1 overflow-hidden">
					<router-view />
				</main>
			</div>
		</template>

		<template v-else>
			<main class="h-full">
				<router-view />
			</main>
		</template>

		<Toaster />
	</div>
</template>

<script setup>
import { Toaster } from '@/common/components/ui/sonner'
import { websocketService } from '@/common/services/websocket'
import { useAuthStore } from '@/common/stores/auth'
import AppSidebar from '@/main/components/AppSidebar.vue'
import AppNavbar from '@/main/components/navbar/AppNavbar.vue'
import { onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const authStore = useAuthStore()

watch(() => authStore.isAuthenticated, (isAuthenticated) => {
	if (isAuthenticated) {
		websocketService.connect()
	} else {
		websocketService.disconnect()
	}
})

onMounted(async () => {
	if (authStore.isAuthenticated) {
		try {
			await authStore.fetchUser()
		} catch (error) {
			console.error('Erreur lors du chargement des données utilisateur:', error)
		}
		websocketService.connect()
	}
})

onUnmounted(() => {
	websocketService.disconnect()
})
</script>
