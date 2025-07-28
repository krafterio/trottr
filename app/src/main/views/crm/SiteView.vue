<template>
    <div class="h-full flex flex-col bg-neutral-100" v-if="site">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-start space-x-2">
                    <Button variant="outline" @click="$router.go(-1)" class="h-9 w-9">
                        <ArrowLeft :size="20" />
                    </Button>
                    <template v-if="isDirty">
                        <Button @click="saveSite" variant="outline" :disabled="loading" class="w-9">
                            <Save class="h-4 w-4" />
                        </Button>
                        <Button variant="outline" @click="handleCancel" :disabled="loading" class="w-9">
                            <RotateCcw class="h-4 w-4" />
                        </Button>
                    </template>
                </div>
                <div class="flex items-center space-x-3">
                    <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                            <Button variant="outline" class="h-9 w-9">
                                <MoreHorizontal :size="20" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem @click="handleDelete">
                                <Trash class="h-4 w-4 text-destructive" />
                                Supprimer
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div class="w-full lg:w-1/4 xl:w-[500px] bg-white border-r overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-lg font-semibold text-neutral-900 mb-4">Informations générales</h2>

                    <form @submit.prevent="saveSite" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Nom du site</label>
                            <Input v-model="siteForm.name" class="mt-1" @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Type de bâtiment</label>
                            <Select v-model="siteForm.building_type" class="mt-1" @update:model-value="checkDirty">
                                <SelectTrigger class="w-full">
                                    <SelectValue placeholder="Sélectionner un type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem v-for="option in getSiteBuildingTypeOptions()" :key="option.value"
                                        :value="option.value">
                                        {{ option.label }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Entreprise associée</label>
                            <div class="mt-1">
                                <CompanySelect v-model="siteForm.company" placeholder="Sélectionner une entreprise..."
                                    clearable @update:model-value="checkDirty" />
                            </div>
                        </div>

                        <Separator class="my-6" />

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Adresse</label>
                                <Input v-model="siteForm.street" class="mt-1" @input="checkDirty" />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Complément d'adresse</label>
                                <Input v-model="siteForm.street_2" class="mt-1" @input="checkDirty" />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Code postal</label>
                                <Input v-model="siteForm.zip" class="mt-1" @input="checkDirty" />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Ville</label>
                                <Input v-model="siteForm.city" class="mt-1" @input="checkDirty" />
                            </div>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Pays</label>
                            <div class="mt-1">
                                <CountrySelect v-model="siteForm.country" placeholder="Sélectionner un pays..."
                                    clearable @update:model-value="checkDirty" />
                            </div>
                        </div>

                        <Separator class="my-6" />

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Informations d'accès</label>
                            <Textarea v-model="siteForm.access_info" class="mt-1" rows="3"
                                placeholder="Code portail, interphone, instructions d'accès..." @input="checkDirty" />
                        </div>
                    </form>
                </div>
            </div>

            <div class="flex-1 bg-neutral-50 overflow-y-auto">
                <div class="p-6">
                    <div class="bg-white mb-4 rounded-lg border">
                        <div class="p-6">
                            <div class="flex items-start justify-between">
                                <div class="flex items-start space-x-2">
                                    <MapPinIcon class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                    <div class="flex flex-col gap-1">
                                        <h1 class="text-2xl font-semibold">{{ site.name }}</h1>
                                        <div class="flex gap-2">
                                            <Badge variant="outline">
                                                <Building class="h-4 w-4" />
                                                {{ getSiteBuildingTypeLabel(site.building_type) }}
                                            </Badge>
                                            <Badge variant="outline" v-if="site.company">
                                                <Building2 class="h-4 w-4" />
                                                {{ site.company.name }}
                                            </Badge>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 gap-4 mb-4"
                        :class="{ 'grid-cols-2': workspaceStore.workspace?.use_subsites }">
                        <div class="bg-white p-4 rounded-lg border">
                            <div class="text-2xl font-semibold text-neutral-900">{{ kpis.totalInterventions }}</div>
                            <div class="text-sm text-neutral-600">Interventions</div>
                        </div>
                        <div v-if="workspaceStore.workspace?.use_subsites" class="bg-white p-4 rounded-lg border">
                            <div class="text-2xl font-semibold text-neutral-900">{{ kpis.totalLots }}</div>
                            <div class="text-sm text-neutral-600">Lots/Logements</div>
                        </div>
                    </div>

                    <Tabs default-value="interventions" class="w-full">
                        <TabsList class="grid w-full mb-3 bg-neutral-200"
                            :class="workspaceStore.workspace?.use_subsites ? 'grid-cols-2' : 'grid-cols-1'">
                            <TabsTrigger value="interventions" class="flex items-center space-x-2">
                                <Wrench class="h-4 w-4" />
                                <span>Interventions</span>
                            </TabsTrigger>
                            <TabsTrigger v-if="workspaceStore.workspace?.use_subsites" value="lots"
                                class="flex items-center space-x-2">
                                <Building class="h-4 w-4" />
                                <span>Lots</span>
                            </TabsTrigger>
                        </TabsList>

                        <TabsContent value="interventions">
                            <div class="bg-white rounded-lg border">
                                <div class="px-6 py-4 border-b">
                                    <div class="flex items-center justify-between">
                                        <h3 class="text-lg font-semibold text-neutral-900">Interventions</h3>
                                        <Button size="sm">
                                            <Plus class="h-4 w-4" />
                                            Programmer une intervention
                                        </Button>
                                    </div>
                                </div>
                                <div class="p-6 text-center text-neutral-500">
                                    <Wrench class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
                                    <p>Fonctionnalité à venir</p>
                                    <p class="text-sm">La gestion des interventions sera bientôt disponible</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent v-if="workspaceStore.workspace?.use_subsites" value="lots">
                            <div class="bg-white rounded-lg border">
                                <div class="px-6 py-4 border-b">
                                    <div class="flex items-center justify-between">
                                        <h3 class="text-lg font-semibold text-neutral-900">Lots</h3>
                                        <Button size="sm">
                                            <Plus class="h-4 w-4" />
                                            Ajouter un lot
                                        </Button>
                                    </div>
                                </div>
                                <div class="p-6 text-center text-neutral-500">
                                    <Building class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
                                    <p>Fonctionnalité à venir</p>
                                    <p class="text-sm">Les lots et logements seront bientôt disponibles</p>
                                </div>
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
        </div>
    </div>

    <div v-else-if="loading" class="h-full flex items-center justify-center">
        <div class="text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-neutral-900 mx-auto mb-4"></div>
            <p class="text-neutral-600">Chargement du site...</p>
        </div>
    </div>

    <div v-else class="h-full flex items-center justify-center">
        <div class="text-center">
            <MapPin class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
            <p class="text-neutral-600">Site non trouvé</p>
            <Button @click="$router.go(-1)" class="mt-4">Retour</Button>
        </div>
    </div>
</template>

<script setup>
import { CompanySelect } from '@/common/components/form/company-select'
import { CountrySelect } from '@/common/components/form/country-select'
import { Button } from '@/common/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { Textarea } from '@/common/components/ui/textarea'
import { useFetcher } from '@/common/composables/fetcher'

import Badge from '@/common/components/ui/badge/Badge.vue'
import { bus, useBus } from '@/common/composables/bus'
import { useSite } from '@/common/composables/useSite'

import { useWorkspaceStore } from '@/main/stores/workspace'
import {
    ArrowLeft,
    Building,
    Building2,
    MapPin,
    MapPinIcon,
    MoreHorizontal,
    Plus,
    RotateCcw,
    Save,
    Trash,
    Wrench
} from 'lucide-vue-next'
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const route = useRoute()
const router = useRouter()
const fetcher = useFetcher()
const { getSiteBuildingTypeLabel, getSiteBuildingTypeOptions } = useSite()
const workspaceStore = useWorkspaceStore()

const site = ref(null)
const loading = ref(false)
const siteId = route.params.id

const siteForm = reactive({
    name: '',
    building_type: '',
    street: '',
    street_2: '',
    zip: '',
    city: '',
    access_info: ''
})

const kpis = reactive({
    totalLots: 0,
    totalInterventions: 0
})

const isDirty = ref(false)

// Écoute la confirmation de suppression
useBus(bus, 'confirm-delete-site:confirmed', () => {
    deleteSite()
})

const fetchSite = async () => {
    if (!siteId) return

    loading.value = true
    try {
        const response = await fetcher.get(`/sites/${siteId}`)
        site.value = response.data

        Object.assign(siteForm, {
            name: site.value.name || '',
            building_type: site.value.building_type || '',
            street: site.value.street || '',
            street_2: site.value.street_2 || '',
            zip: site.value.zip || '',
            city: site.value.city || '',
            access_info: site.value.access_info || '',
            company: site.value.company || null,
            country: site.value.country || null
        })

        kpis.totalLots = 0
        kpis.totalInterventions = 0

        isDirty.value = false

    } catch (error) {
        console.error('Erreur lors du chargement du site:', error)
        toast.error('Erreur lors du chargement du site')
    } finally {
        loading.value = false
    }
}

const saveSite = async () => {
    if (!site.value) return

    loading.value = true
    try {
        const updateData = {
            ...siteForm,
            company: siteForm.company?.id || null,
            country: siteForm.country?.id || null
        }

        const response = await fetcher.patch(`/sites/${site.value.id}`, updateData)
        site.value = response.data
        toast.success('Site mis à jour avec succès')
        isDirty.value = false
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error('Erreur lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}

const handleCancel = () => {
    if (site.value) {
        Object.assign(siteForm, {
            name: site.value.name || '',
            building_type: site.value.building_type || '',
            street: site.value.street || '',
            street_2: site.value.street_2 || '',
            zip: site.value.zip || '',
            city: site.value.city || '',
            access_info: site.value.access_info || '',
            company: site.value.company || null,
            country: site.value.country || null
        })
        isDirty.value = false
    }
}

const handleDelete = () => {
    if (!site.value) return

    bus.trigger('confirm-delete', {
        title: 'Supprimer le site',
        message: 'Êtes-vous sûr de vouloir supprimer ce site ?',
        itemName: site.value.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-site:confirmed'
    })
}

const deleteSite = async () => {
    if (!site.value) return

    try {
        await fetcher.delete(`/sites/${site.value.id}`)
        toast.success('Site supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        router.push('/sites')
    } catch (error) {
        console.error('Erreur lors de la suppression du site:', error)
        toast.error('Erreur lors de la suppression du site')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const checkDirty = () => {
    const originalValues = {
        name: site.value?.name || '',
        building_type: site.value?.building_type || '',
        street: site.value?.street || '',
        street_2: site.value?.street_2 || '',
        zip: site.value?.zip || '',
        city: site.value?.city || '',
        access_info: site.value?.access_info || '',
        company: site.value?.company || null,
        country: site.value?.country || null
    }

    const currentValues = {
        name: siteForm.name,
        building_type: siteForm.building_type,
        street: siteForm.street,
        street_2: siteForm.street_2,
        zip: siteForm.zip,
        city: siteForm.city,
        access_info: siteForm.access_info,
        company: siteForm.company,
        country: siteForm.country
    }

    isDirty.value = JSON.stringify(originalValues) !== JSON.stringify(currentValues)
}

onMounted(() => {
    fetchSite()
})
</script>