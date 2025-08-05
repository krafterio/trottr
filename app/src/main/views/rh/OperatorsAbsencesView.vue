<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-0">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Absences / Congés</h1>
                    <p class="text-neutral-600">Gestion des absences des techniciens</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouvelle absence
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Type d'absence</h4>
                        <div class="space-y-2">
                            <label v-for="option in unavailabilityTypeOptions" :key="option.value"
                                class="flex items-center">
                                <Checkbox :checked="selectedFilters.type?.includes(option.value) || false"
                                    @update:checked="toggleFilter('type', option.value)" />
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
                            <Input type="text" placeholder="Rechercher une absence..." class="h-9 pl-10 pr-4 py-2 w-64"
                                v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} absences</span>
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

                <div v-else-if="unavailabilities.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <CalendarIcon class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre première absence</h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Gérez les absences et congés de vos techniciens pour une meilleure planification des
                            interventions.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Ajouter une absence
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
                                <TableHead>Technicien</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Début</TableHead>
                                <TableHead>Fin</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead class="w-10"></TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="unavailability in unavailabilities" :key="unavailability.id"
                                class="hover:bg-neutral-50">
                                <TableCell @click.stop class="ps-3">
                                    <Checkbox :checked="selectedUnavailabilities.includes(unavailability.id)"
                                        @update:checked="toggleUnavailabilitySelection(unavailability.id)" />
                                </TableCell>
                                <TableCell class="font-medium text-neutral-900">
                                    {{ unavailability.user?.name || unavailability.user?.email }}
                                </TableCell>
                                <TableCell>
                                    <Badge :class="getUnavailabilityTypeColor(unavailability.type)">
                                        {{ getUnavailabilityTypeLabel(unavailability.type) }}
                                    </Badge>
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ formatDate(unavailability.start) }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ formatDate(unavailability.end) }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ unavailability.description || '-' }}
                                </TableCell>
                                <TableCell @click.stop>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger as-child>
                                            <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                <MoreVertical class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem @click="handleEdit(unavailability)">
                                                <Edit class="mr-2 h-4 w-4" />
                                                Modifier
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="handleDelete(unavailability)"
                                                class="text-red-600">
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

        <Dialog :open="dialogOpen" @update:open="dialogOpen = false">
            <DialogContent class="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>{{ isEdit ? 'Modifier l\'absence' : 'Nouvelle absence' }}</DialogTitle>
                    <DialogDescription>
                        Informations de l'absence
                    </DialogDescription>
                </DialogHeader>
                <form @submit.prevent="handleSubmit" class="space-y-4">
                    <div class="grid gap-2">
                        <Label for="user">Technicien *</Label>
                        <UserSelect v-model="form.user" placeholder="Sélectionner un technicien" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="type">Type d'absence *</Label>
                        <Select v-model="form.type" required>
                            <SelectTrigger>
                                <SelectValue placeholder="Sélectionner un type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="option in unavailabilityTypeOptions" :key="option.value"
                                    :value="option.value">
                                    {{ option.label }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div class="grid grid-cols-2 gap-4">
                        <div class="grid gap-2">
                            <Label for="start">Date de début *</Label>
                            <Popover>
                                <PopoverTrigger as-child>
                                    <Button variant="outline" class="justify-start text-left font-normal">
                                        <CalendarIcon class="mr-2 h-4 w-4" />
                                        {{ startDateValue ? df.format(toDate(startDateValue)) : 'Sélectionner une date'
                                        }}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent class="w-auto p-0">
                                    <Calendar v-model="startDateValue" calendar-label="Date de début" initial-focus
                                        locale="fr-FR" />
                                </PopoverContent>
                            </Popover>
                        </div>
                        <div class="grid gap-2">
                            <Label for="end">Date de fin *</Label>
                            <Popover>
                                <PopoverTrigger as-child>
                                    <Button variant="outline" class="justify-start text-left font-normal">
                                        <CalendarIcon class="mr-2 h-4 w-4" />
                                        {{ endDateValue ? df.format(toDate(endDateValue)) : 'Sélectionner une date' }}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent class="w-auto p-0">
                                    <Calendar v-model="endDateValue" calendar-label="Date de fin" initial-focus
                                        locale="fr-FR" />
                                </PopoverContent>
                            </Popover>
                        </div>
                    </div>

                    <div class="grid gap-2">
                        <Label for="description">Description</Label>
                        <Textarea v-model="form.description" placeholder="Description de l'absence..." rows="3" />
                    </div>
                </form>
                <DialogFooter>
                    <Button variant="outline" @click="dialogOpen = false">Annuler</Button>
                    <Button @click="handleSubmit" :disabled="loading">
                        {{ loading ? 'Enregistrement...' : (isEdit ? 'Modifier' : 'Créer') }}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>

    </div>
</template>

<script setup>
import UserSelect from '@/common/components/form/user-select/UserSelect.vue'
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Calendar } from '@/common/components/ui/calendar'
import { Checkbox } from '@/common/components/ui/checkbox'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/common/components/ui/popover'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import { Textarea } from '@/common/components/ui/textarea'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useUnavailability } from '@/common/composables/useUnavailability'
import TablePagination from '@/main/components/TablePagination.vue'
import { usePreferencesStore } from '@/main/stores/preferences'
import { CalendarDate, DateFormatter } from '@internationalized/date'
import { toDate } from 'reka-ui/date'

import { debounce } from 'lodash'
import { CalendarIcon, Download, Edit, MoreVertical, PanelLeftClose, PanelLeftOpen, Plus, RotateCcw, Search, Trash } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'

const fetcher = useFetcher()
const {
    getUnavailabilityTypeLabel,
    getUnavailabilityTypeOptions,
    getUnavailabilityTypeColor,
    fetchUnavailabilities,
    createUnavailability,
    updateUnavailability,
    deleteUnavailability
} = useUnavailability()
const preferencesStore = usePreferencesStore()

const unavailabilities = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedUnavailabilities = ref([])
const selectedUnavailabilityForDelete = ref(null)
const selectedFilters = reactive({
    type: []
})

const dialogOpen = ref(false)
const isEdit = ref(false)
const users = ref([])
const form = reactive({
    user: '',
    type: '',
    start: '',
    end: '',
    description: ''
})

const df = new DateFormatter('fr-FR', {
    dateStyle: 'long',
})

const startDateValue = computed({
    get: () => {
        if (!form.start) return undefined
        try {
            const date = new Date(form.start)
            return new CalendarDate(date.getFullYear(), date.getMonth() + 1, date.getDate())
        } catch (error) {
            console.error('Erreur parsing date start:', error)
            return undefined
        }
    },
    set: (val) => {
        if (val) {
            const startDate = new Date(val.toString())
            startDate.setHours(0, 0, 0, 0)
            form.start = startDate.toISOString()
        } else {
            form.start = ''
        }
    }
})

const endDateValue = computed({
    get: () => {
        if (!form.end) return undefined
        try {
            const date = new Date(form.end)
            return new CalendarDate(date.getFullYear(), date.getMonth() + 1, date.getDate())
        } catch (error) {
            console.error('Erreur parsing date end:', error)
            return undefined
        }
    },
    set: (val) => {
        if (val) {
            const endDate = new Date(val.toString())
            endDate.setHours(23, 59, 59, 999)
            form.end = endDate.toISOString()
        } else {
            form.end = ''
        }
    }
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

const unavailabilityTypeOptions = getUnavailabilityTypeOptions()

const selectAll = computed({
    get() {
        return unavailabilities.value.length > 0 && selectedUnavailabilities.value.length === unavailabilities.value.length
    },
    set(value) {
        if (value) {
            selectedUnavailabilities.value = unavailabilities.value.map(u => u.id)
        } else {
            selectedUnavailabilities.value = []
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
    selectedFilters.type = []
    applyFilters()
}

const applyFilters = () => {
    currentPage.value = 1
    fetchUnavailabilitiesList()
}

const fetchUnavailabilitiesList = async () => {
    loading.value = true
    error.value = null

    try {
        const params = {
            page: currentPage.value,
            per_page: itemsPerPage.value
        }

        if (selectedFilters.type.length > 0) {
            params.type = selectedFilters.type
        }

        const response = await fetchUnavailabilities(params)
        unavailabilities.value = response.items || []
        totalItems.value = response.total || 0
        totalPages.value = response.total_pages || 1
        currentPage.value = response.page || 1
    } catch (err) {
        console.error('Erreur lors du chargement des indisponibilités:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchUnavailabilities = async (query) => {
    if (!query || query.trim().length < 2) {
        currentPage.value = 1
        fetchUnavailabilitiesList()
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

        if (selectedFilters.type.length > 0) {
            params.type = selectedFilters.type
        }

        const response = await fetchUnavailabilities(params)
        unavailabilities.value = response.items || []
        totalItems.value = response.total || 0
        totalPages.value = response.total_pages || 1
        currentPage.value = response.page || 1
    } catch (err) {
        console.error('Erreur lors de la recherche:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const debouncedSearchUnavailabilities = debounce(searchUnavailabilities, 300)

const handleCreate = () => {
    isEdit.value = false
    form.user = ''
    form.type = ''
    form.start = ''
    form.end = ''
    form.description = ''
    selectedUnavailabilityForDelete.value = null
    dialogOpen.value = true
}

const handleEdit = (unavailability) => {
    isEdit.value = true
    form.user = unavailability.user.id
    form.type = unavailability.type
    form.description = unavailability.description || ''
    form.start = unavailability.start || ''
    form.end = unavailability.end || ''
    selectedUnavailabilityForDelete.value = unavailability
    dialogOpen.value = true
}

const handleSubmit = async () => {
    if (!form.user || !form.type || !form.start || !form.end) {
        toast.error('Veuillez remplir tous les champs obligatoires')
        return
    }

    if (new Date(form.start) >= new Date(form.end)) {
        toast.error('La date de fin doit être postérieure à la date de début')
        return
    }

    loading.value = true
    try {
        const userId = typeof form.user === 'object' ? form.user.id : form.user

        const data = {
            user: parseInt(userId),
            type: form.type,
            start: form.start,
            end: form.end,
            description: form.description
        }

        if (isEdit.value) {
            await updateUnavailability(selectedUnavailabilityForDelete.value.id, data)
        } else {
            await createUnavailability(data)
        }

        dialogOpen.value = false
        refreshList()
    } catch (err) {
        console.error('Erreur lors de la sauvegarde:', err)
    } finally {
        loading.value = false
    }
}

const handleSearch = () => {
    debouncedSearchUnavailabilities(searchQuery.value)
}

const handlePageChange = (page) => {
    currentPage.value = page
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchUnavailabilities(searchQuery.value)
    } else {
        fetchUnavailabilitiesList()
    }
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchUnavailabilities(searchQuery.value)
    } else {
        fetchUnavailabilitiesList()
    }
}

const toggleSelectAll = () => {
    selectAll.value = !selectAll.value
}

const toggleUnavailabilitySelection = (unavailabilityId) => {
    const index = selectedUnavailabilities.value.indexOf(unavailabilityId)
    if (index > -1) {
        selectedUnavailabilities.value.splice(index, 1)
    } else {
        selectedUnavailabilities.value.push(unavailabilityId)
    }
}

const handleDelete = (unavailability) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer l\'absence',
        message: 'Êtes-vous sûr de vouloir supprimer cette absence ?',
        itemName: `${unavailability.user?.name || unavailability.user?.email} - ${getUnavailabilityTypeLabel(unavailability.type)}`,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-unavailability:confirmed'
    })

    selectedUnavailabilityForDelete.value = unavailability
}

const deleteUnavailabilityItem = async () => {
    if (!selectedUnavailabilityForDelete.value) return

    try {
        await deleteUnavailability(selectedUnavailabilityForDelete.value.id)
        bus.trigger('confirm-delete-dialog:close')
        refreshList()
        selectedUnavailabilityForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        bus.trigger('confirm-delete-dialog:close')
    }
}

const refreshList = () => {
    selectedUnavailabilities.value = []
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchUnavailabilities(searchQuery.value)
    } else {
        fetchUnavailabilitiesList()
    }
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleDateString('fr-FR')
}



useBus(bus, 'unavailability-saved', () => {
    refreshList()
})

useBus(bus, 'unavailability-created-stay', () => {
    refreshList()
})

useBus(bus, 'confirm-delete-unavailability:confirmed', () => {
    deleteUnavailabilityItem()
})

onMounted(() => {
    fetchUnavailabilitiesList()
})
</script>