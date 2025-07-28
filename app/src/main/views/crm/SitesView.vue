<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-0">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Sites d'intervention</h1>
                    <p class="text-neutral-600">Gestion des sites d'intervention</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouveau site
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Type de bâtiment</h4>
                        <div class="space-y-2">
                            <label v-for="option in buildingTypeOptions" :key="option.value" class="flex items-center">
                                <Checkbox :checked="selectedFilters.building_type?.includes(option.value) || false"
                                    @update:checked="toggleFilter('building_type', option.value)" />
                                <span class="ml-2 text-sm text-neutral-600">{{ option.label }}</span>
                            </label>
                        </div>
                    </div>

                    <Button variant="outline" size="sm" class="w-full" @click="resetFilters">
                        <RotateCcw class="h-4 w-4 mr-2" />
                        Réinitialiser
                    </Button>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto pb-16">
                <div class="px-6 py-4 border-b">
                    <div class="flex items-center justify-between">
                        <div class="relative">
                            <Search
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                            <Input type="text" placeholder="Rechercher un site..." class="h-9 pl-10 pr-4 py-2 w-64"
                                v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} sites</span>
                    </div>
                </div>

                <div v-if="loading" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center">
                        <div
                            class="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto mb-4">
                        </div>
                        <p class="text-neutral-600">Chargement...</p>
                    </div>
                </div>

                <div v-else-if="sites.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <MapPin class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre premier site d'intervention
                        </h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Les sites d'intervention sont les lieux où vous réalisez vos prestations. Commencez par
                            ajouter vos
                            premiers sites pour organiser vos interventions et suivre vos projets efficacement.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Ajouter un site
                        </Button>
                    </div>
                </div>

                <div v-else>
                    <Table>
                        <TableHeader>
                            <TableRow class="bg-neutral-50 border-b uppercase tracking-wider text-xs text-neutral-500">
                                <TableHead class="ps-3 w-8">
                                    <Checkbox v-model="selectAll" @update:model-value="toggleSelectAll" />
                                </TableHead>
                                <TableHead>Nom du site</TableHead>
                                <TableHead>Type de bâtiment</TableHead>
                                <TableHead>Adresse</TableHead>
                                <TableHead>Ville</TableHead>
                                <TableHead>Code postal</TableHead>
                                <TableHead>Pays</TableHead>
                                <TableHead>Entreprise</TableHead>
                                <TableHead class="w-10"></TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="site in sites" :key="site.id" class="hover:bg-neutral-50">
                                <TableCell @click.stop class="ps-3">
                                    <Checkbox :checked="selectedSites.includes(site.id)"
                                        @update:checked="toggleSiteSelection(site.id)" />
                                </TableCell>
                                <TableCell class="font-medium text-neutral-900">
                                    <router-link :to="`/site/${site.id}`"
                                        class="text-neutral-900 hover:text-neutral-700 underline">
                                        {{ site.name }}
                                    </router-link>
                                </TableCell>
                                <TableCell>
                                    <Badge variant="outline" v-if="site.building_type">
                                        {{ getSiteBuildingTypeLabel(site.building_type) }}
                                    </Badge>
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ site.street }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ site.city }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ site.zip }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ site.country?.name || '-' }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    <router-link v-if="site.company" :to="`/company/${site.company.id}`"
                                        class="text-neutral-900 hover:text-neutral-700 underline">
                                        {{ site.company.name }}
                                    </router-link>
                                    <span v-else class="text-neutral-500">-</span>
                                </TableCell>
                                <TableCell @click.stop>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger as-child>
                                            <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                <MoreVertical class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem @click="handleView(site)">
                                                <Eye class="mr-2 h-4 w-4" />
                                                Voir
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="handleDelete(site)" class="text-red-600">
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

        <TablePagination :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
            :items-per-page="itemsPerPage"
            :position-classes="showFilters ? 'bottom-0 left-80 right-0' : 'bottom-0 left-32 right-0'"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />
    </div>

    <SiteDialog :is-open="isDialogOpen" :site="selectedSite" @close="handleDialogClose" @saved="handleSiteSaved" />
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Input } from '@/common/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useSite } from '@/common/composables/useSite'
import SiteDialog from '@/main/components/sites/SiteDialog.vue'
import TablePagination from '@/main/components/TablePagination.vue'
import { debounce } from 'lodash'
import { Download, Eye, MapPin, MoreVertical, PanelLeftClose, PanelLeftOpen, Plus, RotateCcw, Search, Trash } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()
const { getSiteBuildingTypeLabel, getSiteBuildingTypeOptions } = useSite()

const sites = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedSites = ref([])
const selectedSiteForDelete = ref(null)
const showFilters = ref(true)
const selectedFilters = reactive({
    building_type: []
})

const isDialogOpen = ref(false)
const selectedSite = ref(null)

const buildingTypeOptions = getSiteBuildingTypeOptions()

const selectAll = computed({
    get() {
        return sites.value.length > 0 && selectedSites.value.length === sites.value.length
    },
    set(value) {
        if (value) {
            selectedSites.value = sites.value.map(s => s.id)
        } else {
            selectedSites.value = []
        }
    }
})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const toggleFilter = (filterKey, value) => {
    if (!selectedFilters[filterKey]) {
        selectedFilters[filterKey] = []
    }

    const index = selectedFilters[filterKey].indexOf(value)
    if (index > -1) {
        selectedFilters[filterKey].splice(index, 1)
    } else {
        selectedFilters[filterKey].push(value)
    }

    applyFilters()
}

const resetFilters = () => {
    selectedFilters.building_type = []
    applyFilters()
}

const applyFilters = () => {
    currentPage.value = 1
    fetchSites()
}

const fetchSites = async () => {
    loading.value = true
    error.value = null

    try {
        const params = {
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        if (selectedFilters.building_type.length > 0) {
            params.building_type = selectedFilters.building_type
        }

        const response = await fetcher.get('/sites', { params })
        sites.value = response.data.items || []
        totalItems.value = response.data.total || 0
        totalPages.value = response.data.total_pages || 1
        currentPage.value = response.data.page || 1
    } catch (err) {
        console.error('Erreur lors du chargement des sites:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchSites = async (query) => {
    if (!query || query.trim().length < 2) {
        currentPage.value = 1
        fetchSites()
        return
    }

    loading.value = true
    error.value = null

    try {
        const params = {
            q: query.trim(),
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        if (selectedFilters.building_type.length > 0) {
            params.building_type = selectedFilters.building_type
        }

        const response = await fetcher.get('/sites/quick_search', { params })
        sites.value = response.data.items || []
        totalItems.value = response.data.total || 0
        totalPages.value = response.data.total_pages || 1
        currentPage.value = response.data.page || 1
    } catch (err) {
        console.error('Erreur lors de la recherche:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const debouncedSearchSites = debounce(searchSites, 300)

const handleCreate = () => {
    selectedSite.value = null
    isDialogOpen.value = true
}

const handleView = (site) => {
    router.push(`/site/${site.id}`)
}

const handleSearch = () => {
    debouncedSearchSites(searchQuery.value)
}

const handlePageChange = (page) => {
    currentPage.value = page
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchSites(searchQuery.value)
    } else {
        fetchSites()
    }
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchSites(searchQuery.value)
    } else {
        fetchSites()
    }
}

const toggleSelectAll = () => {
    selectAll.value = !selectAll.value
}

const toggleSiteSelection = (siteId) => {
    const index = selectedSites.value.indexOf(siteId)
    if (index > -1) {
        selectedSites.value.splice(index, 1)
    } else {
        selectedSites.value.push(siteId)
    }
}

const handleDelete = (site) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le site',
        message: 'Êtes-vous sûr de vouloir supprimer ce site ?',
        itemName: site.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-site:confirmed'
    })

    selectedSiteForDelete.value = site
}

const deleteSite = async () => {
    if (!selectedSiteForDelete.value) return

    try {
        await fetcher.delete(`/sites/${selectedSiteForDelete.value.id}`)
        toast.success('Site supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        refreshList()
        selectedSiteForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const refreshList = () => {
    selectedSites.value = []
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchSites(searchQuery.value)
    } else {
        fetchSites()
    }
}

const handleDialogClose = () => {
    isDialogOpen.value = false
    selectedSite.value = null
}

const handleSiteSaved = () => {
    refreshList()
}

useBus(bus, 'sites:refresh', () => {
    refreshList()
})

useBus(bus, 'confirm-delete-site:confirmed', () => {
    deleteSite()
})

onMounted(() => {
    fetchSites()
})
</script>