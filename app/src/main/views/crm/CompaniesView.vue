<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-0">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Entreprises</h1>
                    <p class="text-neutral-600">Gestion des entreprises clientes</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouvelle entreprise
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Type</h4>
                        <div class="space-y-2">
                            <label v-for="option in companyTypeOptions" :key="option.value" class="flex items-center">
                                <Checkbox :checked="selectedFilters.company_type?.includes(option.value) || false"
                                    @update:checked="toggleFilter('company_type', option.value)" />
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
                            <Input type="text" placeholder="Rechercher une entreprise..."
                                class="h-9 pl-10 pr-4 py-2 w-64" v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} entreprises</span>
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

                <div v-else-if="companies.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <Building2 class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre première entreprise cliente
                        </h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Les entreprises sont le cœur de votre activité. Commencez par ajouter vos clients pour
                            organiser vos interventions,
                            suivre vos contacts et gérer vos projets efficacement.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Ajouter une entreprise
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
                                <TableHead>Entreprise</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Référence</TableHead>
                                <TableHead>Adresse</TableHead>
                                <TableHead>Ville</TableHead>
                                <TableHead>Téléphone</TableHead>
                                <TableHead>Email</TableHead>
                                <TableHead>SIRET</TableHead>
                                <TableHead class="w-10"></TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="company in companies" :key="company.id" class="hover:bg-neutral-50">
                                <TableCell @click.stop class="ps-3">
                                    <Checkbox :checked="selectedCompanies.includes(company.id)"
                                        @update:checked="toggleCompanySelection(company.id)" />
                                </TableCell>
                                <TableCell class="font-medium text-neutral-900">
                                    <router-link :to="`/company/${company.id}`"
                                        class="text-neutral-900 hover:text-neutral-700 underline">
                                        {{ company.name }}
                                    </router-link>
                                </TableCell>
                                <TableCell>
                                    <Badge variant="outline" v-if="company.company_type">
                                        {{ getCompanyTypeLabel(company.company_type) }}
                                    </Badge>
                                </TableCell>
                                <TableCell class="text-neutral-900 font-mono">
                                    {{ company.reference }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ company.invoice_street }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ company.invoice_city }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ company.phone }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ company.email }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ company.siret }}
                                </TableCell>
                                <TableCell @click.stop>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger as-child>
                                            <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                <MoreVertical class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem @click="handleView(company)">
                                                <Eye class="mr-2 h-4 w-4" />
                                                Voir
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="handleDelete(company)" class="text-red-600">
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
import { useCompany } from '@/common/composables/useCompany'
import TablePagination from '@/main/components/TablePagination.vue'
import { usePreferencesStore } from '@/main/stores/preferences'

import { debounce } from 'lodash'
import { Building2, Download, Eye, MoreVertical, PanelLeftClose, PanelLeftOpen, Plus, RotateCcw, Search, Trash } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()
const { getCompanyTypeLabel, getCompanyTypeOptions } = useCompany()
const preferencesStore = usePreferencesStore()

const companies = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedCompanies = ref([])
const selectedCompanyForDelete = ref(null)
const selectedFilters = reactive({
    company_type: []
})

const showFilters = computed({
    get() {
        return preferencesStore.getPreference('display_filters', true)
    },
    set(value) {
        preferencesStore.updatePreference('display_filters', value)
        toast.success('Préférences mises à jour')
    }
})

const companyTypeOptions = getCompanyTypeOptions()

const selectAll = computed({
    get() {
        return companies.value.length > 0 && selectedCompanies.value.length === companies.value.length
    },
    set(value) {
        if (value) {
            selectedCompanies.value = companies.value.map(c => c.id)
        } else {
            selectedCompanies.value = []
        }
    }
})

const toggleFilters = async () => {
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
    selectedFilters.company_type = []
    applyFilters()
}

const applyFilters = () => {
    currentPage.value = 1
    fetchCompanies()
}

const fetchCompanies = async () => {
    loading.value = true
    error.value = null

    try {
        const params = {
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        if (selectedFilters.company_type.length > 0) {
            params.company_type = selectedFilters.company_type
        }

        const response = await fetcher.get('/companies', { params })
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
        const params = {
            q: query.trim(),
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        if (selectedFilters.company_type.length > 0) {
            params.company_type = selectedFilters.company_type
        }

        const response = await fetcher.get('/companies/quick_search', { params })
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

const handleView = (company) => {
    router.push(`/company/${company.id}`)
}

const handleSearch = () => {
    debouncedSearchCompanies(searchQuery.value)
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
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchCompanies(searchQuery.value)
    } else {
        fetchCompanies()
    }
}

const toggleSelectAll = () => {
    selectAll.value = !selectAll.value
}

const toggleCompanySelection = (companyId) => {
    const index = selectedCompanies.value.indexOf(companyId)
    if (index > -1) {
        selectedCompanies.value.splice(index, 1)
    } else {
        selectedCompanies.value.push(companyId)
    }
}

const handleDelete = (company) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer l\'entreprise',
        message: 'Êtes-vous sûr de vouloir supprimer cette entreprise ?',
        itemName: company.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-company:confirmed'
    })

    selectedCompanyForDelete.value = company
}

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
    selectedCompanies.value = []
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

useBus(bus, 'confirm-delete-company:confirmed', () => {
    deleteCompany()
})

onMounted(() => {
    fetchCompanies()
})
</script>