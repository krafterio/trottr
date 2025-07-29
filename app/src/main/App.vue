<template>
	<div id="app" class="h-screen flex flex-col">
		<template v-if="authStore.isAuthenticated">
			<AppNavbar class="fixed top-0 left-0 right-0 z-50" />
			<div class="flex flex-1 pt-15">
				<AppSidebar class="fixed left-0 top-15 bottom-0 z-40" />
				<main class="flex-1 overflow-hidden ml-16">
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
		<CompanyDialog />
		<ContactDialog />
		<SiteDialog />
		<JobDialog />
		<ConfirmDeleteDialog />
	</div>
</template>

<script setup>
import { Toaster } from '@/common/components/ui/sonner'
import { websocketService } from '@/common/services/websocket'
import { useAuthStore } from '@/common/stores/auth'
import { usePreferencesStore } from '@/main/stores/preferences'
import AppSidebar from '@/main/components/AppSidebar.vue'
import CompanyDialog from '@/main/components/companies/CompanyDialog.vue'
import ContactDialog from '@/main/components/contacts/ContactDialog.vue'
import ConfirmDeleteDialog from '@/main/components/dialogs/ConfirmDeleteDialog.vue'
import JobDialog from '@/main/components/jobs/JobDialog.vue'
import AppNavbar from '@/main/components/navbar/AppNavbar.vue'
import SiteDialog from '@/main/components/sites/SiteDialog.vue'
import { onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import 'vue-sonner/style.css'


const route = useRoute()

const authStore = useAuthStore()
const preferencesStore = usePreferencesStore()

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
            await preferencesStore.loadPreferences()
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
