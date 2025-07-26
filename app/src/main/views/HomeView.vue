<template>
    <div class="h-full flex flex-col">
        <!-- Bandeau supérieur avec actions et KPIs -->
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="showKpis ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Interventions</h1>
                    <p class="text-neutral-600">Gestion des interventions terrain</p>
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
                        Nouvelle intervention
                    </Button>
                </div>
            </div>

            <!-- KPIs compacts -->
            <div v-show="showKpis" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Calendar class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Aujourd'hui</p>
                        <p class="text-lg font-semibold text-neutral-900">12</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <AlertTriangle class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">En retard</p>
                        <p class="text-lg font-semibold text-neutral-900">3</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Clock class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">En cours</p>
                        <p class="text-lg font-semibold text-neutral-900">8</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <CheckCircle class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Terminées</p>
                        <p class="text-lg font-semibold text-neutral-900">27</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contenu principal avec sidebar -->
        <div class="flex-1 flex overflow-hidden">
            <div class="w-64 bg-neutral-50 border-r p-4 overflow-y-auto">
                <h3 class="font-semibold text-neutral-900 mb-4">Filtres</h3>

                <!-- Statut -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Statut</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Planifiée</span>
                            <span class="ml-auto text-xs text-neutral-400">15</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">En cours</span>
                            <span class="ml-auto text-xs text-neutral-400">8</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">En retard</span>
                            <span class="ml-auto text-xs text-neutral-400">3</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox />
                            <span class="ml-2 text-sm text-neutral-600">Terminée</span>
                            <span class="ml-auto text-xs text-neutral-400">27</span>
                        </label>
                    </div>
                </div>

                <!-- Priorité -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Priorité</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Urgente</span>
                            <span class="ml-auto text-xs text-neutral-400">5</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Élevée</span>
                            <span class="ml-auto text-xs text-neutral-400">12</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Normale</span>
                            <span class="ml-auto text-xs text-neutral-400">26</span>
                        </label>
                    </div>
                </div>

                <!-- Type d'intervention -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Type</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Maintenance</span>
                            <span class="ml-auto text-xs text-neutral-400">18</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Dépannage</span>
                            <span class="ml-auto text-xs text-neutral-400">15</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Installation</span>
                            <span class="ml-auto text-xs text-neutral-400">10</span>
                        </label>
                    </div>
                </div>

                <!-- Opérateur -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Opérateur</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Jean Martin</span>
                            <span class="ml-auto text-xs text-neutral-400">8</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Sophie Dubois</span>
                            <span class="ml-auto text-xs text-neutral-400">6</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox />
                            <span class="ml-2 text-sm text-neutral-600">Pierre Leclerc</span>
                            <span class="ml-auto text-xs text-neutral-400">4</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox />
                            <span class="ml-2 text-sm text-neutral-600">Marie Rousseau</span>
                            <span class="ml-auto text-xs text-neutral-400">5</span>
                        </label>
                    </div>
                </div>

                <Button variant="outline" size="sm" class="w-full">
                    <RotateCcw class="h-4 w-4 mr-2" />
                    Réinitialiser
                </Button>
            </div>

            <!-- Tableau des interventions -->
            <div class="flex-1 overflow-y-auto">
                <div class="">
                    <div class="px-6 py-4 border-b">
                        <div class="flex items-center justify-between">
                            <h3 class="text-lg font-semibold text-neutral-900">Liste des interventions</h3>
                            <div class="flex items-center space-x-3">
                                <span class="text-sm text-muted-foreground">26 interventions</span>
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
                                        Réf.
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Intervention
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Client
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Opérateur
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Date/Heure
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Statut
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Priorité
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="intervention in interventions" :key="intervention.id"
                                    :class="['hover:bg-neutral-50', intervention.isClickable ? 'cursor-pointer' : '']"
                                    @click="intervention.isClickable ? $router.push(`/job/${intervention.ref}`) : null">
                                    <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                        <div class="text-sm font-mono font-medium text-neutral-900">{{ intervention.ref
                                        }}</div>
                                        <div class="text-xs text-neutral-500">{{ intervention.date }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                        <div class="text-sm font-medium text-neutral-900">{{ intervention.title }}</div>
                                        <div class="text-xs text-neutral-500">{{ intervention.category }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                        <div class="text-sm text-neutral-900 font-medium">{{ intervention.client.name }}
                                        </div>
                                        <div class="text-xs text-neutral-500 flex items-center">
                                            {{ intervention.client.address }}
                                            <Button v-if="intervention.client.showMap" variant="ghost" size="sm"
                                                class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                        <div class="flex items-center gap-1">
                                            <div class="w-4 h-4 bg-neutral-300 rounded-full flex items-center justify-center font-medium"
                                                style="font-size:9px">
                                                {{ intervention.operator.initials }}
                                            </div>
                                            <div class="text-sm font-medium text-neutral-900">{{
                                                intervention.operator.name }}</div>
                                        </div>
                                        <div class="text-xs text-neutral-500">{{ intervention.operator.role }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap text-sm text-neutral-900 space-y-1">
                                        <div>{{ intervention.schedule.time }}</div>
                                        <div :class="['text-xs', intervention.schedule.statusColor]">{{
                                            intervention.schedule.status }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <span :class="[
                                            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                            intervention.status.bgColor,
                                            intervention.status.textColor
                                        ]">
                                            {{ intervention.status.label }}
                                        </span>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <span :class="[
                                            'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                            intervention.priority.bgColor,
                                            intervention.priority.textColor
                                        ]">
                                            {{ intervention.priority.label }}
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pagination fixe -->
        <TablePagination :current-page="1" :total-pages="3" :total-items="26" :items-per-page="10"
            position-classes="bottom-0 left-80 right-0" @page-change="handlePageChange"
            @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { Switch } from '@/common/components/ui/switch'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    AlertTriangle,
    Calendar,
    CheckCircle,
    ChevronDown,
    Clock,
    Columns,
    Download,
    MapPin,
    MoreVertical,
    Plus,
    RotateCcw
} from 'lucide-vue-next'
import { ref } from 'vue'

const showKpis = ref(false)

const interventions = [
    {
        id: 1,
        ref: 'TR42K8',
        date: '26.07.2025',
        title: 'Panne électrique',
        category: 'Dépannage simple',
        client: {
            name: 'SARL Martin',
            address: '15 rue de la République',
            showMap: false
        },
        operator: {
            name: 'Jean Martin',
            role: 'Technicien',
            initials: 'J'
        },
        schedule: {
            time: 'Aujourd\'hui 14:00',
            status: 'En retard de 30min',
            statusColor: 'text-red-600'
        },
        status: {
            label: 'En retard',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        },
        priority: {
            label: 'Urgente',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        },
        isClickable: true
    },
    {
        id: 2,
        ref: 'MP7X3L',
        date: '27.07.2025',
        title: 'Maintenance préventive',
        category: 'Contrôle mensuel',
        client: {
            name: 'Hotel Plaza',
            address: '42 av. Champs-Élysées',
            showMap: true
        },
        operator: {
            name: 'Sophie Dubois',
            role: 'Technicienne',
            initials: 'S'
        },
        schedule: {
            time: 'Aujourd\'hui 16:30',
            status: 'Dans 2h',
            statusColor: 'text-neutral-600'
        },
        status: {
            label: 'Planifiée',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        priority: {
            label: 'Élevée',
            bgColor: 'bg-orange-100',
            textColor: 'text-orange-800'
        },
        isClickable: false
    },
    {
        id: 3,
        ref: 'IN9R4V',
        date: '28.07.2025',
        title: 'Installation équipement',
        category: 'Nouvel équipement',
        client: {
            name: 'Café Central',
            address: '8 place de la Bastille',
            showMap: true
        },
        operator: {
            name: 'Pierre Leclerc',
            role: 'Installateur',
            initials: 'P'
        },
        schedule: {
            time: 'Demain 09:00',
            status: 'Durée: 2h',
            statusColor: 'text-neutral-500'
        },
        status: {
            label: 'Planifiée',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        priority: {
            label: 'Normale',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        isClickable: true
    },
    {
        id: 4,
        ref: 'RP8M2N',
        date: '26.07.2025',
        title: 'Réparation urgente',
        category: 'Système défaillant',
        client: {
            name: 'Boulangerie Paul',
            address: '23 rue de Rivoli',
            showMap: true
        },
        operator: {
            name: 'Marie Rousseau',
            role: 'Technicienne',
            initials: 'M'
        },
        schedule: {
            time: 'Aujourd\'hui 13:15',
            status: 'En cours',
            statusColor: 'text-green-600'
        },
        status: {
            label: 'En cours',
            bgColor: 'bg-orange-100',
            textColor: 'text-orange-800'
        },
        priority: {
            label: 'Urgente',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        },
        isClickable: true
    },
    {
        id: 5,
        ref: 'CT5B7Q',
        date: '30.07.2025',
        title: 'Contrôle technique',
        category: 'Vérification annuelle',
        client: {
            name: 'Garage Moderne',
            address: '67 boulevard Voltaire',
            showMap: true
        },
        operator: {
            name: 'Antoine Bernard',
            role: 'Contrôleur',
            initials: 'A'
        },
        schedule: {
            time: 'Lundi 10:00',
            status: 'Dans 3 jours',
            statusColor: 'text-neutral-500'
        },
        status: {
            label: 'Planifiée',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        priority: {
            label: 'Normale',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        isClickable: true
    },
    {
        id: 6,
        ref: 'DP3X9K',
        date: '31.07.2025',
        title: 'Diagnostic complet',
        category: 'Analyse système',
        client: {
            name: 'Clinique Pasteur',
            address: '156 rue de Vaugirard',
            showMap: true
        },
        operator: {
            name: 'François Lambert',
            role: 'Diagnostiqueur',
            initials: 'F'
        },
        schedule: {
            time: 'Mardi 08:30',
            status: 'Dans 4 jours',
            statusColor: 'text-neutral-500'
        },
        status: {
            label: 'Planifiée',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        priority: {
            label: 'Élevée',
            bgColor: 'bg-orange-100',
            textColor: 'text-orange-800'
        },
        isClickable: true
    },
    {
        id: 7,
        ref: 'GZ4R8T',
        date: '01.08.2025',
        title: 'Contrôle gaz',
        category: 'Audit Gaz',
        client: {
            name: 'Restaurant Le Petit Zinc',
            address: '32 rue Saint-Antoine',
            showMap: true
        },
        operator: {
            name: 'Sylvie Moreau',
            role: 'Gazière',
            initials: 'S'
        },
        schedule: {
            time: 'Mercredi 14:00',
            status: 'Dans 5 jours',
            statusColor: 'text-neutral-500'
        },
        status: {
            label: 'Planifiée',
            bgColor: 'bg-neutral-100',
            textColor: 'text-neutral-800'
        },
        priority: {
            label: 'Urgente',
            bgColor: 'bg-red-100',
            textColor: 'text-red-800'
        },
        isClickable: true
    },
    {
        id: 8,
        ref: 'EL9K2M',
        date: '02.08.2025',
        title: 'Dépannage électrique',
        category: 'Dépannage urgent',
        client: {
            name: 'Pharmacie de la Paix',
            address: '78 rue de la Paix',
            showMap: false
        },
        operator: {
            name: 'Thomas Durand',
            role: 'Électricien',
            initials: 'T'
        },
        schedule: {
            time: 'Jeudi 09:30',
            status: 'Dans 6 jours',
            statusColor: 'text-neutral-500'
        },
        status: {
            label: 'À assigner',
            bgColor: 'bg-yellow-100',
            textColor: 'text-yellow-800'
        },
        priority: {
            label: 'Élevée',
            bgColor: 'bg-orange-100',
            textColor: 'text-orange-800'
        },
        isClickable: true
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>