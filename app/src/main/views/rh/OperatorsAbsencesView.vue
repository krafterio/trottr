<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="showKpis ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Absences / Congés</h1>
                    <p class="text-neutral-600">Gestion des absences des techniciens</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2 bg-accent rounded-md p-2 h-9">
                        <p class="text-sm text-neutral-600">Afficher KPIs</p>
                        <Switch v-model="showKpis" />
                    </div>
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button @click="openCreateDialog">
                        <Plus class="h-4 w-4" />
                        Nouvelle absence
                    </Button>
                </div>
            </div>

            <div v-show="showKpis" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <CalendarIcon class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Total</p>
                        <p class="text-lg font-semibold text-neutral-900">42</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Heart class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Vacances</p>
                        <p class="text-lg font-semibold text-neutral-900">18</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Stethoscope class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Maladie</p>
                        <p class="text-lg font-semibold text-neutral-900">12</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <GraduationCap class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Formation</p>
                        <p class="text-lg font-semibold text-neutral-900">8</p>
                    </div>
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
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Vacances</span>
                                <span class="ml-auto text-xs text-neutral-400">18</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Maladie</span>
                                <span class="ml-auto text-xs text-neutral-400">12</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Formation</span>
                                <span class="ml-auto text-xs text-neutral-400">8</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Autre</span>
                                <span class="ml-auto text-xs text-neutral-400">4</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Technicien</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Pierre Martin</span>
                                <span class="ml-auto text-xs text-neutral-400">5</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Marie Dubois</span>
                                <span class="ml-auto text-xs text-neutral-400">4</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Jean Dupont</span>
                                <span class="ml-auto text-xs text-neutral-400">6</span>
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
                                <span class="text-sm text-muted-foreground">42 absences</span>

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
                                        Type
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Date début
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Date fin
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Durée
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Motif
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Actions
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="absence in absences" :key="absence.id"
                                    class="hover:bg-neutral-50 cursor-pointer" @click.stop="editAbsence(absence)">
                                    <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium text-neutral-900">{{ absence.technicianName }}
                                        </div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge :class="getTypeColor(absence.type)">{{ absence.type }}</Badge>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ formatDate(absence.startDate) }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ formatDate(absence.endDate) }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ absence.duration }} jours</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ absence.reason || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Button variant="ghost" size="sm" @click.stop="editAbsence(absence)">
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

        <TablePagination :current-page="1" :total-pages="3" :total-items="42" :items-per-page="20"
            :position-classes="`bottom-0 ${showFilters ? 'left-80' : 'left-32'} right-0`"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />

        <!-- Dialog d'édition -->
        <Dialog v-model:open="isEditModalOpen">
            <DialogContent class="max-w-md">
                <DialogHeader>
                    <DialogTitle>{{ editingAbsence?.id ? 'Modifier' : 'Ajouter' }} une absence</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Technicien</label>
                        <Select v-model="editingAbsence.technicianId">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner un technicien" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="tech in technicians" :key="tech.id" :value="tech.id">
                                    {{ tech.firstName }} {{ tech.lastName }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Type d'absence</label>
                        <Select v-model="editingAbsence.type">
                            <SelectTrigger class="mt-1 w-full">
                                <SelectValue placeholder="Sélectionner un type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Vacances">Vacances</SelectItem>
                                <SelectItem value="Maladie">Maladie</SelectItem>
                                <SelectItem value="Formation">Formation</SelectItem>
                                <SelectItem value="Autre">Autre</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Date de début</label>
                            <Popover>
                                <PopoverTrigger as-child>
                                    <Button variant="outline" :class="cn(
                                        'w-full justify-start text-left font-normal mt-1',
                                        !startDateValue && 'text-muted-foreground',
                                    )">
                                        <CalendarIcon class="mr-2 h-4 w-4" />
                                        {{ startDateValue ? df.format(startDateValue.toDate(getLocalTimeZone())) :
                                            "Sélectionner une date" }}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent class="w-auto p-0">
                                    <Calendar v-model="startDateValue" initial-focus
                                        @update:model-value="updateStartDate" />
                                </PopoverContent>
                            </Popover>
                        </div>
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Date de fin</label>
                            <Popover>
                                <PopoverTrigger as-child>
                                    <Button variant="outline" :class="cn(
                                        'w-full justify-start text-left font-normal mt-1',
                                        !endDateValue && 'text-muted-foreground',
                                    )">
                                        <CalendarIcon class="mr-2 h-4 w-4" />
                                        {{ endDateValue ? df.format(endDateValue.toDate(getLocalTimeZone())) :
                                            "Sélectionner une date" }}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent class="w-auto p-0">
                                    <Calendar v-model="endDateValue" initial-focus
                                        @update:model-value="updateEndDate" />
                                </PopoverContent>
                            </Popover>
                        </div>
                    </div>
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Motif (optionnel)</label>
                        <Textarea v-model="editingAbsence.reason" class="mt-1" placeholder="Motif de l'absence..." />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Annuler</Button>
                    <Button @click="saveAbsence">{{ editingAbsence?.id ? 'Modifier' : 'Ajouter' }}</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Calendar } from '@/common/components/ui/calendar'
import { Checkbox } from '@/common/components/ui/checkbox'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import Input from '@/common/components/ui/input/Input.vue'
import { Popover, PopoverContent, PopoverTrigger } from '@/common/components/ui/popover'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Switch } from '@/common/components/ui/switch'
import { Textarea } from '@/common/components/ui/textarea'
import { cn } from '@/common/lib/utils'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    CalendarDate,
    DateFormatter,
    getLocalTimeZone,
} from '@internationalized/date'
import {
    Calendar as CalendarIcon,
    ChevronDown,
    Columns,
    Download,
    Edit,
    GraduationCap,
    Heart,
    MoreVertical,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    RotateCcw,
    Search,
    Stethoscope
} from 'lucide-vue-next'
import { ref } from 'vue'

const showKpis = ref(false)
const showFilters = ref(true)
const isEditModalOpen = ref(false)

// DatePicker
const df = new DateFormatter('fr-FR', {
    dateStyle: 'long',
})

const startDateValue = ref()
const endDateValue = ref()

const editingAbsence = ref({
    id: null,
    technicianId: '',
    type: '',
    startDate: '',
    endDate: '',
    reason: ''
})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const updateStartDate = (date) => {
    startDateValue.value = date
    editingAbsence.value.startDate = date ? date.toString() : ''
}

const updateEndDate = (date) => {
    endDateValue.value = date
    editingAbsence.value.endDate = date ? date.toString() : ''
}

const openCreateDialog = () => {
    editingAbsence.value = {
        id: null,
        technicianId: '',
        type: '',
        startDate: '',
        endDate: '',
        reason: ''
    }
    startDateValue.value = undefined
    endDateValue.value = undefined
    isEditModalOpen.value = true
}

const editAbsence = (absence) => {
    editingAbsence.value = { ...absence }
    // Convertir les dates string en DateValue si nécessaire
    startDateValue.value = absence.startDate ? parseDate(absence.startDate) : undefined
    endDateValue.value = absence.endDate ? parseDate(absence.endDate) : undefined
    isEditModalOpen.value = true
}

const parseDate = (dateStr) => {
    if (!dateStr) return undefined
    const [year, month, day] = dateStr.split('-')
    return new CalendarDate(parseInt(year), parseInt(month), parseInt(day))
}

const cancelEdit = () => {
    editingAbsence.value = {
        id: null,
        technicianId: '',
        type: '',
        startDate: '',
        endDate: '',
        reason: ''
    }
    startDateValue.value = undefined
    endDateValue.value = undefined
    isEditModalOpen.value = false
}

const saveAbsence = () => {
    if (editingAbsence.value.id) {
        const index = absences.findIndex(abs => abs.id === editingAbsence.value.id)
        if (index !== -1) {
            const technicianName = technicians.find(t => t.id === editingAbsence.value.technicianId)?.firstName + ' ' +
                technicians.find(t => t.id === editingAbsence.value.technicianId)?.lastName
            const duration = calculateDuration(editingAbsence.value.startDate, editingAbsence.value.endDate)
            absences[index] = {
                ...editingAbsence.value,
                technicianName,
                duration
            }
        }
    } else {
        const newId = Math.max(...absences.map(abs => abs.id)) + 1
        const technicianName = technicians.find(t => t.id === editingAbsence.value.technicianId)?.firstName + ' ' +
            technicians.find(t => t.id === editingAbsence.value.technicianId)?.lastName
        const duration = calculateDuration(editingAbsence.value.startDate, editingAbsence.value.endDate)
        absences.push({
            ...editingAbsence.value,
            id: newId,
            technicianName,
            duration
        })
    }
    cancelEdit()
}

const calculateDuration = (startDate, endDate) => {
    if (!startDate || !endDate) return 0
    const start = new Date(startDate)
    const end = new Date(endDate)
    const diffTime = Math.abs(end - start)
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
}

const formatDate = (dateStr) => {
    if (!dateStr) return '-'
    const date = new Date(dateStr)
    return date.toLocaleDateString('fr-FR')
}

const getTypeColor = (type) => {
    switch (type) {
        case 'Vacances':
            return 'bg-blue-100 text-blue-800'
        case 'Maladie':
            return 'bg-red-100 text-red-800'
        case 'Formation':
            return 'bg-green-100 text-green-800'
        case 'Autre':
            return 'bg-neutral-100 text-neutral-800'
        default:
            return 'bg-neutral-100 text-neutral-800'
    }
}

const technicians = [
    { id: 1, firstName: 'Pierre', lastName: 'Martin' },
    { id: 2, firstName: 'Marie', lastName: 'Dubois' },
    { id: 3, firstName: 'Jean', lastName: 'Dupont' },
    { id: 4, firstName: 'Sophie', lastName: 'Leroy' },
    { id: 5, firstName: 'Thomas', lastName: 'Bernard' },
    { id: 6, firstName: 'Émilie', lastName: 'Moreau' },
    { id: 7, firstName: 'Nicolas', lastName: 'Rousseau' },
    { id: 8, firstName: 'Lucie', lastName: 'Simon' }
]

const absences = [
    {
        id: 1,
        technicianId: 1,
        technicianName: 'Pierre Martin',
        type: 'Vacances',
        startDate: '2025-02-15',
        endDate: '2025-02-28',
        duration: 14,
        reason: 'Congés annuels'
    },
    {
        id: 2,
        technicianId: 2,
        technicianName: 'Marie Dubois',
        type: 'Maladie',
        startDate: '2025-01-20',
        endDate: '2025-01-22',
        duration: 3,
        reason: 'Grippe'
    },
    {
        id: 3,
        technicianId: 3,
        technicianName: 'Jean Dupont',
        type: 'Formation',
        startDate: '2025-01-25',
        endDate: '2025-01-26',
        duration: 2,
        reason: 'Formation habilitation électrique'
    },
    {
        id: 4,
        technicianId: 4,
        technicianName: 'Sophie Leroy',
        type: 'Vacances',
        startDate: '2025-03-01',
        endDate: '2025-03-07',
        duration: 7,
        reason: 'Vacances scolaires'
    },
    {
        id: 5,
        technicianId: 1,
        technicianName: 'Pierre Martin',
        type: 'Maladie',
        startDate: '2025-01-10',
        endDate: '2025-01-10',
        duration: 1,
        reason: 'Mal de dos'
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>