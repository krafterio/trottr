import { bus } from "@/common/composables/bus";
import { useFetcher } from "@/common/composables/fetcher.js";
import { useAuthStore } from '@/common/stores/auth';
import { defineStore } from 'pinia';
import { computed, ref, watch } from 'vue';

export const useWorkspaceStore = defineStore('workspace', () => {
    const workspace = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const authStore = useAuthStore()
    const fetcher = useFetcher({ abortOnUnmounted: false })

    const name = computed(() => {
        return workspace.value?.name || '';
    })

    function hasPlan(targetPlan) {
        return availablePlans.value.includes(targetPlan);
    }

    const isValid = computed(() => {
        const ws = workspace.value;

        if (!ws || isTrial.value || (!ws?.is_trial && !ws?.trial_end)) {
            return true;
        }

        return false;
    })

    const isTrial = computed(() => {
        const ws = workspace.value;

        return !!ws?.is_trial && !!ws?.trial_end;
    })

    const trialDaysRemaining = computed(() => {
        const ws = workspace.value;

        if (!ws || !ws?.is_trial || !ws?.trial_end) {
            return 0;
        }

        const now = new Date();
        const trialEnd = new Date(ws?.trial_end);
        const diff = trialEnd.getTime() - now.getTime();

        return Math.ceil(diff / (1000 * 60 * 60 * 24));
    })

    const trialDaysRemainingRatio = computed(() => {
        const remaining = trialDaysRemaining.value;
        const available = Math.max(remaining, 14);

        if (available > 0) {
            return (remaining / available) * 100;
        }

        return 0;
    })

    const currentUsageCredits = computed(() => {
        return workspace.value?.current_usage_credits || 0.0
    })

    const availableUsageCredits = computed(() => {
        return workspace.value?.available_usage_credits || 0.0
    })

    const remainingAvailableUsageCredits = computed(() => {
        return availableUsageCredits.value - currentUsageCredits.value
    })

    const ratioUsageCredits = computed(() => {
        return availableUsageCredits.value > 0 ? (remainingAvailableUsageCredits.value / availableUsageCredits.value) * 100 : 0.0
    })

    const planAvailableUsageCredits = computed(() => {
        return workspace.value?.plan_available_usage_credits || 0.0
    })

    const planCurrentUsageCredits = computed(() => {
        return workspace.value?.plan_current_usage_credits || 0.0
    })

    const remainingPlanAvailableUsageCredits = computed(() => {
        return planAvailableUsageCredits.value - planCurrentUsageCredits.value
    })

    const ratioPlanUsageCredits = computed(() => {
        return planAvailableUsageCredits.value > 0 ? (remainingPlanAvailableUsageCredits.value / planAvailableUsageCredits.value) * 100 : 0.0
    })

    const packAvailableUsageCredits = computed(() => {
        return workspace.value?.pack_available_usage_credits || 0.0
    })

    const packCurrentUsageCredits = computed(() => {
        return workspace.value?.pack_current_usage_credits || 0.0
    })

    const remainingPackAvailableUsageCredits = computed(() => {
        return packAvailableUsageCredits.value - packCurrentUsageCredits.value
    })

    const ratioPackUsageCredits = computed(() => {
        return packAvailableUsageCredits.value > 0 ? (remainingPackAvailableUsageCredits.value / packAvailableUsageCredits.value) * 100 : 0.0
    })

    async function fetchWorkspace(force = false) {
        if (!authStore.isAuthenticated || loading.value || (workspace.value && !force)) return

        loading.value = true
        error.value = null
        try {
            const response = await fetcher.get(`/workspace`)
            setWorkspace(response.data)
        } catch (err) {
            console.error('Erreur lors du chargement du workspace:', err)
            error.value = err
        } finally {
            loading.value = false
        }
    }

    function setWorkspace(newWorkspace) {
        workspace.value = newWorkspace
    }

    async function updateWorkspaceName(name) {
        if (!workspace.value) return

        loading.value = true
        error.value = null
        try {
            const response = await fetcher.patch(`/workspace`, { name })
            setWorkspace(response.data)
        } catch (err) {
            console.error('Erreur lors de la mise à jour du nom du workspace:', err)
            error.value = err
        } finally {
            loading.value = false
        }
    }

    async function updateWorkspace(data) {
        if (!workspace.value) return

        loading.value = true
        error.value = null
        try {
            const response = await fetcher.patch(`/workspace`, data)
            setWorkspace(response.data)
        } catch (err) {
            console.error('Erreur lors de la mise à jour du workspace:', err)
            error.value = err
        } finally {
            loading.value = false
        }
    }

    async function updateWorkspaceImage(file) {
        if (!workspace.value) return

        loading.value = true
        error.value = null
        const formData = new FormData()
        formData.append('file', file)

        try {
            const response = await fetcher.post(`/workspace/upload-image`, formData)
            setWorkspace(response.data)
        } catch (err) {
            console.error('Erreur lors de la mise à jour de l\'image du workspace:', err?.data, err)
            error.value = err
        } finally {
            loading.value = false
        }
    }

    watch(() => authStore.currentUser, async (user) => {
        if (user) {
            await fetchWorkspace()
        }
    })

    watch(() => isValid.value, async (valid) => {
        if (!valid) {
            bus.trigger('workspace:invalid-license')
        }
    })

    return {
        workspace,
        name,
        hasPlan,
        isValid,
        isTrial,
        trialDaysRemaining,
        trialDaysRemainingRatio,
        currentUsageCredits,
        availableUsageCredits,
        remainingAvailableUsageCredits,
        ratioUsageCredits,
        planAvailableUsageCredits,
        planCurrentUsageCredits,
        remainingPlanAvailableUsageCredits,
        ratioPlanUsageCredits,
        packAvailableUsageCredits,
        packCurrentUsageCredits,
        remainingPackAvailableUsageCredits,
        ratioPackUsageCredits,
        loading,
        error,
        fetchWorkspace,
        setWorkspace,
        updateWorkspaceName,
        updateWorkspace,
        updateWorkspaceImage,
    }
})
