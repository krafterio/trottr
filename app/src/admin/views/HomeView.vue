<template>
    <div>
        <div class="container mx-auto pt-12">
            <div class="mb-6">
                <h1 class="text-4xl font-bold mb-2">
                    Bienvenue sur le <br />
                    Gestionnaire admin Trottr
                </h1>
                <p class="text-gray-600 mt-2">
                    Administrer l'intégralité de Trottr, gérer les espaces de travail, les utilisateurs et les services.
                </p>
            </div>

            <Card class="mb-10 py-1">
                <CardContent class="p-6">
                    <h4 class="text-lg font-semibold mb-1">Statistiques générales</h4>
                        <div class="flex flex-wrap gap-4 mt-3">
                            <div class="flex items-center">
                                <Crown :size="16" class="mr-2 text-gray-500" />
                                <span class="text-sm">{{ workspaceTotal }} espaces de travail</span>
                            </div>
                            <div class="flex items-center">
                                <Users :size="16" class="mr-2 text-gray-500" />
                                <span class="text-sm">{{ workspaceUserTotal }} utilisateurs</span>
                            </div>
                        </div>
                </CardContent>
            </Card>

            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card class="h-full cursor-pointer hover:shadow-lg hover:bg-accent"
                    @click="$router.push({ name: 'workspaces' })">
                    <CardContent class="px-6">
                        <div class="flex flex-col items-start">
                            <Building2 :size="40" class="mb-3" :stroke-width="1.2" />
                            <h3 class="text-xl font-semibold mb-3">Espaces de travail</h3>
                            <p class="text-sm text-gray-600 mb-4">
                                Gérer les espaces de travail et leurs utilisateurs
                            </p>
                        </div>
                    </CardContent>
                </Card>

                <Card class="h-full cursor-pointer hover:shadow-lg hover:bg-accent"
                    @click="$router.push({ name: 'service-plans' })">
                    <CardContent class="px-6">
                        <div class="flex flex-col items-start">
                            <WalletCards :size="40" class="mb-3" :stroke-width="1.2" />
                            <h3 class="text-xl font-semibold mb-3">Plans d'abonnement</h3>
                            <p class="text-sm text-gray-600 mb-4">
                                Gérer les plans d'abonnement Stripe et leurs configurations
                            </p>
                        </div>
                    </CardContent>
                </Card>

                <Card class="h-full cursor-pointer hover:shadow-lg hover:bg-accent"
                    @click="$router.push({ name: 'service-taxes' })">
                    <CardContent class="px-6">
                        <div class="flex flex-col items-start">
                            <Landmark :size="40" class="mb-3" :stroke-width="1.2" />
                            <h3 class="text-xl font-semibold mb-3">Taxes</h3>
                            <p class="text-sm text-gray-600 mb-4">
                                Configurer les taxes Stripe par pays et région
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '@/common/stores/auth';
import { Crown, Users } from "lucide-vue-next";
import { useFetcher } from "@/common/composables/fetcher.js";
import { onMounted, ref } from "vue";
import { Card, CardContent } from '@/common/components/ui/card';
import { Building2, CreditCard, Landmark, User, Users2, WalletCards } from 'lucide-vue-next';

const authStore = useAuthStore();
const fetcher = useFetcher();
const workspaceLoading = ref(false);
const workspaceTotal = ref(0);
const workspaceUserLoading = ref(false);
const workspaceUserTotal = ref(0);

async function fetchWorkspaceTotals() {
    if (!authStore.isAuthenticated || workspaceLoading.value) {
        return;
    }

    workspaceLoading.value = true;

    try {
        const response = await fetcher.get(`/admin/workspaces`, {
            params: { limit: 1 },
            headers: { 'X-Fields': 'id' }
        });

        workspaceTotal.value = response.data?.total || 0;
    } catch (err) {
    } finally {
        workspaceLoading.value = false;
    }
}

async function fetchUserTotals() {
    if (!authStore.isAuthenticated || workspaceUserLoading.value) {
        return;
    }

    workspaceUserLoading.value = true;

    try {
        const response = await fetcher.get(`/admin/users`, {
            params: { limit: 1 },
            headers: { 'X-Fields': 'id' }
        });

        workspaceUserTotal.value = response.data?.total || 0;
    } catch (err) {
    } finally {
        workspaceUserLoading.value = false;
    }
}

onMounted(async () => {
    return Promise.all([
        fetchWorkspaceTotals(),
        fetchUserTotals(),
    ]);
});
</script>
