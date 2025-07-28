<template>
    <ListView :config="config" :columns="columns" :items="formattedCompanies" :filter-fields="filterFields"
        :search-fields="searchFields" :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
        :items-per-page="itemsPerPage" :loading="loading" @create="handleCreate" @row-click="handleRowClick"
        @search="handleSearch" @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange"
        @filter-change="handleFilterChange" @selection-change="handleSelectionChange" />
</template>

<script setup>
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
const itemsPerPage = ref(20)
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
                skip: (currentPage.value - 1) * itemsPerPage.value,
                limit: itemsPerPage.value
            }
        })
        companies.value = response.data || []
        totalItems.value = response.data.length
        totalPages.value = Math.ceil(totalItems.value / itemsPerPage.value)
    } catch (err) {
        console.error('Erreur lors du chargement des entreprises:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchCompanies = async (query) => {
    if (!query || query.trim().length < 2) {
        fetchCompanies()
        return
    }

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/companies/quick_search', {
            params: {
                q: query.trim(),
                limit: 50
            }
        })
        companies.value = response.data || []
        totalItems.value = response.data.length
        totalPages.value = 1
        currentPage.value = 1
    } catch (err) {
        console.error('Erreur lors de la recherche:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const debouncedSearchCompanies = debounce(searchCompanies, 300)

onMounted(() => {
    fetchCompanies()
})

const handleCreate = () => {
    router.push('/companies/create')
}

const handleRowClick = (company) => {
    router.push(`/company/${company.id}`)
}

const handleSearch = (query) => {
    searchQuery.value = query
    debouncedSearchCompanies(query)
}

const handlePageChange = (page) => {
    if (searchQuery.value) {
        return
    }
    currentPage.value = page
    fetchCompanies()
}

const handleItemsPerPageChange = (itemsCount) => {
    if (searchQuery.value) {
        return
    }
    itemsPerPage.value = itemsCount
    currentPage.value = 1
    fetchCompanies()
}

const handleFilterChange = (filters) => {
    console.log('Filters changed:', filters)
}

const handleSelectionChange = (selectedIds) => {
    console.log('Selection changed:', selectedIds)
}
</script>