<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="showKpis ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Entreprises</h1>
                    <p class="text-neutral-600">Gestion des entreprises clientes</p>
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
                        Nouvelle entreprise
                    </Button>
                </div>
            </div>

            <div v-show="showKpis" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Building class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Total</p>
                        <p class="text-lg font-semibold text-neutral-900">147</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <CheckCircle class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Actives</p>
                        <p class="text-lg font-semibold text-neutral-900">132</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Clock class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">En attente</p>
                        <p class="text-lg font-semibold text-neutral-900">12</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <AlertTriangle class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Suspendues</p>
                        <p class="text-lg font-semibold text-neutral-900">3</p>
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
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Statut</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Active</span>
                                <span class="ml-auto text-xs text-neutral-400">132</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">En attente</span>
                                <span class="ml-auto text-xs text-neutral-400">12</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox />
                                <span class="ml-2 text-sm text-neutral-600">Suspendue</span>
                                <span class="ml-auto text-xs text-neutral-400">3</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Type</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Client final</span>
                                <span class="ml-auto text-xs text-neutral-400">89</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Régie / gestionnaire</span>
                                <span class="ml-auto text-xs text-neutral-400">23</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Donneur d'ordre</span>
                                <span class="ml-auto text-xs text-neutral-400">18</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Sous-traitant</span>
                                <span class="ml-auto text-xs text-neutral-400">12</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Fournisseur</span>
                                <span class="ml-auto text-xs text-neutral-400">5</span>
                            </label>
                        </div>
                    </div>

                    <div class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">Contrat</h4>
                        <div class="space-y-2">
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Actif</span>
                                <span class="ml-auto text-xs text-neutral-400">98</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Expiré</span>
                                <span class="ml-auto text-xs text-neutral-400">31</span>
                            </label>
                            <label class="flex items-center">
                                <Checkbox checked />
                                <span class="ml-2 text-sm text-neutral-600">Sans contrat</span>
                                <span class="ml-auto text-xs text-neutral-400">18</span>
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
                                <span class="text-sm text-muted-foreground">147 entreprises</span>

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
                                        Entreprise
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Type
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Nb adresses
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Adresse
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Téléphone
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Contrat
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Statut
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="company in companies" :key="company.id"
                                    class="hover:bg-neutral-50 cursor-pointer"
                                    @click="$router.push(`/company/${company.id}`)">
                                    <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium text-neutral-900">{{ company.name }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <Badge variant="outline">{{ company.type }}
                                        </Badge>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ company.addressCount }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ company.address }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ company.phone }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <span :class="[
                                            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                            company.contract.bgColor,
                                            company.contract.textColor
                                        ]">
                                            {{ company.contract.label }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <span :class="[
                                            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                            company.status.bgColor,
                                            company.status.textColor
                                        ]">
                                            {{ company.status.label }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <TablePagination :current-page="1" :total-pages="8" :total-items="147" :items-per-page="20"
            :position-classes="`bottom-0 ${showFilters ? 'left-80' : 'left-32'} right-0`"
            @page-change="handlePageChange" @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import Input from '@/common/components/ui/input/Input.vue'
import { Switch } from '@/common/components/ui/switch'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    AlertTriangle,
    Building,
    CheckCircle,
    ChevronDown,
    Clock,
    Columns,
    Download,
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

const companies = [
    {
        id: 1,
        name: 'SARL Martin',
        type: 'Client final',
        addressCount: 3,
        address: '15 rue de la République, Paris',
        phone: '01 42 33 44 55',
        contract: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 2,
        name: 'Hotel Plaza',
        type: 'Client final',
        addressCount: 1,
        address: '42 av. Champs-Élysées, Paris',
        phone: '01 56 78 90 12',
        contract: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 3,
        name: 'Café Central',
        type: 'Client final',
        addressCount: 2,
        address: '8 place de la Bastille, Paris',
        phone: '01 47 88 92 34',
        contract: {
            label: 'Expiré',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 4,
        name: 'Boulangerie Paul',
        type: 'Donneur d\'ordre',
        addressCount: 5,
        address: '23 rue de Rivoli, Paris',
        phone: '01 53 67 89 01',
        contract: {
            label: 'Sans contrat',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        status: {
            label: 'En attente',
            bgColor: 'bg-yellow-100',
            textColor: 'text-yellow-800'
        }
    },
    {
        id: 5,
        name: 'Garage Moderne',
        type: 'Client final',
        addressCount: 1,
        address: '67 boulevard Voltaire, Paris',
        phone: '01 48 95 73 26',
        contract: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 6,
        name: 'Clinique Pasteur',
        type: 'Régie / gestionnaire',
        addressCount: 8,
        address: '156 rue de Vaugirard, Paris',
        phone: '01 44 82 67 39',
        contract: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 7,
        name: 'Restaurant Le Petit Zinc',
        type: 'Client final',
        addressCount: 1,
        address: '32 rue Saint-Antoine, Paris',
        phone: '01 49 73 84 52',
        contract: {
            label: 'Expiré',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        },
        status: {
            label: 'Suspendue',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        }
    },
    {
        id: 8,
        name: 'Pharmacie de la Paix',
        type: 'Sous-traitant',
        addressCount: 3,
        address: '78 rue de la Paix, Paris',
        phone: '01 56 91 42 78',
        contract: {
            label: 'Sans contrat',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        status: {
            label: 'En attente',
            bgColor: 'bg-yellow-100',
            textColor: 'text-yellow-800'
        }
    },
    {
        id: 9,
        name: 'Bureau Études Technique',
        type: 'Fournisseur',
        addressCount: 2,
        address: '45 rue du Faubourg Saint-Antoine, Paris',
        phone: '01 43 87 65 21',
        contract: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 10,
        name: 'Société Générale du Bâtiment',
        type: 'Donneur d\'ordre',
        addressCount: 12,
        address: '129 avenue de la République, Paris',
        phone: '01 48 52 73 94',
        contract: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        status: {
            label: 'Active',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>