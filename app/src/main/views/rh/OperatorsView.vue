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
                    <Button @click="openCreateDialog">
                        <Plus class="h-4 w-4" />
                        Nouveau technicien
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
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Électricité</span>
                                <span class="ml-auto text-xs text-neutral-400">8</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Plomberie</span>
                                <span class="ml-auto text-xs text-neutral-400">6</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Chauffage</span>
                                <span class="ml-auto text-xs text-neutral-400">5</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Climatisation</span>
                                <span class="ml-auto text-xs text-neutral-400">4</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Généraliste</span>
                                <span class="ml-auto text-xs text-neutral-400">5</span>
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
                                <span class="text-sm text-muted-foreground">28 techniciens</span>

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
                                        Technicien
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Spécialité
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
                                        Interventions
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
                                        <div class="text-sm font-medium text-neutral-900">{{ operator.firstName }} {{
                                            operator.lastName }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge variant="outline">{{ operator.specialty }}
                                        </Badge>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ operator.zone }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ operator.phone }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ operator.email }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ operator.interventionsCount }}</div>
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
        </div>

        <TablePagination :current-page="1" :total-pages="2" :total-items="28" :items-per-page="20"
            :position-classes="`bottom-0 ${showFilters ? 'left-80' : 'left-32'} right-0`"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />

        <!-- Dialog d'édition -->
        <Dialog v-model:open="isEditModalOpen">
            <DialogContent class="max-w-md">
                <DialogHeader>
                    <DialogTitle>{{ editingOperator?.id ? 'Modifier' : 'Ajouter' }} un technicien</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Prénom</label>
                            <Input v-model="editingOperator.firstName" class="mt-1" placeholder="Prénom" />
                        </div>
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Nom</label>
                            <Input v-model="editingOperator.lastName" class="mt-1" placeholder="Nom" />
                        </div>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Spécialité</label>
                        <Select v-model="editingOperator.specialty">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner une spécialité" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Électricité">Électricité</SelectItem>
                                <SelectItem value="Plomberie">Plomberie</SelectItem>
                                <SelectItem value="Chauffage">Chauffage</SelectItem>
                                <SelectItem value="Climatisation">Climatisation</SelectItem>
                                <SelectItem value="Généraliste">Généraliste</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Zone d'intervention</label>
                        <Select v-model="editingOperator.zone">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner une zone" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Paris">Paris</SelectItem>
                                <SelectItem value="Île-de-France">Île-de-France</SelectItem>
                                <SelectItem value="National">National</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Téléphone</label>
                        <Input v-model="editingOperator.phone" class="mt-1" placeholder="06 12 34 56 78" />
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Email</label>
                        <Input v-model="editingOperator.email" type="email" class="mt-1"
                            placeholder="email@trottr.com" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Annuler</Button>
                    <Button @click="saveOperator">{{ editingOperator?.id ? 'Modifier' : 'Ajouter' }}</Button>
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
    MoreVertical,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    RotateCcw,
    Search
} from 'lucide-vue-next'
import { ref } from 'vue'

const showFilters = ref(true)
const isEditModalOpen = ref(false)
const editingOperator = ref({
    id: null,
    firstName: '',
    lastName: '',
    specialty: '',
    zone: '',
    phone: '',
    email: '',
    interventionsCount: 0
})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const openCreateDialog = () => {
    editingOperator.value = {
        id: null,
        firstName: '',
        lastName: '',
        specialty: '',
        zone: '',
        phone: '',
        email: '',
        interventionsCount: 0
    }
    isEditModalOpen.value = true
}

const editOperator = (operator) => {
    editingOperator.value = { ...operator }
    isEditModalOpen.value = true
}

const cancelEdit = () => {
    editingOperator.value = {
        id: null,
        firstName: '',
        lastName: '',
        specialty: '',
        zone: '',
        phone: '',
        email: '',
        interventionsCount: 0
    }
    isEditModalOpen.value = false
}

const saveOperator = () => {
    if (editingOperator.value.id) {
        const index = operators.findIndex(op => op.id === editingOperator.value.id)
        if (index !== -1) {
            operators[index] = { ...editingOperator.value }
        }
    } else {
        const newId = Math.max(...operators.map(op => op.id)) + 1
        operators.push({
            ...editingOperator.value,
            id: newId
        })
    }
    cancelEdit()
}

const operators = [
    {
        id: 1,
        firstName: 'Pierre',
        lastName: 'Martin',
        specialty: 'Électricité',
        zone: 'Paris',
        phone: '06 12 34 56 78',
        email: 'pierre.martin@trottr.com',
        interventionsCount: 45
    },
    {
        id: 2,
        firstName: 'Marie',
        lastName: 'Dubois',
        specialty: 'Plomberie',
        zone: 'Île-de-France',
        phone: '06 98 76 54 32',
        email: 'marie.dubois@trottr.com',
        interventionsCount: 38
    },
    {
        id: 3,
        firstName: 'Jean',
        lastName: 'Dupont',
        specialty: 'Chauffage',
        zone: 'Paris',
        phone: '06 45 67 89 12',
        email: 'jean.dupont@trottr.com',
        interventionsCount: 52
    },
    {
        id: 4,
        firstName: 'Sophie',
        lastName: 'Leroy',
        specialty: 'Climatisation',
        zone: 'Île-de-France',
        phone: '06 23 45 67 89',
        email: 'sophie.leroy@trottr.com',
        interventionsCount: 29
    },
    {
        id: 5,
        firstName: 'Thomas',
        lastName: 'Bernard',
        specialty: 'Généraliste',
        zone: 'National',
        phone: '06 78 90 12 34',
        email: 'thomas.bernard@trottr.com',
        interventionsCount: 67
    },
    {
        id: 6,
        firstName: 'Émilie',
        lastName: 'Moreau',
        specialty: 'Électricité',
        zone: 'Paris',
        phone: '06 56 78 90 12',
        email: 'emilie.moreau@trottr.com',
        interventionsCount: 41
    },
    {
        id: 7,
        firstName: 'Nicolas',
        lastName: 'Rousseau',
        specialty: 'Plomberie',
        zone: 'Île-de-France',
        phone: '06 34 56 78 90',
        email: 'nicolas.rousseau@trottr.com',
        interventionsCount: 33
    },
    {
        id: 8,
        firstName: 'Lucie',
        lastName: 'Simon',
        specialty: 'Chauffage',
        zone: 'Paris',
        phone: '06 12 78 90 34',
        email: 'lucie.simon@trottr.com',
        interventionsCount: 0
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>