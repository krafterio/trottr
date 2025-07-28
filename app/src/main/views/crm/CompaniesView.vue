<template>
    <ListView :config="config" :columns="columns" :items="formattedCompanies" :filter-fields="filterFields"
        :search-fields="searchFields" :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
        :items-per-page="itemsPerPage" :loading="loading" @create="handleCreate" @row-click="handleRowClick"
        @search="handleSearch" @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange"
        @filter-change="handleFilterChange" @selection-change="handleSelectionChange" />
</template>

<script setup>
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useCompany } from '@/common/composables/useCompany'
import ListView from '@/main/components/ListView.vue'
import {
    companiesColumns,
    companiesConfig,
    companiesFilters
} from '@/main/components/companies/columns.js'
import { debounce } from 'lodash'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fetcher = useFetcher()
const { getCompanyTypeLabel } = useCompany()

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

const formattedCompanies = computed(() => {
    return companies.value.map(company => ({
        ...company,
        company_type: getCompanyTypeLabel(company.company_type)
    }))
})

const fetchCompanies = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/companies/', {
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

onMounted(() => {
    fetchCompanies()
})


</script>