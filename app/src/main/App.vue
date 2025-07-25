<template>
	<div id="app" class="h-screen flex flex-col">
		<template v-if="authStore.isAuthenticated">
			<AppNavbar />
			<main>
				<router-view />
			</main>
		</template>

		<template v-else>
			<main>
				<router-view />
			</main>
		</template>

		<Toaster />
	</div>
</template>

<script setup>
import { useAuthStore } from '@/common/stores/auth'
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

onMounted(() => {
	if (authStore.isAuthenticated) {
		websocketService.connect()
	}
})

onUnmounted(() => {
	websocketService.disconnect()
})
</script>
