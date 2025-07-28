<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Techniciens</h1>
                    <p class="text-neutral-600">Gestion des techniciens</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Spécialité</h4>
                        <div class="space-y-2" v-if="availableSpecialities.length > 0">
                            <label v-for="speciality in availableSpecialities" :key="speciality.id"
                                class="flex items-center">
                                <Checkbox :checked="selectedFilters.speciality_ids?.includes(speciality.id) || false"
                                    @update:checked="toggleFilter('speciality_ids', speciality.id)" />
                                <div class="flex items-center ml-2">
                                    <span class="text-sm text-neutral-600">{{ speciality.name }}</span>
                                </div>
                            </label>
                        </div>
                        <div v-else class="text-sm text-neutral-400 italic">
                            Aucune spécialité
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
                            <Input type="text" placeholder="Rechercher un technicien..."
                                class="h-9 pl-10 pr-4 py-2 w-64" v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} techniciens</span>
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

                <div v-else-if="operators.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <Users class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Aucun technicien trouvé</h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Commencez par inviter des techniciens dans votre workspace ou modifiez vos filtres de
                            recherche.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Inviter un technicien
                        </Button>
                    </div>
                </div>

                <div v-else class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-neutral-50 border-b">
                            <tr>
                                <th
                                    class="px-3 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-5">
                                    <Checkbox />
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    Technicien
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    Spécialités
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    Zone intervention
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    Téléphone
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    Email
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    Actions
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-neutral-200">
                            <tr v-for="operator in operators" :key="operator.id"
                                class="hover:bg-neutral-50 cursor-pointer" @click.stop="editOperator(operator)">
                                <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                    <Checkbox />
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <div class="flex items-center space-x-3">
                                        <Avatar class="w-5 h-5 rounded-full">
                                            <AvatarImage v-if="operator.avatar"
                                                :src="`/storage/download/${operator.avatar}`" v-fetcher-src.lazy
                                                :alt="operator.name || operator.email" />
                                            <AvatarFallback
                                                class="bg-primary/10 text-primary text-xs font-medium rounded-md">
                                                {{ operator.initials || getInitials(operator.name, operator.email) }}
                                            </AvatarFallback>
                                        </Avatar>
                                        <div class="text-sm font-medium text-neutral-900">{{ operator.name ||
                                            operator.email }}</div>
                                    </div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <div class="flex flex-wrap gap-1"
                                        v-if="operator.job_specialities && operator.job_specialities.length > 0">
                                        <Badge v-for="speciality in operator.job_specialities" :key="speciality.id"
                                            variant="outline" class="flex items-center gap-1">
                                            <div class="w-2 h-2 rounded-full"
                                                :style="{ backgroundColor: speciality.color }"></div>
                                            {{ speciality.name }}
                                        </Badge>
                                    </div>
                                    <span v-else class="text-sm text-neutral-400">Aucune spécialité</span>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <div class="text-sm text-neutral-900">{{ operator.zone || '-' }}</div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <div class="text-sm text-neutral-900">{{ operator.phone || '-' }}</div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <div class="text-sm text-neutral-900">{{ operator.email }}</div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <Button variant="ghost" size="sm" @click.stop="editOperator(operator)">
                                        <Edit class="h-4 w-4" />
                                    </Button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <TablePagination :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
            :items-per-page="itemsPerPage"
            :position-classes="showFilters ? 'bottom-0 left-80 right-0' : 'bottom-0 left-32 right-0'"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />

        <!-- Dialog d'édition utilisateur -->
        <UserEditDialog :is-open="showEditDialog" :user="selectedUser" />
    </div>
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import Input from '@/common/components/ui/input/Input.vue'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import TablePagination from '@/main/components/TablePagination.vue'
import UserEditDialog from '@/main/components/dialogs/UserEditDialog.vue'
import { usePreferencesStore } from '@/main/stores/preferences'
import { debounce } from 'lodash'
import {
    Download,
    Edit,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    RotateCcw,
    Search,
    Users
} from 'lucide-vue-next'
import { computed, onMounted, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'

const fetcher = useFetcher()
const preferencesStore = usePreferencesStore()

const operators = ref([])
const availableSpecialities = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedFilters = reactive({
    speciality_ids: []
})
const showEditDialog = ref(false)
const selectedUser = ref(null)

const showFilters = computed({
    get() {
        return preferencesStore.getPreference('display_filters', true)
    },
    set(value) {
        preferencesStore.updatePreference('display_filters', value)
        toast.success('Préférences mises à jour')
    }
})

const getInitials = (name, email) => {
    if (name) {
        return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()
    }
    return email ? email.substring(0, 2).toUpperCase() : '??'
}

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
    selectedFilters.speciality_ids = []
    applyFilters()
}

const applyFilters = () => {
    currentPage.value = 1
    fetchOperators()
}

const fetchOperators = async () => {
    loading.value = true
    error.value = null

    try {
        const params = {
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        if (selectedFilters.speciality_ids.length > 0) {
            params.speciality_ids = selectedFilters.speciality_ids
        }

        if (searchQuery.value && searchQuery.value.trim().length >= 2) {
            params.q = searchQuery.value.trim()
        }

        const response = await fetcher.get('/operators', { params })
        operators.value = response.data.items || []
        totalItems.value = response.data.total || 0
        totalPages.value = response.data.total_pages || 1
        currentPage.value = response.data.page || 1
    } catch (err) {
        console.error('Erreur lors du chargement des techniciens:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const fetchSpecialities = async () => {
    try {
        const response = await fetcher.get('/job-speciality')
        availableSpecialities.value = response.data || []
    } catch (err) {
        console.error('Erreur lors du chargement des spécialités:', err)
    }
}

const debouncedSearchOperators = debounce(() => {
    currentPage.value = 1
    fetchOperators()
}, 300)

const handleCreate = () => {
    selectedUser.value = { role: 'OPERATOR' }
    showEditDialog.value = true
}

const editOperator = (operator) => {
    selectedUser.value = operator
    showEditDialog.value = true
}

const handleSearch = () => {
    debouncedSearchOperators()
}

const handlePageChange = (page) => {
    currentPage.value = page
    fetchOperators()
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    fetchOperators()
}

const refreshList = () => {
    fetchOperators()
}

useBus(bus, 'user-edit-dialog:update-open', (event) => {
    showEditDialog.value = event.detail
})

useBus(bus, 'user-edit-dialog:user-updated', () => {
    refreshList()
})

onMounted(() => {
    fetchOperators()
    fetchSpecialities()
})
</script>