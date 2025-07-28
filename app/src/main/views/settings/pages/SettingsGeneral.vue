<template>
    <div class="max-w-5xl space-y-8">
        <div>
            <h2 class="text-lg font-semibold text-neutral-900">Votre entreprise</h2>
            <p class="text-neutral-600">Informations sur votre entreprise.</p>
        </div>

        <div class="space-y-6">

            <div class="space-y-6">
                <div class="space-y-2">
                    <Label for="company-name">Raison sociale</Label>
                    <Input id="company-name" v-model="formData.name" placeholder="Nom de votre entreprise" />
                </div>

                <div class="space-y-2">
                    <Label for="street">Rue</Label>
                    <Input id="street" v-model="formData.street" placeholder="123 rue de la République" />
                </div>

                <div class="space-y-2">
                    <Label for="street2">Rue 2 (optionnel)</Label>
                    <Input id="street2" v-model="formData.street2" placeholder="Appartement, étage, etc." />
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="postal-code">Code postal</Label>
                        <Input id="postal-code" v-model="formData.zip" placeholder="75001" />
                    </div>
                    <div class="space-y-2">
                        <Label for="city">Ville</Label>
                        <Input id="city" v-model="formData.city" placeholder="Paris" />
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="country">Pays</Label>
                    <CountrySelect v-model="selectedCountry" />
                </div>
            </div>

            <Separator />

            <!-- Section Informations légales -->
            <div>
                <h2 class="text-lg font-semibold text-neutral-900">Informations légales</h2>
                <p class="text-neutral-600">Informations légales et fiscales de votre entreprise.</p>
            </div>

            <div class="space-y-6">
                <div class="space-y-2">
                    <Label for="siren">Numéro de SIREN</Label>
                    <Input id="siren" v-model="formData.siren" placeholder="123 456 789" />
                    <p class="text-sm text-neutral-500">
                        Numéro d'identification unique de votre entreprise (9 chiffres).
                    </p>
                </div>

                <div class="space-y-2">
                    <Label for="tva">Numéro de TVA</Label>
                    <Input id="tva" v-model="formData.vat" placeholder="FR 12 345678901" />
                    <p class="text-sm text-neutral-500">
                        Numéro de TVA intracommunautaire (optionnel).
                    </p>
                </div>
            </div>

            <Separator />

            <div class="flex justify-end">
                <Button @click="updateProfile" :disabled="loading">
                    {{ loading ? 'Mise à jour en cours...' : 'Mettre à jour le profil' }}
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import CountrySelect from '@/common/components/ui/country-select/CountrySelect.vue'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Separator } from '@/common/components/ui/separator'
import { useFetcher } from '@/common/composables/fetcher'
import { useAuthStore } from '@/common/stores/auth'
import { useWorkspaceStore } from '@/main/stores/workspace'
import { computed, onMounted, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const authStore = useAuthStore()
const workspaceStore = useWorkspaceStore()
const fetcher = useFetcher()

const loading = ref(false)

const formData = ref({
    name: '',
    street: '',
    street2: '',
    zip: '',
    city: '',
    country_id: null,
    siren: '',
    vat: ''
})

const selectedCountry = ref(null)

const workspace = computed(() => workspaceStore.workspace)

const loadWorkspaceData = () => {
    if (workspace.value) {
        formData.value = {
            name: workspace.value.name || '',
            street: workspace.value.street || '',
            street2: workspace.value.street2 || '',
            zip: workspace.value.zip || '',
            city: workspace.value.city || '',
            country_id: workspace.value.country?.id || null,
            siren: workspace.value.siren || '',
            vat: workspace.value.vat || ''
        }
        selectedCountry.value = workspace.value.country || null
    }
}

const updateProfile = async () => {
    try {
        loading.value = true

        const dataToSend = {
            ...formData.value,
            country_id: selectedCountry.value?.id || null
        }

        await workspaceStore.updateWorkspace(dataToSend)

        toast.success('Profil mis à jour avec succès !')
    } catch (error) {
        console.error('Erreur lors de la mise à jour:', error)
        toast.error('Erreur lors de la mise à jour du profil')
    } finally {
        loading.value = false
    }
}

onMounted(async () => {
    await workspaceStore.fetchWorkspace()
    loadWorkspaceData()
})

watch(workspace, () => {
    loadWorkspaceData()
}, { deep: true })
</script>