<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Interventions</h1>
                    <p class="text-neutral-600">Gestion des interventions terrain</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouvelle intervention
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div :class="[
                'bg-neutral-50 border-r overflow-y-auto',
                showFilters ? 'w-64 p-4' : 'w-16 p-2 pt-4 cursor-pointer hover:bg-neutral-100'
            ]" @click="!showFilters && toggleFilters()">
                <div v-if="showFilters" class="flex items-center justify-between mb-4">
                    <h3 class="font-semibold text-neutral-900">Filtres</h3>
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0 cursor-pointer" @click.stop="toggleFilters">
                        <PanelLeftClose class="h-4 w-4" />
                    </Button>
                </div>

                <div v-else class="flex flex-col items-center mb-4">
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0 mb-2 cursor-pointer"
                        @click.stop="toggleFilters">
                        <PanelLeftOpen class="h-4 w-4" />
                    </Button>
                    <h3 class="font-semibold text-neutral-900 transform -rotate-90 origin-center mt-4">
                        Filtres
                    </h3>
                </div>

                <div v-show="showFilters" class="space-y-6">
                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Recherche</h4>
                        <Input v-model="searchQuery" placeholder="Rechercher..." class="w-full" />
                    </div>
                </div>
            </div>

            <div class="flex-1 flex flex-col overflow-hidden">
                <div class="flex-1 overflow-auto">
                    <div class="px-6 py-4 border-b">
                        <div class="flex items-center justify-between">
                            <div class="relative">
                                <Search
                                    class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                                <Input v-model="searchQuery" placeholder="Recherche rapide..."
                                    class="h-9 pl-10 pr-4 py-2 w-64" />
                            </div>

                            <div class="flex items-center space-x-3">
                                <span class="text-sm text-muted-foreground">{{ jobs.length }} interventions</span>
                                <Button variant="outline" size="sm" class="w-8">
                                    <MoreVertical class="h-4 w-4" />
                                </Button>
                                <Button variant="outline">
                                    <Columns class="h-4 w-4" />
                                    Colonnes
                                    <ChevronDown class="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div>
                        <Table>
                            <TableHeader
                                class="bg-neutral-50 text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-5">
                                <TableRow>
                                    <TableHead class="py-3 w-12">
                                        <Checkbox :checked="isAllSelected" @update:checked="toggleSelectAll" />
                                    </TableHead>
                                    <TableHead class="py-3">Réf.</TableHead>
                                    <TableHead class="py-3">Intervention</TableHead>
                                    <TableHead class="py-3">Client</TableHead>
                                    <TableHead class="py-3">Opérateur</TableHead>
                                    <TableHead class="py-3">Date/Heure</TableHead>
                                    <TableHead class="py-3">Statut</TableHead>
                                    <TableHead class="py-3">Priorité</TableHead>
                                    <TableHead class="w-12 py-3"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-for="job in jobs" :key="job.id" class="hover:bg-neutral-50">
                                    <TableCell @click.stop>
                                        <Checkbox :checked="selectedJobs.includes(job.id)"
                                            @update:checked="toggleJobSelection(job.id)" />
                                    </TableCell>
                                    <TableCell>
                                        <div class="flex flex-col gap-1 py-2">
                                            <div class="text-sm font-medium font-mono underline text-neutral-900 cursor-pointer hover:text-primary"
                                                @click.stop="handleRowClick(job)">{{ job.reference
                                                }}</div>
                                            <div class="text-xs text-neutral-500">{{ formatDate(job.created_at) }}</div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div class="flex flex-col gap-1 py-2">
                                            <div class="text-sm font-medium text-neutral-900 underline cursor-pointer hover:text-primary"
                                                @click="handleRowClick(job)">{{ job.name }}</div>
                                            <div v-if="job.category" class="text-xs text-neutral-500">
                                                {{ job.category.name }}
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div class="flex flex-col gap-1">
                                            <div v-if="job.customer_company"
                                                class="text-sm text-neutral-900 cursor-pointer hover:text-primary underline"
                                                @click.stop="handleCompanyClick(job.customer_company)">
                                                {{ job.customer_company.name }}
                                            </div>
                                            <div v-else-if="job.customer_contact" class="text-sm text-neutral-900">
                                                {{ job.customer_contact.full_name }}
                                            </div>
                                            <div v-else class="text-sm text-neutral-500">-</div>
                                            <div v-if="job.site" class="text-xs text-neutral-500 truncate max-w-xs">
                                                {{ getSiteAddress(job.site) }}
                                            </div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div v-if="job.operator" class="flex items-center py-2">
                                            <div class="flex-shrink-0 h-8 w-8">
                                                <div
                                                    class="h-8 w-8 rounded-full bg-neutral-100 flex items-center justify-center">
                                                    <span class="text-sm font-medium text-neutral-600">
                                                        {{ getInitials(job.operator.name) }}
                                                    </span>
                                                </div>
                                            </div>
                                            <div class="ml-3">
                                                <div class="text-sm font-medium text-neutral-900">
                                                    {{ job.operator.name }}
                                                </div>
                                            </div>
                                        </div>
                                        <div v-else class="text-sm text-neutral-500">Non assigné</div>
                                    </TableCell>
                                    <TableCell>
                                        <div v-if="job.scheduled_start" class="py-2">
                                            {{ formatDate(job.scheduled_start) }}
                                        </div>
                                        <div v-else class="text-neutral-500">Non planifié</div>
                                    </TableCell>
                                    <TableCell>
                                        <span v-if="job.status"
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800 py-2">
                                            {{ job.status.name }}
                                        </span>
                                        <span v-else class="text-neutral-500">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <div class="flex items-center gap-2 py-2">
                                            <component :is="getPriorityConfig(job.priority).icon" class="w-4 h-4"
                                                :class="getPriorityConfig(job.priority).color" />
                                            <span class="text-sm">{{ getPriorityConfig(job.priority).label }}</span>
                                        </div>
                                    </TableCell>
                                    <TableCell @click.stop>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger as-child>
                                                <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                    <MoreVertical class="h-4 w-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem @click.stop="handleEdit(job)">
                                                    <Eye class="mr-2 h-4 w-4" />
                                                    Voir
                                                </DropdownMenuItem>
                                                <DropdownMenuItem @click.stop="handleDelete(job)" class="text-red-600">
                                                    <Trash class="mr-2 h-4 w-4" />
                                                    Supprimer
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>
                </div>
            </div>
        </div>

        <TablePagination :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
            :items-per-page="itemsPerPage"
            :position-classes="showFilters ? 'bottom-0 left-80 right-0' : 'bottom-0 left-32 right-0'"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Input } from '@/common/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useJob } from '@/common/composables/useJob'
import TablePagination from '@/main/components/TablePagination.vue'
import { usePreferencesStore } from '@/main/stores/preferences'
import { ChevronDown, Columns, Download, Eye, MoreVertical, PanelLeftClose, PanelLeftOpen, Plus, Search, Trash } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const fetcher = useFetcher()
const preferencesStore = usePreferencesStore()
const { getPriorityConfig } = useJob()
const router = useRouter()

const jobs = ref([])
const loading = ref(false)
const searchQuery = ref('')
const selectedJobs = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)

const showFilters = computed({
    get() {
        return preferencesStore.getPreference('display_filters', true)
    },
    set(value) {
        preferencesStore.updatePreference('display_filters', value)
        toast.success('Préférences mises à jour')
    }
})

const toggleFilters = async () => {
    showFilters.value = !showFilters.value
}

const isAllSelected = computed(() => {
    return jobs.value.length > 0 && selectedJobs.value.length === jobs.value.length
})

const fetchJobs = async () => {
    loading.value = true
    try {
        const skip = (currentPage.value - 1) * itemsPerPage.value
        const response = await fetcher.get(`/jobs?skip=${skip}&limit=${itemsPerPage.value}`)
        jobs.value = response.data
        totalItems.value = response.total || jobs.value.length
        totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value)
    } catch (error) {
        console.error('Erreur lors du chargement des interventions:', error)
        toast.error('Erreur lors du chargement des interventions')
    } finally {
        loading.value = false
    }
}

const handleCreate = () => {
    bus.trigger('open-job-dialog', { mode: 'create' })
}

const handleEdit = (job) => {
    bus.trigger('open-job-dialog', { mode: 'edit', job })
}

const handleDelete = (job) => {
    bus.trigger('confirm-delete-job', { job })
}

const handleRowClick = (job) => {
    console.log('Clicking on job:', job.id)
    router.push({ name: 'job', params: { id: job.id } })
}

const handleCompanyClick = (company) => {
    router.push({ name: 'company', params: { id: company.id } })
}

const handlePageChange = (page) => {
    currentPage.value = page
    fetchJobs()
}

const handleItemsPerPageChange = (itemsPerPageValue) => {
    itemsPerPage.value = itemsPerPageValue
    currentPage.value = 1
    fetchJobs()
}

const toggleJobSelection = (jobId) => {
    const index = selectedJobs.value.indexOf(jobId)
    if (index > -1) {
        selectedJobs.value.splice(index, 1)
    } else {
        selectedJobs.value.push(jobId)
    }
}

const toggleSelectAll = (checked) => {
    if (checked) {
        selectedJobs.value = jobs.value.map(job => job.id)
    } else {
        selectedJobs.value = []
    }
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    })
}

const getInitials = (name) => {
    if (!name) return ''
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getSiteAddress = (site) => {
    if (!site) return '-'
    const parts = [
        site.name,
        site.street,
        site.zip,
        site.city
    ].filter(Boolean)
    return parts.join(' - ')
}

onMounted(() => {
    fetchJobs()

    useBus(bus, 'job-saved', () => {
        fetchJobs()
    })

    useBus(bus, 'job-created-stay', () => {
        fetchJobs()
    })
})
</script>