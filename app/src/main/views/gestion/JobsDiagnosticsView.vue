<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-0">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Diagnostics</h1>
                    <p class="text-neutral-600">Gestion des diagnostics d'intervention</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="handleCreate">
                        <Plus class="h-4 w-4" />
                        Nouveau diagnostic
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
                            <Input type="text" placeholder="Rechercher un diagnostic..."
                                class="h-9 pl-10 pr-4 py-2 w-64" v-model="searchQuery" @input="handleSearch" />
                        </div>
                        <span class="text-sm text-muted-foreground">{{ totalItems }} diagnostics</span>
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

                <div v-else-if="diagnostics.length === 0" class="flex-1 flex items-center justify-center py-12">
                    <div class="text-center py-8">
                        <div
                            class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                            <Stethoscope class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                        </div>
                        <h3 class="text-lg font-semibold text-neutral-900 mb-2">Créez votre premier diagnostic
                            d'intervention
                        </h3>
                        <p class="text-neutral-600 mb-6 max-w-md mx-auto">
                            Les diagnostics permettent de catégoriser et analyser les problèmes rencontrés lors des
                            interventions.
                            Commencez par ajouter vos diagnostics pour mieux organiser vos interventions.
                        </p>
                        <Button @click="handleCreate" class="inline-flex items-center">
                            <Plus class="w-4 h-4 mr-2" />
                            Ajouter un diagnostic
                        </Button>
                    </div>
                </div>

                <div v-else>
                    <Table>
                        <TableHeader>
                            <TableRow class="bg-neutral-50 border-b uppercase tracking-wider text-xs text-neutral-500">
                                <TableHead class="ps-3 w-8"></TableHead>
                                <TableHead>Diagnostic</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead class="w-10"></TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="diagnostics" :animation="200" handle=".drag-handle" tag="tbody"
                            @end="onDiagnosticReorder">
                            <TableRow v-for="diagnostic in diagnostics" :key="diagnostic.id"
                                class="hover:bg-neutral-50">
                                <TableCell @click.stop class="ps-3">
                                    <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                        <GripVertical class="h-4 w-4" />
                                    </div>
                                </TableCell>
                                <TableCell class="font-medium text-neutral-900">
                                    <button @click="handleEdit(diagnostic)"
                                        class="text-primary hover:text-neutral-700  cursor-pointer underline">
                                        {{ diagnostic.name }}
                                    </button>
                                </TableCell>
                                <TableCell class="text-neutral-900">
                                    {{ diagnostic.description }}
                                </TableCell>
                                <TableCell @click.stop>
                                    <DropdownMenu>
                                        <DropdownMenuTrigger as-child>
                                            <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                <MoreVertical class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem @click="handleEdit(diagnostic)">
                                                <Pen class="h-4 w-4" />
                                                Modifier
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="handleDelete(diagnostic)">
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
                    <DialogTitle>{{ isEdit ? 'Modifier le diagnostic' : 'Nouveau diagnostic' }}</DialogTitle>
                    <DialogDescription>
                        Informations du diagnostic
                    </DialogDescription>
                </DialogHeader>
                <form @submit.prevent="handleSubmit" class="space-y-4">
                    <div class="grid gap-2">
                        <Label for="name">Nom du diagnostic *</Label>
                        <Input v-model="form.name" placeholder="Ex: Panne électrique" required />
                    </div>

                    <div class="grid gap-2">
                        <Label for="description">Description</Label>
                        <Textarea v-model="form.description" placeholder="Description détaillée du diagnostic..."
                            rows="4" />
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
import { Download, GripVertical, MoreVertical, PanelLeftClose, PanelLeftOpen, Pen, Plus, RotateCcw, Search, Stethoscope, Trash } from 'lucide-vue-next'
import { computed, onMounted, reactive, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()
const preferencesStore = usePreferencesStore()
const workspaceStore = useWorkspaceStore()

const diagnostics = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const itemsPerPage = ref(50)
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedDiagnostics = ref([])
const selectedDiagnosticForDelete = ref(null)
const selectedFilters = reactive({})

// Dialog variables
const dialogOpen = ref(false)
const isEdit = ref(false)
const form = reactive({
    name: '',
    description: ''
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
        return diagnostics.value.length > 0 && selectedDiagnostics.value.length === diagnostics.value.length
    },
    set(value) {
        if (value) {
            selectedDiagnostics.value = diagnostics.value.map(d => d.id)
        } else {
            selectedDiagnostics.value = []
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
    fetchDiagnostics()
}

const fetchDiagnostics = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/job-diagnostics')
        diagnostics.value = response.data || []
        totalItems.value = diagnostics.value.length
        totalPages.value = 1
        currentPage.value = 1
    } catch (err) {
        console.error('Erreur lors du chargement des diagnostics:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const searchDiagnostics = async (query) => {
    if (!query || query.trim().length < 2) {
        currentPage.value = 1
        fetchDiagnostics()
        return
    }

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/job-diagnostics')
        const allDiagnostics = response.data || []

        const filteredDiagnostics = allDiagnostics.filter(diagnostic =>
            diagnostic.name.toLowerCase().includes(query.toLowerCase()) ||
            (diagnostic.description && diagnostic.description.toLowerCase().includes(query.toLowerCase()))
        )

        diagnostics.value = filteredDiagnostics
        totalItems.value = filteredDiagnostics.length
        totalPages.value = 1
        currentPage.value = 1
    } catch (err) {
        console.error('Erreur lors de la recherche:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const debouncedSearchDiagnostics = debounce(searchDiagnostics, 300)

const handleCreate = () => {
    isEdit.value = false
    form.name = ''
    form.description = ''
    selectedDiagnosticForDelete.value = null
    dialogOpen.value = true
}

const handleEdit = (diagnostic) => {
    isEdit.value = true
    form.name = diagnostic.name
    form.description = diagnostic.description
    selectedDiagnosticForDelete.value = diagnostic
    dialogOpen.value = true
}

const handleSubmit = async () => {
    if (!form.name.trim()) {
        toast.error('Le nom du diagnostic est obligatoire')
        return
    }

    loading.value = true
    try {
        if (isEdit.value) {
            await fetcher.patch(`/job-diagnostics/${selectedDiagnosticForDelete.value.id}`, form)
            toast.success('Diagnostic modifié avec succès')
        } else {
            await fetcher.post('/job-diagnostics', form)
            toast.success('Diagnostic créé avec succès')
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

const handleRowClick = (diagnostic) => {
    router.push(`/diagnostic/${diagnostic.id}`)
}

const handleView = (diagnostic) => {
    router.push(`/diagnostic/${diagnostic.id}`)
}

const handleSearch = () => {
    debouncedSearchDiagnostics(searchQuery.value)
}

const handlePageChange = (page) => {
    currentPage.value = page
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchDiagnostics(searchQuery.value)
    } else {
        fetchDiagnostics()
    }
}

const handleItemsPerPageChange = (itemsCount) => {
    itemsPerPage.value = parseInt(itemsCount)
    currentPage.value = 1
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchDiagnostics(searchQuery.value)
    } else {
        fetchDiagnostics()
    }
}

const toggleSelectAll = () => {
    selectAll.value = !selectAll.value
}

const toggleDiagnosticSelection = (diagnosticId) => {
    const index = selectedDiagnostics.value.indexOf(diagnosticId)
    if (index > -1) {
        selectedDiagnostics.value.splice(index, 1)
    } else {
        selectedDiagnostics.value.push(diagnosticId)
    }
}

const handleDelete = (diagnostic) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le diagnostic',
        message: 'Êtes-vous sûr de vouloir supprimer ce diagnostic ?',
        itemName: diagnostic.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-diagnostic:confirmed'
    })

    selectedDiagnosticForDelete.value = diagnostic
}

const deleteDiagnostic = async () => {
    if (!selectedDiagnosticForDelete.value) return

    try {
        await fetcher.delete(`/job-diagnostics/${selectedDiagnosticForDelete.value.id}`)
        toast.success('Diagnostic supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        refreshList()
        selectedDiagnosticForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const refreshList = () => {
    selectedDiagnostics.value = []
    if (searchQuery.value && searchQuery.value.trim().length >= 2) {
        searchDiagnostics(searchQuery.value)
    } else {
        fetchDiagnostics()
    }
}

useBus(bus, 'job-diagnostic-saved', () => {
    refreshList()
})

useBus(bus, 'job-diagnostic-created-stay', () => {
    refreshList()
})

useBus(bus, 'confirm-delete-diagnostic:confirmed', () => {
    deleteDiagnostic()
})

const onDiagnosticReorder = async () => {
    try {
        const reorderedDiagnostics = diagnostics.value.map((diagnostic, index) => ({
            id: diagnostic.id,
            sequence: index + 1
        }))

        await fetcher.put('/job-diagnostics/reorder', { diagnostics: reorderedDiagnostics })
        toast.success('Diagnostics réorganisés avec succès')
    } catch (error) {
        console.error('Erreur lors de la réorganisation des diagnostics:', error)
        toast.error(error.message || 'Erreur lors de la réorganisation des diagnostics')
        await fetchDiagnostics()
    }
}

onMounted(() => {
    if (!workspaceStore.workspace?.use_diagnostics) {
        router.push('/jobs')
        return
    }

    fetchDiagnostics()
})
</script>