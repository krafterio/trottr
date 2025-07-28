<template>
    <div class="p-6">
        <div v-if="loading" class="text-center py-8">
            <div class="animate-spin w-8 h-8 border-2 border-neutral-300 border-t-neutral-900 rounded-full mx-auto">
            </div>
            <p class="text-neutral-600 mt-4">Chargement des sites...</p>
        </div>

        <div v-else-if="sites.length === 0" class="text-center py-8">
            <MapPin class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-neutral-900 mb-2">Aucun site</h3>
            <p class="text-neutral-600 mb-4">Cette entreprise n'a pas encore de sites d'intervention associés.</p>
            <Button @click="handleCreateSite" class="inline-flex items-center">
                <Plus class="w-4 h-4" />
                Ajouter un site
            </Button>
        </div>

        <div v-else class="space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="text-lg font-medium text-neutral-900">Sites d'intervention ({{ sites.length }})</h3>
                <Button @click="handleCreateSite" size="sm" class="inline-flex items-center">
                    <Plus class="w-4 h-4" />
                    Ajouter un site
                </Button>
            </div>

            <div class="border rounded-lg overflow-hidden">
                <table class="w-full">
                    <thead class="bg-neutral-50 border-b">
                        <tr>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Nom du site
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Type
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Adresse
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Ville
                            </th>
                            <th
                                class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-neutral-200">
                        <tr v-for="site in sites" :key="site.id" class="hover:bg-neutral-50">
                            <td class="px-4 py-3">
                                <div class="text-sm font-medium text-neutral-900">{{ site.name }}</div>
                            </td>
                            <td class="px-4 py-3">
                                <Badge variant="outline">{{ getSiteBuildingTypeLabel(site.building_type) }}</Badge>
                            </td>
                            <td class="px-4 py-3">
                                <div class="text-sm text-neutral-900">{{ site.street }}</div>
                                <div v-if="site.street_2" class="text-sm text-neutral-500">{{ site.street_2 }}</div>
                            </td>
                            <td class="px-4 py-3">
                                <div class="text-sm text-neutral-900">{{ site.zip }} {{ site.city }}</div>
                                <div v-if="site.country" class="text-sm text-neutral-500">{{ site.country.name }}</div>
                            </td>
                            <td class="px-4 py-3">
                                <div class="flex items-center space-x-2">
                                    <Button variant="ghost" size="sm" @click="viewSite(site)">
                                        <Eye class="w-4 h-4" />
                                    </Button>
                                    <Button variant="ghost" size="sm" @click="editSite(site)">
                                        <Edit class="w-4 h-4" />
                                    </Button>
                                    <Button variant="ghost" size="sm" @click="deleteSite(site)">
                                        <Trash class="w-4 h-4 text-destructive" />
                                    </Button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useSite } from '@/common/composables/useSite'
import { Edit, Eye, MapPin, Plus, Trash } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
    companyId: {
        type: Number,
        default: null
    },
    contactId: {
        type: Number,
        default: null
    },
    attachmentType: {
        type: String,
        default: 'company',
        validator: (value) => ['company', 'contact'].includes(value)
    }
})

const fetcher = useFetcher()
const { getSiteBuildingTypeLabel } = useSite()

const sites = ref([])
const loading = ref(false)

const fetchSites = async () => {
    const entityId = props.attachmentType === 'company' ? props.companyId : props.contactId
    if (!entityId) return

    loading.value = true
    try {
        const params = {}
        if (props.attachmentType === 'company') {
            params.company = props.companyId
        } else {
            params.contact = props.contactId
        }

        const response = await fetcher.get('/sites', { params })
        sites.value = response.data.items || []
    } catch (error) {
        console.error('Erreur lors du chargement des sites:', error)
        toast.error('Erreur lors du chargement des sites')
    } finally {
        loading.value = false
    }
}

const handleCreateSite = () => {
    const data = { attachmentType: props.attachmentType }
    if (props.attachmentType === 'company') {
        data.company = props.companyId
    } else {
        data.contact = props.contactId
    }
    bus.trigger('open-site-dialog', data)
}

const viewSite = (site) => {
    console.log('View site:', site)
}

const editSite = (site) => {
    const data = { ...site, attachmentType: props.attachmentType }
    bus.trigger('open-site-dialog', data)
}

const deleteSite = (site) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le site',
        message: 'Êtes-vous sûr de vouloir supprimer ce site ?',
        itemName: site.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-site:confirmed'
    })

    selectedSiteForDelete.value = site
}

const selectedSiteForDelete = ref(null)

const performDeleteSite = async () => {
    if (!selectedSiteForDelete.value) return

    try {
        await fetcher.delete(`/sites/${selectedSiteForDelete.value.id}`)
        toast.success('Site supprimé avec succès')
        fetchSites()

        // Notifier la vue parente que le site a été supprimé
        bus.trigger('site:deleted', {
            siteId: selectedSiteForDelete.value.id,
            siteName: selectedSiteForDelete.value.name
        })

        selectedSiteForDelete.value = null
        bus.trigger('confirm-delete-dialog:close')
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}



useBus(bus, 'confirm-delete-site:confirmed', () => {
    performDeleteSite()
})

useBus(bus, 'site-saved', () => {
    fetchSites()
})

useBus(bus, 'site-created-stay', () => {
    fetchSites()
})

watch(() => [props.companyId, props.contactId, props.attachmentType], () => {
    const entityId = props.attachmentType === 'company' ? props.companyId : props.contactId
    if (entityId) {
        fetchSites()
    }
}, { immediate: true })

onMounted(() => {
    fetchSites()
})
</script>