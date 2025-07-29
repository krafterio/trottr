<template>
    <div v-if="loading" class="h-full flex items-center justify-center">
        <div class="text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p class="text-neutral-600">Chargement de l'intervention...</p>
        </div>
    </div>

    <div v-else class="h-full flex flex-col bg-neutral-100">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <Button v-if="!inDialog" variant="outline" @click="$router.go(-1)" class="h-9 w-9">
                        <ArrowLeft :size="20" />
                    </Button>
                    <div class="flex flex-col gap-1">
                        <div class="flex items-center space-x-3">
                            <h1 class="text-xl text-neutral-900 font-mono">{{ job?.reference || 'Chargement...' }}</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge v-if="job?.status" class="bg-green-100 text-green-800">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                {{ job.status.name }}
                            </Badge>
                            <Badge v-if="!job?.operator" class="bg-yellow-50 text-yellow-700">
                                <User class="h-4 w-4" />
                                À assigner
                            </Badge>
                            <Badge v-if="job?.category" variant="outline">
                                <Folder class="h-4 w-4" />
                                {{ job.category.name }}
                            </Badge>
                            <Badge v-if="job?.scheduled_start" variant="outline">
                                <Calendar class="h-4 w-4" />
                                {{ formatDate(job.scheduled_start) }}
                            </Badge>
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <CalendarArrowUp class="h-4 w-4" />
                        Replanifier
                    </Button>
                    <Button variant="outline">
                        <UserPlus class="h-4 w-4" />
                        Assigner technicien
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Action
                        <ChevronDown class="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div :class="inDialog ? 'flex-1 overflow-y-auto p-6 bg-accent' : 'flex-1 p-6 overflow-y-auto'">
                <Card class="mb-6 py-0">
                    <CardContent class="px-5 py-4">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex items-start space-x-2">
                                <ScanSearch class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                <div class="flex flex-col">
                                    <h1 class="text-2xl font-semibold">{{ job?.name || 'Chargement...' }}</h1>
                                    <p class="text-neutral-600">{{ getClientName() }} • {{
                                        getClientAddress().split(',')[0] }}
                                    </p>
                                </div>
                            </div>
                            <Badge v-if="job?.status" class="bg-green-100 text-green-800">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                {{ job.status.name }}
                            </Badge>
                        </div>

                        <div class="grid grid-cols-3 gap-4 mb-4 ps-11">
                            <div class="flex items-start space-x-3">
                                <Calendar class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ job?.scheduled_start ?
                                        formatDate(job.scheduled_start) : 'Non planifié' }}</p>
                                    <p class="text-xs text-neutral-500">Début prévu</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <Clock class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ getDuration() }}</p>
                                    <p class="text-xs text-neutral-500">Durée prévue</p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-4 pt-4 border-t border-dashed ps-11">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="flex items-center space-x-2" v-if="job?.site">
                                        <MapPin class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ getClientAddress().split(',')[1] }},
                                            {{
                                                getClientAddress().split(',')[2] }}</span>
                                    </div>
                                    <Badge class="flex items-center bg-yellow-100 text-yellow-900" v-else>
                                        <MapPin class="h-4 w-4" />
                                        <span class="text-sm">Adresse non définie</span>
                                    </Badge>

                                    <Badge v-if="job?.priority" class="flex items-center space-x-1"
                                        :class="getPriorityConfig(job.priority).bgColor + ' ' + getPriorityConfig(job.priority).color">
                                        <AlertTriangle class="h-4 w-4" />
                                        <span class="text-sm">{{ getPriorityConfig(job.priority).label }}</span>
                                    </Badge>
                                </div>
                                <div class="flex gap-2">
                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            <Button variant="outline">
                                                <AlertTriangle class="h-4 w-4 text-orange-500" />
                                                Signaler intervention
                                                <ChevronDown class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem>
                                                <UserRoundX class="h-4 w-4 text-orange-500" />
                                                Absence contact
                                            </DropdownMenuItem>
                                            <DropdownMenuItem>
                                                <ShieldAlert class="h-4 w-4 text-orange-500" />
                                                Intervention impossible
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>

                                    <Button>
                                        <Play class="h-3 w-3 fill-current" />
                                        Démarrer
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <div class="bg-white rounded-lg border">
                    <Tabs default-value="historique" class="border-b p-4 py-3">
                        <TabsList>
                            <TabsTrigger value="historique">Historique</TabsTrigger>
                            <TabsTrigger value="operations">Opérations</TabsTrigger>
                            <TabsTrigger value="pieces">Pièces détachées</TabsTrigger>
                            <TabsTrigger value="rapports">Rapports</TabsTrigger>
                            <TabsTrigger value="questionnaire">Questionnaire satisfaction</TabsTrigger>
                        </TabsList>

                        <TabsContent value="historique">

                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Historique</h2>
                                    <div class="flex items-center space-x-2">
                                        <Button variant="outline">
                                            <File class="h-4 w-4" />
                                            Ajouter une pièce jointe
                                        </Button>
                                        <Button variant="outline">
                                            <Plus class="h-4 w-4" />
                                            Ajouter une note
                                        </Button>
                                    </div>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">L'historique des interventions sera bientôt disponible</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="operations">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Opérations effectuées</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter une opération
                                    </Button>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La gestion des opérations sera bientôt disponible</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="pieces">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Pièces détachées utilisées</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter une pièce
                                    </Button>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La gestion des pièces détachées sera bientôt disponible</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="rapports">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Rapports d'intervention</h2>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La génération de rapports sera bientôt disponible</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="questionnaire">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Questionnaire de satisfaction
                                    </h2>
                                    <Badge class="bg-green-100 text-green-800">Complété</Badge>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">Les questionnaires de satisfaction seront bientôt
                                        disponibles</p>
                                </div>
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>

            <div v-if="!inDialog" class="w-140 bg-white border-l p-6 overflow-y-auto">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-neutral-900">Détails de l'intervention</h3>
                        <Button
                            class="bg-green-100 text-green-800 hover:bg-green-200 hover:text-green-900 cursor-pointer">
                            <Circle class="fill-current" style="height: 6px; width: 6px;" />
                            Planifié
                            <ChevronDown class="h-4 w-4" />
                        </Button>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <h4 class="text-sm font-medium text-neutral-700">Référence intervention</h4>
                            <p class="text-xl font-mono text-neutral-900">{{ job?.reference || 'Chargement...' }}</p>
                            <p class="text-xs text-neutral-400">Créé le {{ job?.created_at ? formatDate(job.created_at)
                                : 'Chargement...' }}</p>
                        </div>

                        <div class="bg-neutral-100 border rounded-lg p-3">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-sm font-medium text-neutral-700">Démarrage prévu</span>
                                <span class="text-sm text-neutral-900">{{ job?.scheduled_start ?
                                    formatDate(job.scheduled_start) : 'Non planifié' }}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-sm font-medium text-neutral-700">À terminer</span>
                                <div class="text-sm">
                                    <span class="text-neutral-900">{{ job?.scheduled_end ? formatDate(job.scheduled_end)
                                        : 'Non planifié' }}</span>
                                    <span class="text-neutral-600 ml-2">{{ getDuration() }}</span>
                                </div>
                            </div>
                        </div>


                        <Card class="p-4 gap-0 items-start relative">
                            <div class="flex absolute top-3 right-3 gap-2">
                                <Button variant="outline" class="h-8 w-8" size="icon" @click="openEditDialog">
                                    <Edit class="h-3 w-3" />
                                </Button>
                            </div>
                            <div class="flex items-center gap-1 mb-2">
                                <ScrollText class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Description de l'intervention</h4>
                            </div>
                            <p class="text-sm font-medium">{{ job?.name || 'Aucun sujet' }}</p>
                            <p class="text-sm text-neutral-600">{{ job?.description || 'Aucune description' }}</p>
                        </Card>

                        <Card class="p-4 gap-0 items-start relative">
                            <div class="flex absolute top-3 right-3 gap-2">
                                <Button variant="outline" class="h-8 w-8" size="icon" @click="openSiteDialog">
                                    <Edit class="h-3 w-3" />
                                </Button>

                                <Button variant="outline" class=" h-8 w-8" size="icon">
                                    <Map />
                                </Button>
                            </div>
                            <div class="flex items-center gap-1 mb-2">
                                <MapPinned class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Site d'intervention</h4>
                            </div>
                            <div class="text-sm text-neutral-600">
                                <p v-if="job?.site?.name" class="cursor-pointer hover:text-primary underline"
                                    @click="viewSite(job.site)">{{ job.site.name }}</p>
                                <p v-if="job?.site?.street">{{ job.site.street }}</p>
                                <p v-if="job?.site?.zip && job?.site?.city">{{ job.site.zip }} {{ job.site.city }}</p>
                                <p v-if="!job?.site">Aucun site défini</p>
                            </div>
                        </Card>

                        <Card
                            class="p-4 gap-0 border-dashed flex items-center justify-center cursor-pointer hover:bg-neutral-50">
                            <UserPlus class="h-10 w-10 mb-3 text-neutral-500" :stroke-width="1.2" />
                            <p class="text-sm text-neutral-500">Assigner un technicien</p>
                        </Card>

                        <Separator />

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Client commanditaire</Label>
                            <div class="col-span-2">
                                <CompanySelect v-if="job?.customer_company" v-model="job.customer_company.id"
                                    class="w-full" />
                                <ContactSelect v-else-if="job?.customer_contact" v-model="job.customer_contact.id"
                                    class="w-full" />
                                <div v-else class="text-sm text-neutral-500">Aucun client défini</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Priorité</Label>
                            <div class="col-span-2">
                                <PrioritySelect v-if="job?.priority" v-model="job.priority" class="w-full" />
                                <div v-else class="text-sm text-neutral-500">Priorité non définie</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Type d'intervention</Label>
                            <div class="col-span-2">
                                <CategorySelect v-if="job?.category" v-model="job.category.id" class="w-full" />
                                <div v-else class="text-sm text-neutral-500">Catégorie non définie</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Référence client</Label>
                            <div class="col-span-2">
                                <Input v-if="job?.customer_reference !== undefined" v-model="job.customer_reference"
                                    class="w-full" placeholder="Référence client" />
                                <div v-else class="text-sm text-neutral-500">Aucune référence client</div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>

    <Dialog :open="editDialogOpen" @update:open="editDialogOpen = false">
        <DialogContent class="sm:max-w-[625px]">
            <DialogHeader>
                <DialogTitle>Modifier l'intervention</DialogTitle>
                <DialogDescription>
                    Modifiez le nom et la description de l'intervention.
                </DialogDescription>
            </DialogHeader>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="name">Nom de l'intervention</Label>
                    <Input id="name" v-model="editForm.name" placeholder="Nom de l'intervention" />
                </div>
                <div class="grid gap-2">
                    <Label for="description">Description</Label>
                    <Textarea id="description" v-model="editForm.description"
                        placeholder="Description de l'intervention" />
                </div>
            </div>
            <DialogFooter>
                <Button variant="outline" @click="editDialogOpen = false">Annuler</Button>
                <Button @click="saveEdit" :disabled="loading">Enregistrer</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>

    <Dialog :open="siteDialogOpen" @update:open="siteDialogOpen = false">
        <DialogContent class="sm:max-w-[625px]">
            <DialogHeader>
                <DialogTitle>Modifier le site d'intervention</DialogTitle>
                <DialogDescription>
                    Sélectionnez un nouveau site pour cette intervention.
                </DialogDescription>
            </DialogHeader>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="site">Site d'intervention</Label>
                    <SiteSelect v-model="siteForm.site" class="w-full" placeholder="Sélectionner un site"
                        :company-id="job?.customer_company?.id" :contact-id="job?.customer_contact?.id" />
                </div>

                <div v-if="selectedSite" class="border rounded-lg p-4 bg-neutral-50">
                    <h4 class="text-sm font-medium text-neutral-900 mb-2">Aperçu du site</h4>
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
                <Button variant="outline" @click="siteDialogOpen = false">Annuler</Button>
                <Button @click="saveSite" :disabled="loading">Enregistrer</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import CategorySelect from '@/common/components/form/category-select/CategorySelect.vue'
import CompanySelect from '@/common/components/form/company-select/CompanySelect.vue'
import ContactSelect from '@/common/components/form/contact-select/ContactSelect.vue'
import PrioritySelect from '@/common/components/form/priority-select/PrioritySelect.vue'
import SiteSelect from '@/common/components/form/site-select/SiteSelect.vue'
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import Card from '@/common/components/ui/card/Card.vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import Input from '@/common/components/ui/input/Input.vue'
import Label from '@/common/components/ui/label/Label.vue'
import Separator from '@/common/components/ui/separator/Separator.vue'
import Tabs from '@/common/components/ui/tabs/Tabs.vue'
import TabsContent from '@/common/components/ui/tabs/TabsContent.vue'
import TabsList from '@/common/components/ui/tabs/TabsList.vue'
import TabsTrigger from '@/common/components/ui/tabs/TabsTrigger.vue'
import { Textarea } from '@/common/components/ui/textarea'
import { useFetcher } from '@/common/composables/fetcher'
import { useJob } from '@/common/composables/useJob'
import {
    AlertTriangle,
    ArrowLeft,
    Calendar,
    CalendarArrowUp,
    ChevronDown,
    Circle,
    Clock,
    Edit,
    File,
    Folder,
    Map,
    MapPin,
    MapPinned,
    Play,
    Plus,
    ScanSearch,
    ScrollText,
    ShieldAlert,
    User,
    UserPlus,
    UserRoundX
} from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const props = defineProps({
    inDialog: {
        type: Boolean,
        default: false
    }
})

const route = useRoute()
const router = useRouter()
const fetcher = useFetcher()
const { getPriorityConfig } = useJob()

const job = ref(null)
const loading = ref(false)

const editDialogOpen = ref(false)
const editForm = ref({
    name: '',
    description: ''
})

const siteDialogOpen = ref(false)
const siteForm = ref({
    site: null
})

const selectedSite = ref(null)

const fetchJob = async () => {
    loading.value = true
    try {
        const jobId = route.params.id
        const response = await fetcher.get(`/jobs/${jobId}`)
        job.value = response.data
        console.log('Job loaded:', job.value)
    } catch (error) {
        console.error('Erreur lors du chargement du job:', error)
        toast.error('Erreur lors du chargement du job')
    } finally {
        loading.value = false
    }
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const getClientName = () => {
    if (job.value?.customer_company) {
        return job.value.customer_company.name
    }
    if (job.value?.customer_contact) {
        return job.value.customer_contact.full_name
    }
    return 'Client non défini'
}

const getClientAddress = () => {
    if (job.value?.site) {
        const parts = [
            job.value.site.name,
            job.value.site.street,
            job.value.site.zip,
            job.value.site.city
        ].filter(Boolean)
        return parts.join(', ')
    }
    return 'Adresse non définie'
}

const getDuration = () => {
    if (job.value?.scheduled_start && job.value?.scheduled_end) {
        const start = new Date(job.value.scheduled_start)
        const end = new Date(job.value.scheduled_end)
        const diffMs = end - start
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
        return `${diffHours}h ${diffMinutes}min`
    }
    return 'Durée non définie'
}

const openEditDialog = () => {
    editForm.value = {
        name: job.value?.name || '',
        description: job.value?.description || ''
    }
    editDialogOpen.value = true
}

const saveEdit = async () => {
    loading.value = true
    try {
        const jobId = route.params.id
        await fetcher.put(`/jobs/${jobId}`, editForm.value)
        toast.success('Intervention modifiée avec succès')
        fetchJob() // Refresh job data
        editDialogOpen.value = false
    } catch (error) {
        console.error('Erreur lors de la sauvegarde de l\'intervention:', error)
        toast.error('Erreur lors de la sauvegarde de l\'intervention')
    } finally {
        loading.value = false
    }
}

const openSiteDialog = () => {
    siteForm.value.site = job.value?.site || null
    selectedSite.value = job.value?.site || null
    siteDialogOpen.value = true
}

const saveSite = async () => {
    loading.value = true
    try {
        const jobId = route.params.id
        const siteId = siteForm.value.site?.id || siteForm.value.site
        await fetcher.put(`/jobs/${jobId}`, { site: siteId })
        toast.success('Site d\'intervention modifié avec succès')
        fetchJob() // Refresh job data
        siteDialogOpen.value = false
    } catch (error) {
        console.error('Erreur lors de la sauvegarde du site:', error)
        toast.error('Erreur lors de la sauvegarde du site')
    } finally {
        loading.value = false
    }
}

const viewSite = (site) => {
    if (site?.id) {
        router.push({ name: 'site', params: { id: site.id } })
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

onMounted(() => {
    fetchJob()
})
</script>