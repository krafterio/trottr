<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="showKpis ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Lots</h1>
                    <p class="text-neutral-600">Gestion des lots</p>
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
                    <Button>
                        <Plus class="h-4 w-4" />
                        Nouveau lot
                    </Button>
                </div>
            </div>

            <div v-show="showKpis" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <MapPin class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Total</p>
                        <p class="text-lg font-semibold text-neutral-900">127</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Building class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Appartements</p>
                        <p class="text-lg font-semibold text-neutral-900">89</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Building2 class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Locaux commerciaux</p>
                        <p class="text-lg font-semibold text-neutral-900">23</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <FileText class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Caves/Parkings</p>
                        <p class="text-lg font-semibold text-neutral-900">15</p>
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Type de lot</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Appartement</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Local commercial</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Cave</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Parking</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Site rattaché</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Résidence Les Jardins</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Centre Commercial Bellecour</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Immeuble Saint-Michel</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Contacts</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Avec contacts</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Sans contacts</span>
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
                                <span class="text-sm text-muted-foreground">127 lots</span>

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
                                        Type
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Description
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Surface
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Site rattaché
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Contacts
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Équipements
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Dernière intervention
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="lot in lots" :key="lot.id" class="hover:bg-neutral-50 cursor-pointer"
                                    @click="$router.push(`/subsite/${lot.id}`)">
                                    <td class="px-3 py-2 whitespace-nowrap" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium font-mono text-neutral-900">{{ lot.number }}
                                        </div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.type }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.description }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.surface ? lot.surface + ' m²' : '-'
                                            }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.site }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.contactsCount || '0' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.equipmentsCount || '0' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ lot.lastIntervention || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                            <MoreVertical class="h-4 w-4" />
                                        </Button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <TablePagination :current-page="1" :total-pages="7" :total-items="127" :items-per-page="20"
            :position-classes="`bottom-0 ${showFilters ? 'left-80' : 'left-32'} right-0`"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { Input } from '@/common/components/ui/input'
import { Switch } from '@/common/components/ui/switch'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    Building,
    Building2,
    ChevronDown,
    Columns,
    Download,
    FileText,
    MapPin,
    MoreVertical,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    RotateCcw,
    Search
} from 'lucide-vue-next'
import { ref } from 'vue'

const showKpis = ref(false)
const showFilters = ref(true)

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const lots = [
    {
        id: 1,
        number: 'A101',
        type: 'Appartement',
        description: '3 pièces, 2ème étage',
        surface: 65,
        site: 'Résidence Les Jardins',
        contactsCount: 2,
        equipmentsCount: 3,
        lastIntervention: '15/12/2024'
    },
    {
        id: 2,
        number: 'A102',
        type: 'Appartement',
        description: '2 pièces, 2ème étage',
        surface: 45,
        site: 'Résidence Les Jardins',
        contactsCount: 1,
        equipmentsCount: 2,
        lastIntervention: null
    },
    {
        id: 3,
        number: 'B201',
        type: 'Appartement',
        description: '4 pièces, 1er étage',
        surface: 85,
        site: 'Résidence Les Jardins',
        contactsCount: 0,
        equipmentsCount: 4,
        lastIntervention: '08/01/2025'
    },
    {
        id: 4,
        number: 'CC01',
        type: 'Local commercial',
        description: 'Boutique rez-de-chaussée',
        surface: 120,
        site: 'Centre Commercial Bellecour',
        contactsCount: 3,
        equipmentsCount: 8,
        lastIntervention: '22/11/2024'
    },
    {
        id: 5,
        number: 'P15',
        type: 'Parking',
        description: 'Place de parking sous-sol',
        surface: null,
        site: 'Résidence Les Jardins',
        contactsCount: 1,
        equipmentsCount: 0,
        lastIntervention: null
    },
    {
        id: 6,
        number: 'C042',
        type: 'Cave',
        description: 'Cave individuelle niveau -1',
        surface: 8,
        site: 'Immeuble Saint-Michel',
        contactsCount: 1,
        equipmentsCount: 1,
        lastIntervention: null
    },
    {
        id: 7,
        number: 'B105',
        type: 'Bureau',
        description: 'Bureau 1er étage',
        surface: 95,
        site: 'Centre Commercial Bellecour',
        contactsCount: 2,
        equipmentsCount: 5,
        lastIntervention: '03/01/2025'
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>