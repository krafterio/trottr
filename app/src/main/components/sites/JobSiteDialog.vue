<template>
    <Dialog :open="isOpen" @update:open="handleClose">
        <DialogContent class="sm:max-w-[625px]">
            <DialogHeader>
                <DialogTitle>Modifier le site d'intervention</DialogTitle>
                <DialogDescription>
                    Sélectionnez un nouveau site pour cette intervention.
                </DialogDescription>
            </DialogHeader>
            <div class="grid gap-4 py-4">
                <div class="flex items-center justify-between">
                    <div class="space-y-0.5">
                        <Label class="text-sm font-medium">Filtrer uniquement les sites rattachés au client</Label>
                        <p class="text-xs text-neutral-500">Limite la recherche aux sites du client actuel</p>
                    </div>
                    <Switch v-model="filterSitesByClient" />
                </div>

                <Separator />

                <div class="grid gap-2">
                    <Label for="site">Site d'intervention</Label>
                    <SiteSelect v-model="siteForm.site" class="w-full" placeholder="Sélectionner un site"
                        :company-id="filterSitesByClient && customerCompany ? customerCompany.id : null"
                        :contact-id="filterSitesByClient && customerContact ? customerContact.id : null" />
                </div>

                <div v-if="!selectedSite" class="border rounded-lg p-4 bg-neutral-50">
                    <div class="flex items-center gap-2 mb-2">
                        <Info class="h-4 w-4 text-neutral-500" />
                        <h4 class="text-sm font-medium text-neutral-900">Aucun site sélectionné</h4>
                    </div>
                    <div class="text-sm text-neutral-600 space-y-1">
                        <p>Sélectionnez un site pour voir ses détails ici.</p>
                        <p v-if="filterSitesByClient" class="text-xs text-neutral-500">
                            Seuls les sites rattachés au client sont affichés.
                        </p>
                        <p v-else class="text-xs text-neutral-500">
                            Tous les sites sont disponibles pour la sélection.
                        </p>
                    </div>
                </div>

                <div v-if="selectedSite" class="border rounded-lg p-4 bg-neutral-50">
                    <div class="flex items-center justify-between mb-2">
                        <h4 class="text-sm font-medium text-neutral-900">Aperçu du site</h4>
                        <Button variant="outline" size="sm" @click="openSiteEditDialog">
                            <Edit class="h-3 w-3" />
                            Éditer
                        </Button>
                    </div>
                    <div class="text-sm text-neutral-600 space-y-1">
                        <p v-if="selectedSite.name" class="font-medium">{{ selectedSite.name }}</p>
                        <p v-if="selectedSite.street">{{ selectedSite.street }}</p>
                        <p v-if="selectedSite.street_2">{{ selectedSite.street_2 }}</p>
                        <p v-if="selectedSite.zip && selectedSite.city">{{ selectedSite.zip }} {{ selectedSite.city }}
                        </p>
                        <p v-if="selectedSite.country">{{ selectedSite.country.name }}</p>
                    </div>
                </div>
            </div>
            <DialogFooter>
                <Button variant="outline" @click="handleClose">Annuler</Button>
                <Button @click="saveSite" :disabled="loading">Enregistrer</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import SiteSelect from '@/common/components/form/site-select/SiteSelect.vue'
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import Label from '@/common/components/ui/label/Label.vue'
import Separator from '@/common/components/ui/separator/Separator.vue'
import { Switch } from '@/common/components/ui/switch'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { Edit, Info } from 'lucide-vue-next'
import { ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const isOpen = ref(false)
const job = ref(null)
const customerCompany = ref(null)
const customerContact = ref(null)
const currentSite = ref(null)
const siteForm = ref({
    site: null
})
const selectedSite = ref(null)
const filterSitesByClient = ref(true)
const loading = ref(false)

const fetcher = useFetcher()

const handleClose = () => {
    isOpen.value = false
    job.value = null
    customerCompany.value = null
    customerContact.value = null
    currentSite.value = null
    siteForm.value.site = null
    selectedSite.value = null
    filterSitesByClient.value = true
}

const openSiteEditDialog = async () => {
    if (selectedSite.value) {
        try {
            const response = await fetcher.get(`/sites/${selectedSite.value.id}`)
            const siteData = response.data

            bus.trigger('open-site-dialog', {
                id: siteData.id,
                name: siteData.name,
                building_type: siteData.building_type,
                street: siteData.street,
                street_2: siteData.street_2,
                zip: siteData.zip,
                city: siteData.city,
                country: siteData.country,
                company: siteData.company,
                contact: siteData.contact
            })
            handleClose()
        } catch (error) {
            console.error('Erreur lors du chargement du site:', error)
            toast.error('Erreur lors du chargement du site')
        }
    }
}

const saveSite = async () => {
    loading.value = true
    try {
        const jobId = job.value.id
        const siteId = siteForm.value.site?.id || siteForm.value.site
        await fetcher.patch(`/jobs/${jobId}`, { site: siteId })
        toast.success('Site d\'intervention modifié avec succès')

        // Émettre l'événement pour mettre à jour le job
        bus.trigger('job-site-updated', { jobId, siteId })

        handleClose()
    } catch (error) {
        console.error('Erreur lors de la sauvegarde du site:', error)
        toast.error('Erreur lors de la sauvegarde du site')
    } finally {
        loading.value = false
    }
}

watch(() => siteForm.value.site, async (newSite) => {
    if (newSite && newSite.id) {
        try {
            const response = await fetcher.get(`/sites/${newSite.id}`)
            selectedSite.value = response.data
        } catch (error) {
            console.error('Erreur lors du chargement du site:', error)
            selectedSite.value = null
        }
    } else {
        selectedSite.value = null
    }
})

watch(() => filterSitesByClient.value, () => {
    // Réinitialiser le site sélectionné quand le filtre change
    siteForm.value.site = null
    selectedSite.value = null
})

// Écouter l'ouverture de la dialog
useBus(bus, 'open-job-site-dialog', (data) => {
    const dialogData = data.detail || data

    job.value = dialogData.job

    customerCompany.value = dialogData.customerCompany
    customerContact.value = dialogData.customerContact
    currentSite.value = dialogData.currentSite

    siteForm.value.site = currentSite.value || null
    selectedSite.value = currentSite.value || null
    filterSitesByClient.value = true
    isOpen.value = true
})

// Écouter la création d'un nouveau site
useBus(bus, 'site-saved', (event) => {
    console.log('JobSiteDialog - site-saved reçu:', event)
    console.log('JobSiteDialog - event.detail:', event.detail)

    const siteData = event.detail || event
    console.log('JobSiteDialog - siteData extrait:', siteData)
    console.log('JobSiteDialog - isOpen.value:', isOpen.value)
    console.log('JobSiteDialog - siteData.id:', siteData?.id)

    // Si un site vient d'être créé et qu'on est dans la dialog
    if (isOpen.value && siteData && siteData.id) {
        console.log('JobSiteDialog - Dialog ouverte et site créé')

        // Vérifier que le site correspond aux filtres actuels
        const isCompatible = (
            (customerCompany.value && siteData.company?.id === customerCompany.value.id) ||
            (customerContact.value && siteData.contact?.id === customerContact.value.id) ||
            (!customerCompany.value && !customerContact.value)
        )

        console.log('JobSiteDialog - customerCompany.value:', customerCompany.value)
        console.log('JobSiteDialog - customerContact.value:', customerContact.value)
        console.log('JobSiteDialog - siteData.company:', siteData.company)
        console.log('JobSiteDialog - siteData.contact:', siteData.contact)
        console.log('JobSiteDialog - isCompatible:', isCompatible)

        if (isCompatible) {
            console.log('JobSiteDialog - Site compatible, mise à jour...')
            console.log('JobSiteDialog - Ancien siteForm.value.site:', siteForm.value.site)
            siteForm.value.site = siteData.id
            selectedSite.value = siteData
            console.log('JobSiteDialog - Nouveau siteForm.value.site:', siteForm.value.site)
            console.log('JobSiteDialog - Nouveau selectedSite.value:', selectedSite.value)
        } else {
            console.log('JobSiteDialog - Site non compatible')
        }
    } else {
        console.log('JobSiteDialog - Conditions non remplies pour la mise à jour')
    }
})

// Watcher pour synchroniser selectedSite avec siteForm.site
watch(() => siteForm.value.site, async (newSiteId) => {
    console.log('JobSiteDialog - siteForm.site changé:', newSiteId)
    if (newSiteId) {
        try {
            const response = await fetcher.get(`/sites/${newSiteId}`)
            selectedSite.value = response.data
            console.log('JobSiteDialog - selectedSite mis à jour:', selectedSite.value)
        } catch (error) {
            console.error('Erreur lors de la récupération du site:', error)
            selectedSite.value = null
        }
    } else {
        selectedSite.value = null
    }
}, { immediate: true })
</script>