<template>
    <ListView :config="config" :columns="columns" :items="companies" :filter-fields="filterFields"
        :search-fields="searchFields" :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
        :items-per-page="itemsPerPage" :loading="loading" :context-menu-actions="contextMenuActions"
        @create="handleCreate" @row-click="handleRowClick" @search="handleSearch" @page-change="handlePageChange"
        @items-per-page-change="handleItemsPerPageChange" @filter-change="handleFilterChange"
        @selection-change="handleSelectionChange" @context-menu-action="handleContextMenuAction">

        <template #empty-state>
            <div class="text-center py-8">
                <div class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                    <Building2 class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                </div>
                <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre première entreprise cliente</h3>
                <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                    Les entreprises sont le cœur de votre activité. Commencez par ajouter vos clients pour organiser vos
                    interventions,
                    suivre vos contacts et gérer vos projets efficacement.
                </p>
                <Button @click="handleCreate" class="inline-flex items-center">
                    <Plus class="w-4 h-4 mr-2" />
                    Ajouter une entreprise
                </Button>
            </div>
        </template>
    </ListView>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import {
    companiesColumns,
    companiesConfig,
    companiesFilters
} from '@/main/components/companies/columns.js'
import ListView from '@/main/components/ListView.vue'
import { debounce } from 'lodash'
import { Building2, Eye, Plus, Trash } from 'lucide-vue-next'
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()

const config = reactive(companiesConfig)
const columns = companiesColumns
const filterFields = companiesFilters
const searchFields = "name,city,reference"

const companies = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')

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

const fetchCompanies = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/companies', {
            params: {
                page: currentPage.value,
                per_page: itemsPerPage.value
            }
        })
        companies.value = response.data.items || []
        totalItems.value = response.data.total || 0
        totalPages.value = response.data.total_pages || 1
        currentPage.value = response.data.page || 1
    } catch (err) {
        console.error('Erreur lors du chargement des entreprises:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchCompanies = async (query) => {
    if (!query || query.trim().length < 2) {
        currentPage.value = 1
        fetchCompanies()
        return
    }

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/companies/quick_search', {
            params: {
                q: query.trim(),
                page: currentPage.value,
                per_page: itemsPerPage.value
            }
        })
        companies.value = response.data.items || []
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

const debouncedSearchCompanies = debounce(searchCompanies, 300)

const handleCreate = () => {
    bus.trigger('open-company-dialog')
}

const handleRowClick = (company) => {
    router.push(`/company/${company.id}`)
}

const handleSearch = (query) => {
    searchQuery.value = query
    debouncedSearchCompanies(query)
}

const handlePageChange = (page) => {
    currentPage.value = page
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchCompanies(searchQuery.value)
    } else {
        fetchCompanies()
    }
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = itemsCount
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchCompanies(searchQuery.value)
    } else {
        fetchCompanies()
    }
}

const handleFilterChange = (filters) => {
    console.log('Filters changed:', filters)
}

const handleSelectionChange = (selectedIds) => {
    console.log('Selection changed:', selectedIds)
}

const handleContextMenuAction = (action, company) => {
    switch (action) {
        case 'view':
            router.push(`/company/${company.id}`)
            break
        case 'delete':
            handleDelete(company)
            break
    }
}

const handleDelete = (company) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer l\'entreprise',
        message: 'Êtes-vous sûr de vouloir supprimer cette entreprise ?',
        itemName: company.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-company-list:confirmed'
    })

    selectedCompanyForDelete.value = company
}

const selectedCompanyForDelete = ref(null)

const deleteCompany = async () => {
    if (!selectedCompanyForDelete.value) return

    try {
        await fetcher.delete(`/companies/${selectedCompanyForDelete.value.id}`)
        toast.success('Entreprise supprimée avec succès')
        bus.trigger('confirm-delete-dialog:close')
        refreshList()
        selectedCompanyForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const refreshList = () => {
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchCompanies(searchQuery.value)
    } else {
        fetchCompanies()
    }
}

useBus(bus, 'company-saved', () => {
    refreshList()
})

useBus(bus, 'company-created-stay', () => {
    refreshList()
})

useBus(bus, 'confirm-delete-company-list:confirmed', () => {
    deleteCompany()
})

onMounted(() => {
    fetchCompanies()
})


</script>