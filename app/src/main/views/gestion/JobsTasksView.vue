<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-0">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Tâches</h1>
                    <p class="text-neutral-600">Gestion des tâches d'intervention</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouvelle tâche
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
                            <Input type="text" placeholder="Rechercher une tâche..." class="h-9 pl-10 pr-4 py-2 w-64"
                                v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} tâches</span>
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

                <div v-else-if="tasks.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <ClipboardList class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre première tâche
                            d'intervention
                        </h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Les tâches permettent de décomposer les interventions en actions spécifiques.
                            Commencez par ajouter vos tâches pour mieux organiser vos interventions.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Ajouter une tâche
                        </Button>
                    </div>
                </div>

                <div v-else>
                    <Table>
                        <TableHeader>
                            <TableRow class="bg-neutral-50 border-b uppercase tracking-wider text-xs text-neutral-500">
                                <TableHead class="ps-3 w-8"></TableHead>
                                <TableHead>Tâche</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead>Prix par défaut</TableHead>
                                <TableHead class="w-10"></TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="tasks" :animation="200" handle=".drag-handle" tag="tbody"
                            @end="onTaskReorder">
                            <TableRow v-for="task in tasks" :key="task.id" class="hover:bg-neutral-50">
                                <TableCell @click.stop class="ps-3">
                                    <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                        <GripVertical class="h-4 w-4" />
                                    </div>
                                </TableCell>
                                <TableCell class="font-medium text-neutral-900">
                                    <button @click="handleEdit(task)"
                                        class="text-primary hover:text-neutral-700  cursor-pointer underline">
                                        {{ task.name }}
                                    </button>
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ task.description }}
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ formatPrice(task.default_price) }}
                                </TableCell>
                                <TableCell @click.stop>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger as-child>
                                            <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                <MoreVertical class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem @click="handleEdit(task)">
                                                <Pen class="h-4 w-4" />
                                                Modifier
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="handleDelete(task)">
                                                <Trash class="text-destructive h-4 w-4" />
                                                Supprimer
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </TableCell>
                            </TableRow>
                        </VueDraggable>
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
                    <DialogTitle>{{ isEdit ? 'Modifier la tâche' : 'Nouvelle tâche' }}</DialogTitle>
                    <DialogDescription>
                        Informations de la tâche
                    </DialogDescription>
                </DialogHeader>
                <form @submit.prevent="handleSubmit" class="space-y-4">
                    <div class="grid gap-2">
                        <Label for="name">Nom de la tâche *</Label>
                        <Input v-model="form.name" placeholder="Ex: Remplacement de pièce" required />
                    </div>

                    <div class="grid gap-2">
                        <Label for="description">Description</Label>
                        <Textarea v-model="form.description" placeholder="Description détaillée de la tâche..."
                            rows="4" />
                    </div>

                    <div class="grid gap-2">
                        <Label for="default_price">Prix par défaut (€)</Label>
                        <Input v-model="form.default_price" type="number" step="0.01" min="0" placeholder="0.00" />
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
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Table, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import { Textarea } from '@/common/components/ui/textarea'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import TablePagination from '@/main/components/TablePagination.vue'
import { usePreferencesStore } from '@/main/stores/preferences'
import { useWorkspaceStore } from '@/main/stores/workspace'

import { debounce } from 'lodash'
import { ClipboardList, Download, GripVertical, MoreVertical, PanelLeftClose, PanelLeftOpen, Pen, Plus, RotateCcw, Search, Trash } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()
const preferencesStore = usePreferencesStore()
const workspaceStore = useWorkspaceStore()

const tasks = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedTasks = ref([])
const selectedTaskForDelete = ref(null)
const selectedFilters = reactive({})

const dialogOpen = ref(false)
const isEdit = ref(false)
const form = reactive({
    name: '',
    description: '',
    default_price: 0.0
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

const selectAll = computed({
    get() {
        return tasks.value.length > 0 && selectedTasks.value.length === tasks.value.length
    },
    set(value) {
        if (value) {
            selectedTasks.value = tasks.value.map(t => t.id)
        } else {
            selectedTasks.value = []
        }
    }
})

const toggleFilters = async () => {
    showFilters.value = !showFilters.value
}

const resetFilters = () => {
    applyFilters()
}

const applyFilters = () => {
    currentPage.value = 1
    fetchTasks()
}

const fetchTasks = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/job-tasks')
        tasks.value = response.data || []
        totalItems.value = tasks.value.length
        totalPages.value = 1
        currentPage.value = 1
    } catch (err) {
        console.error('Erreur lors du chargement des tâches:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchTasks = async (query) => {
    if (!query || query.trim().length < 2) {
        currentPage.value = 1
        fetchTasks()
        return
    }

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/job-tasks')
        const allTasks = response.data || []

        const filteredTasks = allTasks.filter(task =>
            task.name.toLowerCase().includes(query.toLowerCase()) ||
            (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
        )

        tasks.value = filteredTasks
        totalItems.value = filteredTasks.length
        totalPages.value = 1
        currentPage.value = 1
    } catch (err) {
        console.error('Erreur lors de la recherche:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const debouncedSearchTasks = debounce(searchTasks, 300)

const handleCreate = () => {
    isEdit.value = false
    form.name = ''
    form.description = ''
    form.default_price = 0.0
    selectedTaskForDelete.value = null
    dialogOpen.value = true
}

const handleEdit = (task) => {
    isEdit.value = true
    form.name = task.name
    form.description = task.description
    form.default_price = task.default_price
    selectedTaskForDelete.value = task
    dialogOpen.value = true
}

const handleSubmit = async () => {
    if (!form.name.trim()) {
        toast.error('Le nom de la tâche est obligatoire')
        return
    }

    loading.value = true
    try {
        if (isEdit.value) {
            await fetcher.patch(`/job-tasks/${selectedTaskForDelete.value.id}`, form)
            toast.success('Tâche modifiée avec succès')
        } else {
            await fetcher.post('/job-tasks', form)
            toast.success('Tâche créée avec succès')
        }

        dialogOpen.value = false
        refreshList()
    } catch (err) {
        console.error('Erreur lors de la sauvegarde:', err)
        toast.error('Erreur lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}

const handleRowClick = (task) => {
    router.push(`/task/${task.id}`)
}

const handleView = (task) => {
    router.push(`/task/${task.id}`)
}

const handleSearch = () => {
    debouncedSearchTasks(searchQuery.value)
}

const handlePageChange = (page) => {
    currentPage.value = page
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchTasks(searchQuery.value)
    } else {
        fetchTasks()
    }
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchTasks(searchQuery.value)
    } else {
        fetchTasks()
    }
}

const toggleSelectAll = () => {
    selectAll.value = !selectAll.value
}

const toggleTaskSelection = (taskId) => {
    const index = selectedTasks.value.indexOf(taskId)
    if (index > -1) {
        selectedTasks.value.splice(index, 1)
    } else {
        selectedTasks.value.push(taskId)
    }
}

const handleDelete = (task) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer la tâche',
        message: 'Êtes-vous sûr de vouloir supprimer cette tâche ?',
        itemName: task.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-task:confirmed'
    })

    selectedTaskForDelete.value = task
}

const deleteTask = async () => {
    if (!selectedTaskForDelete.value) return

    try {
        await fetcher.delete(`/job-tasks/${selectedTaskForDelete.value.id}`)
        toast.success('Tâche supprimée avec succès')
        bus.trigger('confirm-delete-dialog:close')
        refreshList()
        selectedTaskForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const refreshList = () => {
    selectedTasks.value = []
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchTasks(searchQuery.value)
    } else {
        fetchTasks()
    }
}

const formatPrice = (price) => {
    if (price === null || price === undefined) return '0,00 €'
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(price)
}

useBus(bus, 'job-task-saved', () => {
    refreshList()
})

useBus(bus, 'job-task-created-stay', () => {
    refreshList()
})

useBus(bus, 'confirm-delete-task:confirmed', () => {
    deleteTask()
})

const onTaskReorder = async () => {
    try {
        const reorderedTasks = tasks.value.map((task, index) => ({
            id: task.id,
            sequence: index + 1
        }))

        await fetcher.put('/job-tasks/reorder', { tasks: reorderedTasks })
        toast.success('Tâches réorganisées avec succès')
    } catch (error) {
        console.error('Erreur lors de la réorganisation des tâches:', error)
        toast.error(error.message || 'Erreur lors de la réorganisation des tâches')
        await fetchTasks()
    }
}

onMounted(() => {
    fetchTasks()
})
</script>