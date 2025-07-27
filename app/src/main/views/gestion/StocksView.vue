<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Stock pièces détachées</h1>
                    <p class="text-neutral-600">Gestion des stocks et emplacements</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline" @click="openLocationsDialog">
                        <Settings class="h-4 w-4" />
                        Emplacements
                    </Button>
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="openCreateDialog">
                        <Plus class="h-4 w-4" />
                        Nouveau stock
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
                                <span class="ml-auto text-xs text-neutral-400">32</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Chauffage</span>
                                <span class="ml-auto text-xs text-neutral-400">28</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Climatisation</span>
                                <span class="ml-auto text-xs text-neutral-400">15</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Outillage</span>
                                <span class="ml-auto text-xs text-neutral-400">8</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Emplacement</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Entrepôt A</span>
                                <span class="ml-auto text-xs text-neutral-400">68</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Entrepôt B</span>
                                <span class="ml-auto text-xs text-neutral-400">35</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Camion 1</span>
                                <span class="ml-auto text-xs text-neutral-400">12</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Camion 2</span>
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
                                <span class="text-sm text-muted-foreground">128 références en stock</span>

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
                                        Produit
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Catégorie
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Emplacement
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Quantité en stock
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="stock in stocks" :key="stock.id" class="hover:bg-neutral-50 cursor-pointer"
                                    @click.stop="editStock(stock)">
                                    <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium text-neutral-900">{{ stock.product }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge variant="outline">{{ stock.category }}</Badge>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge variant="outline">
                                            <MapPin class="h-4 w-4" />
                                            {{ stock.location }}
                                        </Badge>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900" :class="{
                                            'text-red-600': stock.quantity === 0,
                                            'text-orange-600': stock.quantity > 0 && stock.quantity <= 5,
                                            'text-green-600': stock.quantity > 5
                                        }">
                                            {{ stock.quantity }}
                                        </div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Button variant="ghost" size="sm" @click.stop="editStock(stock)">
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

        <TablePagination :current-page="1" :total-pages="7" :total-items="128" :items-per-page="20"
            :position-classes="`bottom-0 ${showFilters ? 'left-80' : 'left-32'} right-0`"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />

        <!-- Dialog d'édition des stocks -->
        <Dialog v-model:open="isEditModalOpen">
            <DialogContent class="max-w-md">
                <DialogHeader>
                    <DialogTitle>{{ editingStock?.id ? 'Modifier' : 'Ajouter' }} un stock</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Produit</label>
                        <Input v-model="editingStock.product" class="mt-1" placeholder="Ex: Disjoncteur 16A" />
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Catégorie</label>
                        <Select v-model="editingStock.category">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner une catégorie" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Électricité">Électricité</SelectItem>
                                <SelectItem value="Plomberie">Plomberie</SelectItem>
                                <SelectItem value="Chauffage">Chauffage</SelectItem>
                                <SelectItem value="Climatisation">Climatisation</SelectItem>
                                <SelectItem value="Outillage">Outillage</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Emplacement</label>
                        <Select v-model="editingStock.location">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner un emplacement" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="location in locations" :key="location.id" :value="location.name">
                                    {{ location.name }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Quantité en stock</label>
                        <Input v-model="editingStock.quantity" type="number" class="mt-1" placeholder="Ex: 25" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Annuler</Button>
                    <Button @click="saveStock">{{ editingStock?.id ? 'Modifier' : 'Ajouter' }}</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>

        <!-- Dialog de gestion des emplacements -->
        <Dialog v-model:open="isLocationsModalOpen">
            <DialogContent class="max-w-2xl">
                <DialogHeader>
                    <DialogTitle>Gestion des emplacements</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <p class="text-sm text-neutral-600">Glissez-déposez pour réorganiser l'ordre des emplacements
                        </p>
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
                                        Emplacement</th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider w-24">
                                        Utilisé</th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider w-24">
                                        Actions</th>
                                </tr>
                            </thead>
                            <VueDraggable v-model="locations" :animation="200" handle=".drag-handle" tag="tbody">
                                <tr v-for="location in locations" :key="location.id">
                                    <td class="px-2 py-1 max-w-4">
                                        <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                            <GripVertical class="h-4 w-4" />
                                        </div>
                                    </td>
                                    <td class="px-4 py-1">
                                        <div class="text-sm font-medium text-neutral-900">{{ location.name }}</div>
                                    </td>
                                    <td class="px-4 py-1">
                                        <Badge
                                            :class="location.isUsed ? 'bg-green-100 text-green-800' : 'bg-neutral-100 text-neutral-600'">
                                            {{ location.isUsed ? 'Utilisé' : 'Non utilisé' }}
                                        </Badge>
                                    </td>
                                    <td class="px-4 py-1">
                                        <div class="flex items-center space-x-1">
                                            <Button variant="ghost" size="sm" @click="editLocation(location)">
                                                <Edit class="h-4 w-4" />
                                            </Button>
                                            <Button variant="ghost" size="sm" @click="removeLocation(location.id)"
                                                :disabled="location.isUsed">
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
                    <Button variant="outline" @click="closeLocationsDialog">Fermer</Button>
                    <Button @click="openCreateLocationDialog">
                        <Plus class="h-4 w-4 mr-2" />
                        Ajouter un emplacement
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>

        <!-- Dialog d'édition des emplacements -->
        <Dialog v-model:open="isEditLocationModalOpen">
            <DialogContent class="max-w-md">
                <DialogHeader>
                    <DialogTitle>{{ editingLocation?.id ? 'Modifier' : 'Ajouter' }} un emplacement</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Nom de l'emplacement</label>
                        <Input v-model="editingLocation.name" class="mt-1" placeholder="Ex: Entrepôt A" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEditLocation">Annuler</Button>
                    <Button @click="saveLocation">{{ editingLocation?.id ? 'Modifier' : 'Ajouter' }}</Button>
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
    MapPin,
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
const isLocationsModalOpen = ref(false)
const isEditLocationModalOpen = ref(false)

const editingStock = ref({
    id: null,
    product: '',
    category: '',
    location: '',
    quantity: 0
})

const editingLocation = ref({
    id: null,
    name: '',
    isUsed: false
})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const openCreateDialog = () => {
    editingStock.value = {
        id: null,
        product: '',
        category: '',
        location: '',
        quantity: 0
    }
    isEditModalOpen.value = true
}

const editStock = (stock) => {
    editingStock.value = { ...stock }
    isEditModalOpen.value = true
}

const cancelEdit = () => {
    editingStock.value = {
        id: null,
        product: '',
        category: '',
        location: '',
        quantity: 0
    }
    isEditModalOpen.value = false
}

const saveStock = () => {
    if (editingStock.value.id) {
        const index = stocks.findIndex(s => s.id === editingStock.value.id)
        if (index !== -1) {
            stocks[index] = { ...editingStock.value }
        }
    } else {
        const newId = Math.max(...stocks.map(s => s.id)) + 1
        stocks.push({
            ...editingStock.value,
            id: newId
        })
    }
    cancelEdit()
}

const openLocationsDialog = () => {
    isLocationsModalOpen.value = true
}

const closeLocationsDialog = () => {
    isLocationsModalOpen.value = false
}

const openCreateLocationDialog = () => {
    editingLocation.value = {
        id: null,
        name: '',
        isUsed: false
    }
    isEditLocationModalOpen.value = true
}

const editLocation = (location) => {
    editingLocation.value = { ...location }
    isEditLocationModalOpen.value = true
}

const cancelEditLocation = () => {
    editingLocation.value = {
        id: null,
        name: '',
        isUsed: false
    }
    isEditLocationModalOpen.value = false
}

const saveLocation = () => {
    if (editingLocation.value.id) {
        const index = locations.findIndex(loc => loc.id === editingLocation.value.id)
        if (index !== -1) {
            locations[index] = { ...editingLocation.value }
        }
    } else {
        const newId = Math.max(...locations.map(loc => loc.id)) + 1
        locations.push({
            ...editingLocation.value,
            id: newId,
            sequence: locations.length + 1
        })
    }
    cancelEditLocation()
}

const removeLocation = (id) => {
    locations.splice(locations.findIndex(loc => loc.id === id), 1)
}

const locations = ref([
    { id: 1, name: 'Entrepôt A', isUsed: true, sequence: 1 },
    { id: 2, name: 'Entrepôt B', isUsed: true, sequence: 2 },
    { id: 3, name: 'Camion 1', isUsed: true, sequence: 3 },
    { id: 4, name: 'Camion 2', isUsed: true, sequence: 4 },
    { id: 5, name: 'Atelier', isUsed: false, sequence: 5 }
])

const stocks = [
    { id: 1, product: 'Disjoncteur 16A', category: 'Électricité', location: 'Entrepôt A', quantity: 25 },
    { id: 2, product: 'Robinet mitigeur', category: 'Plomberie', location: 'Entrepôt A', quantity: 8 },
    { id: 3, product: 'Thermostat programmable', category: 'Chauffage', location: 'Entrepôt B', quantity: 12 },
    { id: 4, product: 'Prise électrique', category: 'Électricité', location: 'Camion 1', quantity: 45 },
    { id: 5, product: 'Joint d\'étanchéité', category: 'Plomberie', location: 'Entrepôt A', quantity: 0 },
    { id: 6, product: 'Radiateur 1000W', category: 'Chauffage', location: 'Entrepôt B', quantity: 3 },
    { id: 7, product: 'Interrupteur va-et-vient', category: 'Électricité', location: 'Camion 2', quantity: 18 },
    { id: 8, product: 'Siphon lavabo', category: 'Plomberie', location: 'Entrepôt A', quantity: 22 },
    { id: 9, product: 'Vanne thermostatique', category: 'Chauffage', location: 'Entrepôt B', quantity: 15 },
    { id: 10, product: 'Filtre climatisation', category: 'Climatisation', location: 'Camion 1', quantity: 6 }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>