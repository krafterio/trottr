<template>
    <ListView :config="config" :columns="columns" :items="sites" :filter-fields="filterFields"
        :search-fields="searchFields" :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
        :items-per-page="itemsPerPage" :loading="loading" :context-menu-actions="contextMenuActions"
        @create="handleCreate" @row-click="handleRowClick" @search="handleSearch" @page-change="handlePageChange"
        @items-per-page-change="handleItemsPerPageChange" @filter-change="handleFilterChange"
        @selection-change="handleSelectionChange" @context-menu-action="handleContextMenuAction">

        <template #empty-state>
            <div class="text-center py-8">
                <div class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                    <MapPin class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                </div>
                <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre premier site d'intervention</h3>
                <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                    Les sites d'intervention sont les lieux où vous réalisez vos prestations. Commencez par ajouter vos
                    premiers sites pour organiser vos interventions et suivre vos projets efficacement.
                </p>
                <Button @click="handleCreate" class="inline-flex items-center">
                    <Plus class="w-4 h-4 mr-2" />
                    Ajouter un site
                </Button>
            </div>
        </template>
    </ListView>

    <SiteDialog :is-open="isDialogOpen" :site="selectedSite" @close="handleDialogClose" @saved="handleSiteSaved" />
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import ListView from '@/main/components/ListView.vue'
import {
    sitesColumns,
    sitesConfig,
    sitesFilters
} from '@/main/components/sites/columns.js'
import SiteDialog from '@/main/components/sites/SiteDialog.vue'
import { debounce } from 'lodash'
import { Eye, MapPin, Plus, Trash } from 'lucide-vue-next'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()

const config = reactive(sitesConfig)
const columns = sitesColumns
const filterFields = sitesFilters
const searchFields = "name,city,street"

const sites = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')

const isDialogOpen = ref(false)
const selectedSite = ref(null)

const contextMenuActions = [
    {
        key: 'view',
        label: 'Voir',
        icon: Eye
    },
    {
        key: 'delete',
        label: 'Supprimer',
        icon: Trash,
    }
]

const fetchSites = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/sites', {
            params: {
                page: currentPage.value,
                per_page: itemsPerPage.value
            }
        })
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
        const response = await fetcher.get('/sites/', {
            params: {
                page: currentPage.value,
                per_page: itemsPerPage.value
            }
        })

        const filteredSites = response.data.items.filter(site =>
            site.name.toLowerCase().includes(query.toLowerCase()) ||
            site.city.toLowerCase().includes(query.toLowerCase()) ||
            site.street.toLowerCase().includes(query.toLowerCase())
        )

        sites.value = filteredSites
        totalItems.value = filteredSites.length
        totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value)
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

const handleRowClick = (site) => {
    console.log('Site clicked:', site)
}

const handleSearch = (query) => {
    searchQuery.value = query
    debouncedSearchSites(query)
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
    itemsPerPage.value = itemsCount
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchSites(searchQuery.value)
    } else {
        fetchSites()
    }
}

const handleFilterChange = (filters) => {
    console.log('Filters changed:', filters)
}

const handleSelectionChange = (selectedIds) => {
    console.log('Selection changed:', selectedIds)
}

const handleContextMenuAction = (action, site) => {
    switch (action) {
        case 'view':
            console.log('View site:', site)
            break
        case 'delete':
            handleDelete(site)
            break
    }
}

const handleDelete = (site) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le site',
        message: 'Êtes-vous sûr de vouloir supprimer ce site ?',
        itemName: site.name
    })

    selectedSiteForDelete.value = site
}

const selectedSiteForDelete = ref(null)

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

useBus(bus, 'confirm-delete-dialog:confirmed', () => {
    deleteSite()
})

onMounted(() => {
    fetchSites()
})
</script>