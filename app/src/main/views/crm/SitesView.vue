<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="showKpis ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Sites d'intervention</h1>
                    <p class="text-neutral-600">Gestion des sites d'intervention</p>
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
                        Nouveau site
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
                        <p class="text-lg font-semibold text-neutral-900">232</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Building class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Résidentiels</p>
                        <p class="text-lg font-semibold text-neutral-900">156</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Building2 class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Tertiaires</p>
                        <p class="text-lg font-semibold text-neutral-900">76</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <FileText class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Avec contrat</p>
                        <p class="text-lg font-semibold text-neutral-900">89</p>
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Type de bâtiment</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Résidence collective</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Maison individuelle</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Bâtiment tertiaire</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Local commercial</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Pays</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">France</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Belgique</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Suisse</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Contrat</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Avec contrat</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox class="mr-2" />
                                <span class="text-sm">Sans contrat</span>
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
                                <span class="text-sm text-muted-foreground">232 sites</span>

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
                                        Rue
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Code postal
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Ville
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Rattaché à
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Type bâtiment
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Lots
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Dernière intervention
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Contrat
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="site in sites" :key="site.id" class="hover:bg-neutral-50 cursor-pointer"
                                    @click="$router.push(`/site/${site.id}`)">
                                    <td class="px-3 py-2 whitespace-nowrap" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium text-neutral-900">{{ site.label }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.street }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.zipCode }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.city }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.attachedTo || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.buildingType }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.lotCount || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ site.lastIntervention || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge v-if="site.contract" variant="outline">{{ site.contract }}</Badge>
                                        <span v-else class="text-sm text-neutral-300">-</span>
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

        <TablePagination :current-page="1" :total-pages="12" :total-items="232" :items-per-page="20"
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
import Badge from '../../../common/components/ui/badge/Badge.vue'

const showKpis = ref(false)
const showFilters = ref(true)

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}



const sites = [
    {
        id: 1,
        label: 'Résidence Les Jardins',
        street: '15 rue des Lilas',
        zipCode: '75015',
        city: 'Paris',
        country: 'France',
        attachedTo: 'SARL Immobilier Plus',
        buildingType: 'Résidence collective',
        lotCount: 45,
        lastIntervention: '15/12/2024',
        contract: 'CTR-2024-001'
    },
    {
        id: 2,
        label: 'Villa Dupont',
        street: '8 avenue de la Paix',
        zipCode: '69003',
        city: 'Lyon',
        country: 'France',
        attachedTo: 'M. Dupont Pierre',
        buildingType: 'Maison individuelle',
        lotCount: null,
        lastIntervention: null,
        contract: null
    },
    {
        id: 3,
        label: 'Centre Commercial Bellecour',
        street: '23 place Bellecour',
        zipCode: '69002',
        city: 'Lyon',
        country: 'France',
        attachedTo: 'SCI Bellecour',
        buildingType: 'Local commercial',
        lotCount: 12,
        lastIntervention: '08/01/2025',
        contract: 'CTR-2023-045'
    },
    {
        id: 4,
        label: 'Immeuble Saint-Michel',
        street: '42 boulevard Saint-Michel',
        zipCode: '75006',
        city: 'Paris',
        country: 'France',
        attachedTo: 'Syndic Moderne',
        buildingType: 'Résidence collective',
        lotCount: 28,
        lastIntervention: null,
        contract: null
    },
    {
        id: 5,
        label: 'Tour de bureaux Défense',
        street: '1 esplanade du Général de Gaulle',
        zipCode: '92400',
        city: 'Courbevoie',
        country: 'France',
        attachedTo: 'Office Management SA',
        buildingType: 'Bâtiment tertiaire',
        lotCount: 150,
        lastIntervention: '22/12/2024',
        contract: 'CTR-2024-012'
    },
    {
        id: 6,
        label: 'Maison Martin',
        street: '67 rue de la République',
        zipCode: '13001',
        city: 'Marseille',
        country: 'France',
        attachedTo: 'Mme Martin Claire',
        buildingType: 'Maison individuelle',
        lotCount: null,
        lastIntervention: null,
        contract: null
    },
    {
        id: 7,
        label: 'Résidence Atlantique',
        street: '156 avenue de l\'Atlantique',
        zipCode: '44000',
        city: 'Nantes',
        country: 'France',
        attachedTo: 'Gestimmo Nantes',
        buildingType: 'Résidence collective',
        lotCount: 82,
        lastIntervention: '03/01/2025',
        contract: 'CTR-2024-089'
    },
    {
        id: 8,
        label: 'Bureaux Tech Center',
        street: '9 rue de l\'Innovation',
        zipCode: '31000',
        city: 'Toulouse',
        country: 'France',
        attachedTo: 'Tech Properties',
        buildingType: 'Bâtiment tertiaire',
        lotCount: 25,
        lastIntervention: null,
        contract: null
    },
    {
        id: 9,
        label: 'Villa Rochefort',
        street: '34 chemin des Pins',
        zipCode: '06400',
        city: 'Cannes',
        country: 'France',
        attachedTo: 'M. Rochefort Jean',
        buildingType: 'Maison individuelle',
        lotCount: null,
        lastIntervention: '28/11/2024',
        contract: 'CTR-2024-156'
    },
    {
        id: 10,
        label: 'Centre d\'affaires Lille',
        street: '88 rue Nationale',
        zipCode: '59000',
        city: 'Lille',
        country: 'France',
        attachedTo: 'Business Center Lille',
        buildingType: 'Bâtiment tertiaire',
        lotCount: 65,
        lastIntervention: null,
        contract: null
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>