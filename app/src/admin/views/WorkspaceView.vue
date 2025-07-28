<template>
    <v-container fluid class="pa-0 d-flex flex-column">
        <v-row class="fill-height ma-0">
            <v-col class="info-col border-e pa-0">
                <div class="d-flex flex-row pa-5 pb-0 ga-3">
                    <div class="form-view-title d-flex flex-column ga-1 justify-center flex-grow-1">
                        <div class="d-flex justify-space-between ga-2 mb-4">
                            <v-btn variant="outlined" @click="router.push({ name: 'workspaces' })">
                                <ArrowLeft class="me-1" />
                                Retour
                            </v-btn>

                            <v-spacer />

                            <div class="d-flex ga-2">
                                <v-btn v-if="isDirty" @click="saveWorkspace" :loading="loading" icon rounded width="30">
                                    <Save :size="16" />
                                </v-btn>

                                <v-btn v-if="isDirty" @click="resetForm" icon rounded width="30">
                                    <RotateCcw :size="16" class="text-orange" />
                                </v-btn>

                                <v-menu location="bottom start" offset="5">
                                    <template v-slot:activator="{ props }">
                                        <v-btn v-bind="props" icon rounded width="30" elevation="0">
                                            <MoreVertical />
                                        </v-btn>
                                    </template>
                                    <v-list density="compact">
                                        <v-list-item @click="openDeleteDialog">
                                            <template #prepend>
                                                <Trash2 :size="16" class="me-2 text-error" />
                                            </template>
                                            <v-list-item-title>Supprimer</v-list-item-title>
                                        </v-list-item>
                                    </v-list>
                                </v-menu>
                            </div>
                        </div>

                        <v-text-field v-model="form.name" class="ma-0" required placeholder="Nom de l'espace de travail"
                            :autofocus="!isEdit" variant="plain" hide-details density="compact" />

                        <div class="d-flex flex-wrap ga-2 mt-2">
                            <v-chip v-if="form.unique_id" variant="tonal" color="primary" size="small"
                                class="font-weight-medium">
                                <Fingerprint class="me-1" :size="12" />
                                {{ form.unique_id }}
                            </v-chip>

                            <v-chip v-if="form.plan" :color="getPlanColor(form.plan)" variant="tonal" size="small"
                                class="font-weight-medium">
                                <Crown class="me-1" :size="12" />
                                {{ form.plan }}
                            </v-chip>
                        </div>
                    </div>
                </div>

                <v-form @submit.prevent="saveWorkspace" class="mt-3 px-5 py-3">
                    <s-field v-model="form.name" fieldType="v-text-field" horizontal label="Nom" placeholder="Nom" />

                    <s-field v-model="form.unique_id" fieldType="v-text-field" horizontal label="ID Unique"
                        placeholder="ID Unique" disabled />

                    <s-field v-model="form.currency" fieldType="v-select" horizontal label="Devise" placeholder="Devise"
                        disabled />

                    <s-field v-model="form.stripe_customer_id" fieldType="v-text-field" horizontal
                        label="ID Client Stripe" placeholder="ID Client Stripe" />
                </v-form>
            </v-col>

            <v-col class="pa-0 flex-grow-1">
                <v-tabs v-model="activeTab" class="border-b bg-white">
                    <v-tab value="users">
                        <Users :size="16" class="me-1" />
                        <span>Utilisateurs</span>
                    </v-tab>
                    <v-tab value="usage" v-if="false">
                        <ChartLine :size="16" class="me-1" />
                        <span>Utilisation</span>
                    </v-tab>
                    <v-tab value="subscriptions" v-if="false">
                        <CreditCard :size="16" class="me-1" />
                        <span>Abonnements</span>
                    </v-tab>
                </v-tabs>

                <v-window v-model="activeTab">
                    <v-window-item value="users" class="pa-5">
                        <div class="d-flex justify-center align-center" style="height: 200px">
                            <div class="text-center">
                                <p class="text-body-1 mb-3">Liste des utilisateurs du workspace</p>
                            </div>
                        </div>
                    </v-window-item>
                </v-window>
            </v-col>
        </v-row>

        <!-- Confirm Delete Dialog -->
        <v-dialog v-model="deleteDialog" max-width="500">
            <v-card>
                <v-card-title class="text-h5">Confirmation de suppression</v-card-title>
                <v-card-text>
                    Êtes-vous sûr de vouloir supprimer l'espace de travail "{{ form.name }}" ? Cette action est
                    irréversible.
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="secondary" variant="text" @click="deleteDialog = false">Annuler</v-btn>
                    <v-btn color="error" variant="flat" @click="deleteWorkspace" :loading="deleting">Supprimer</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-container>
</template>

<script setup>
import { useFetcher } from "@/common/composables/fetcher.js";
import { useSnackbar } from '@/common/composables/snackbar';
import { cloneDeep, isEqual } from 'lodash';
import {
    ArrowLeft,
    ChartLine,
    CreditCard,
    Crown,
    Fingerprint,
    MoreVertical,
    RotateCcw,
    Save,
    Trash2,
    Users,
} from 'lucide-vue-next';
import { computed, onMounted, ref } from 'vue';
import { onBeforeRouteLeave, useRoute, useRouter } from 'vue-router';

const fetcher = useFetcher();
const route = useRoute();
const router = useRouter();
const { showSnackbar } = useSnackbar();

const isEdit = computed(() => !!route.params.id);
const workspaceId = computed(() => route.params.id);
const activeTab = ref('users');
const loading = ref(false);
const deleting = ref(false);
const deleteDialog = ref(false);

const defaultForm = {
    name: '',
    unique_id: '',
    currency: 'EUR',
    plan: 'pro',
    stripe_customer_id: '',
};

const form = ref({ ...defaultForm });
const originalForm = ref(null);

const isDirty = computed(() => {
    if (!originalForm.value) return false;
    return !isEqual(form.value, originalForm.value);
});

const getPlanColor = (plan) => {
    switch (plan) {
        case 'Pro':
            return 'purple';
        case 'Business':
            return 'blue';
        case 'Entrerprise':
            return 'green';
        default:
            return 'grey';
    }
};

const fetchWorkspace = async () => {
    if (!isEdit.value) return;

    loading.value = true;

    try {
        const response = await fetcher.get(`/admin/workspaces/${workspaceId.value}`);
        const data = await response.data;

        form.value = data;
        originalForm.value = cloneDeep(data);
    } catch (error) {
        console.error('Erreur:', error);
        showSnackbar('Erreur lors du chargement du workspace', 'error');
        router.push({ name: 'workspaces' });
    } finally {
        loading.value = false;
    }
};

const saveWorkspace = async () => {
    loading.value = true;

    try {
        const response = await fetcher.patch(`/admin/workspaces/${workspaceId.value}`, {
            name: form.value.name,
            stripe_customer_id: form.value.stripe_customer_id,
        });
        const data = await response.data;

        showSnackbar(`Workspace ${isEdit.value ? 'modifié' : 'créé'} avec succès`);

        if (!isEdit.value) {
            router.push({ name: 'workspace', params: { id: data.id } });
        } else {
            fetchWorkspace().then();
        }
    } catch (error) {
        console.error('Erreur:', error);
        showSnackbar(`Erreur lors de ${isEdit.value ? 'la modification' : 'la création'} du workspace`, 'error');
    } finally {
        loading.value = false;
    }
};

const resetForm = () => {
    form.value = cloneDeep(originalForm.value);
};

const openDeleteDialog = () => {
    deleteDialog.value = true;
};

const deleteWorkspace = async () => {
    deleting.value = true;

    try {
        await fetcher.delete(`/admin/workspaces/${workspaceId.value}`);
        showSnackbar('Workspace supprimé avec succès');
        deleteDialog.value = false;
        router.push({ name: 'workspaces' });
    } catch (error) {
        console.error('Erreur:', error);
        showSnackbar('Erreur lors de la suppression', 'error');
    } finally {
        deleting.value = false;
    }
};

onBeforeRouteLeave((to, from, next) => {
    if (isDirty.value) {
        if (confirm('Vous avez des modifications non sauvegardées. Voulez-vous vraiment quitter ?')) {
            next();
        } else {
            next(false);
        }
    } else {
        next();
    }
});

onMounted(() => {
    fetchWorkspace().then();
});
</script>

<style scoped>
.info-col {
    width: 450px;
    min-width: 450px;
    background: white;
}

@media (max-width: 1200px) {
    .info-col {
        width: 100%;
        min-width: 100%;
    }
}
</style>
