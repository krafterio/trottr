<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Opérations</h1>
                    <p class="text-neutral-600">Gestion des opérations d'intervention</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline" @click="openCategoriesDialog">
                        <Settings class="h-4 w-4" />
                        Catégories d'opérations
                    </Button>
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="openCreateDialog">
                        <Plus class="h-4 w-4" />
                        Nouvelle opération
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Catégorie</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Électricité</span>
                                <span class="ml-auto text-xs text-neutral-400">45</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Plomberie</span>
                                <span class="ml-auto text-xs text-neutral-400">38</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Chauffage</span>
                                <span class="ml-auto text-xs text-neutral-400">32</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Climatisation</span>
                                <span class="ml-auto text-xs text-neutral-400">28</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Maintenance</span>
                                <span class="ml-auto text-xs text-neutral-400">13</span>
                            </label>
                        </div>
                    </div>

                    <Button variant="outline" size="sm" class="w-full">
                        <RotateCcw class="h-4 w-4 mr-2" />
                        Réinitialiser
                    </Button>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto">
                <div class="">
                    <div class="px-6 py-4 border-b">
                        <div class="flex items-center justify-between">
                            <div class="relative">
                                <Search
                                    class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                                <Input type="text" placeholder="Recherche rapide..." class="h-9 pl-10 pr-4 py-2 w-64" />
                            </div>

                            <div class="flex items-center space-x-3">
                                <span class="text-sm text-muted-foreground">156 opérations</span>

                                <Button variant="outline" size="sm" class="w-8">
                                    <MoreVertical class="h-4 w-4" />
                                </Button>
                                <Button variant="outline">
                                    <Columns class="h-4 w-4" />
                                    Colonnes
                                    <ChevronDown class="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-neutral-50 border-b">
                                <tr>
                                    <th
                                        class="px-3 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-5">
                                        <Checkbox />
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Libellé
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Catégorie
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Utilisations
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="operation in operations" :key="operation.id"
                                    class="hover:bg-neutral-50 cursor-pointer" @click.stop="editOperation(operation)">
                                    <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium text-neutral-900">{{ operation.label }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge variant="outline">{{ operation.category }}</Badge>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ operation.usageCount }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Button variant="ghost" size="sm" @click.stop="editOperation(operation)">
                                            <Edit class="h-4 w-4" />
                                        </Button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <TablePagination :current-page="1" :total-pages="8" :total-items="156" :items-per-page="20"
            :position-classes="`bottom-0 ${showFilters ? 'left-80' : 'left-32'} right-0`"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />

        <!-- Dialog d'édition des opérations -->
        <Dialog v-model:open="isEditModalOpen">
            <DialogContent class="max-w-md">
                <DialogHeader>
                    <DialogTitle>{{ editingOperation?.id ? 'Modifier' : 'Ajouter' }} une opération</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Libellé</label>
                        <Input v-model="editingOperation.label" class="mt-1"
                            placeholder="Ex: Remplacement prise électrique" />
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Catégorie</label>
                        <Select v-model="editingOperation.category">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner une catégorie" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="category in categories" :key="category.id" :value="category.name">
                                    {{ category.name }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Annuler</Button>
                    <Button @click="saveOperation">{{ editingOperation?.id ? 'Modifier' : 'Ajouter' }}</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>

        <!-- Dialog de gestion des catégories -->
        <Dialog v-model:open="isCategoriesModalOpen">
            <DialogContent class="max-w-2xl">
                <DialogHeader>
                    <DialogTitle>Gestion des catégories d'opérations</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <p class="text-sm text-neutral-600">Glissez-déposez pour réorganiser l'ordre des catégories</p>
                    </div>

                    <div class="border rounded-lg">
                        <table class="w-full">
                            <thead class="border-b">
                                <tr class="bg-neutral-50">
                                    <th
                                        class="px-2 py-2 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-2">
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Catégorie</th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider w-24">
                                        Utilisé</th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider w-24">
                                        Actions</th>
                                </tr>
                            </thead>
                            <VueDraggable v-model="categories" :animation="200" handle=".drag-handle" tag="tbody">
                                <tr v-for="category in categories" :key="category.id">
                                    <td class="px-2 py-1 max-w-4">
                                        <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                            <GripVertical class="h-4 w-4" />
                                        </div>
                                    </td>
                                    <td class="px-4 py-1">
                                        <div class="text-sm font-medium text-neutral-900">{{ category.name }}</div>
                                    </td>
                                    <td class="px-4 py-1">
                                        <Badge
                                            :class="category.isUsed ? 'bg-green-100 text-green-800' : 'bg-neutral-100 text-neutral-600'">
                                            {{ category.isUsed ? 'Utilisé' : 'Non utilisé' }}
                                        </Badge>
                                    </td>
                                    <td class="px-4 py-1">
                                        <div class="flex items-center space-x-1">
                                            <Button variant="ghost" size="sm" @click="editCategory(category)">
                                                <Edit class="h-4 w-4" />
                                            </Button>
                                            <Button variant="ghost" size="sm" @click="removeCategory(category.id)"
                                                :disabled="category.isUsed">
                                                <Trash class="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            </VueDraggable>
                        </table>
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="closeCategoriesDialog">Fermer</Button>
                    <Button @click="openCreateCategoryDialog">
                        <Plus class="h-4 w-4 mr-2" />
                        Ajouter une catégorie
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>

        <!-- Dialog d'édition des catégories -->
        <Dialog v-model:open="isEditCategoryModalOpen">
            <DialogContent class="max-w-md">
                <DialogHeader>
                    <DialogTitle>{{ editingCategory?.id ? 'Modifier' : 'Ajouter' }} une catégorie</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Nom de la catégorie</label>
                        <Input v-model="editingCategory.name" class="mt-1" placeholder="Ex: Électricité" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEditCategory">Annuler</Button>
                    <Button @click="saveCategory">{{ editingCategory?.id ? 'Modifier' : 'Ajouter' }}</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import Input from '@/common/components/ui/input/Input.vue'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    ChevronDown,
    Columns,
    Download,
    Edit,
    GripVertical,
    MoreVertical,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    RotateCcw,
    Search,
    Settings,
    Trash
} from 'lucide-vue-next'
import { ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'

const showFilters = ref(true)
const isEditModalOpen = ref(false)
const isCategoriesModalOpen = ref(false)
const isEditCategoryModalOpen = ref(false)

const editingOperation = ref({
    id: null,
    label: '',
    category: '',
    usageCount: 0
})

const editingCategory = ref({
    id: null,
    name: '',
    isUsed: false
})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const openCreateDialog = () => {
    editingOperation.value = {
        id: null,
        label: '',
        category: '',
        usageCount: 0
    }
    isEditModalOpen.value = true
}

const editOperation = (operation) => {
    editingOperation.value = { ...operation }
    isEditModalOpen.value = true
}

const cancelEdit = () => {
    editingOperation.value = {
        id: null,
        label: '',
        category: '',
        usageCount: 0
    }
    isEditModalOpen.value = false
}

const saveOperation = () => {
    if (editingOperation.value.id) {
        const index = operations.findIndex(op => op.id === editingOperation.value.id)
        if (index !== -1) {
            operations[index] = { ...editingOperation.value }
        }
    } else {
        const newId = Math.max(...operations.map(op => op.id)) + 1
        operations.push({
            ...editingOperation.value,
            id: newId
        })
    }
    cancelEdit()
}

const openCategoriesDialog = () => {
    isCategoriesModalOpen.value = true
}

const closeCategoriesDialog = () => {
    isCategoriesModalOpen.value = false
}

const openCreateCategoryDialog = () => {
    editingCategory.value = {
        id: null,
        name: '',
        isUsed: false
    }
    isEditCategoryModalOpen.value = true
}

const editCategory = (category) => {
    editingCategory.value = { ...category }
    isEditCategoryModalOpen.value = true
}

const cancelEditCategory = () => {
    editingCategory.value = {
        id: null,
        name: '',
        isUsed: false
    }
    isEditCategoryModalOpen.value = false
}

const saveCategory = () => {
    if (editingCategory.value.id) {
        const index = categories.findIndex(cat => cat.id === editingCategory.value.id)
        if (index !== -1) {
            categories[index] = { ...editingCategory.value }
        }
    } else {
        const newId = Math.max(...categories.map(cat => cat.id)) + 1
        categories.push({
            ...editingCategory.value,
            id: newId,
            sequence: categories.length + 1
        })
    }
    cancelEditCategory()
}

const removeCategory = (id) => {
    categories.splice(categories.findIndex(cat => cat.id === id), 1)
}

const categories = ref([
    { id: 1, name: 'Électricité', isUsed: true, sequence: 1 },
    { id: 2, name: 'Plomberie', isUsed: true, sequence: 2 },
    { id: 3, name: 'Chauffage', isUsed: true, sequence: 3 },
    { id: 4, name: 'Climatisation', isUsed: true, sequence: 4 },
    { id: 5, name: 'Maintenance', isUsed: false, sequence: 5 }
])

const operations = [
    { id: 1, label: 'Remplacement prise électrique', category: 'Électricité', usageCount: 45 },
    { id: 2, label: 'Réparation fuite robinet', category: 'Plomberie', usageCount: 38 },
    { id: 3, label: 'Entretien chaudière', category: 'Chauffage', usageCount: 32 },
    { id: 4, label: 'Installation interrupteur', category: 'Électricité', usageCount: 28 },
    { id: 5, label: 'Changement joint évier', category: 'Plomberie', usageCount: 25 },
    { id: 6, label: 'Nettoyage radiateur', category: 'Chauffage', usageCount: 22 },
    { id: 7, label: 'Test installation électrique', category: 'Électricité', usageCount: 20 },
    { id: 8, label: 'Débouchage canalisation', category: 'Plomberie', usageCount: 18 },
    { id: 9, label: 'Contrôle thermostat', category: 'Chauffage', usageCount: 15 },
    { id: 10, label: 'Maintenance climatisation', category: 'Climatisation', usageCount: 12 }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>