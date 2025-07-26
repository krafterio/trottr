<template>
    <div class="h-full flex flex-col bg-gray-50">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Tableau de bord</h1>
                    <p class="text-neutral-600">Vue d'ensemble des interventions terrain</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <Calendar />
                        <Button variant="outline" class="justify-start text-left font-normal">
                            <span class="text-sm">{{ dateRange.from }} - {{ dateRange.to }}</span>
                        </Button>
                    </div>
                    <Button variant="outline">
                        <Shredder class="h-5 w-5" />
                        Générer PDF
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 p-6 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="bg-white rounded-lg border p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm text-gray-600">Interventions créées</p>
                            <p class="text-2xl font-bold text-gray-900">34</p>
                        </div>
                        <div class="w-10 h-10 bg-accent rounded-lg flex items-center justify-center">
                            <Plus class="h-5 w-5 text-primary" />
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg border p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm text-gray-600">Interventions terminées</p>
                            <p class="text-2xl font-bold text-gray-900">28</p>
                        </div>
                        <div class="w-10 h-10 bg-accent rounded-lg flex items-center justify-center">
                            <CheckCircle class="h-5 w-5 text-primary" />
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg border p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm text-gray-600">Interventions en retard</p>
                            <p class="text-2xl font-bold text-gray-900">3</p>
                        </div>
                        <div class="w-10 h-10 bg-accent rounded-lg flex items-center justify-center">
                            <AlertTriangle class="h-5 w-5 text-primary" />
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg border p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm text-gray-600">Pourcentage de réalisation</p>
                            <p class="text-2xl font-bold text-gray-900">82%</p>
                        </div>
                        <div class="w-10 h-10 bg-accent rounded-lg flex items-center justify-center">
                            <Target class="h-5 w-5 text-primary" />
                        </div>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6" style="height: 400px;">
                <div class="bg-white rounded-lg border p-6 overflow-auto">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-lg font-semibold text-gray-900">Évolution des interventions</h3>
                    </div>
                    <VisXYContainer :data="weeklyData" :height="300">
                        <VisLine :x="(d, i) => i" :y="[d => d.creees, d => d.faites]" />
                        <VisAxis type=" x" :tickFormat="(v) => weeklyData[v]?.semaine || ''" />
                        <VisAxis type="y" />
                    </VisXYContainer>
                </div>

                <div class="bg-white rounded-lg border p-6 overflow-auto">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-lg font-semibold text-gray-900">Répartition par technicien</h3>
                    </div>
                    <VisSingleContainer :data="technicianData" :height="250">
                        <VisTooltip :triggers="triggers" />
                        <VisDonut :value="d => d.count" :color="['#16190C', '#149770', '#A7E00A', '#BFEDB4']"
                            :arcWidth="50" />
                    </VisSingleContainer>
                </div>

                <div class="bg-white rounded-lg border p-6 overflow-auto">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-lg font-semibold text-gray-900">Répartition par type</h3>
                    </div>
                    <VisSingleContainer :data="typeData" :height="250">
                        <VisTooltip :triggers="triggers" />
                        <VisDonut :value="d => d.count" :color="['#16190C', '#149770', '#A7E00A', '#BFEDB4']"
                            :arcWidth="50" />
                    </VisSingleContainer>
                </div>
            </div>

            <div class="bg-white rounded-lg border">
                <div class="px-6 py-4 border-b">
                    <div class="flex items-center justify-between">
                        <h3 class="text-lg font-semibold text-neutral-900">Interventions de la période</h3>
                        <div class="flex items-center space-x-3">
                            <span class="text-sm text-muted-foreground">{{ interventions.length }} interventions</span>
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
                                    <div class="text-sm font-mono font-medium text-neutral-900">{{ intervention.ref }}
                                    </div>
                                    <div class="text-xs text-neutral-500">{{ intervention.date }}</div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                    <div class="text-sm font-medium text-neutral-900">{{ intervention.title }}</div>
                                    <div class="text-xs text-neutral-500">{{ intervention.category }}</div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                    <div class="text-sm font-medium text-neutral-900">{{ intervention.client.name }}
                                    </div>
                                    <div class="text-xs text-neutral-500">{{ intervention.client.address }}</div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap">
                                    <div class="flex items-center space-x-3">
                                        <div
                                            class="w-8 h-8 bg-neutral-200 rounded-full flex items-center justify-center">
                                            <span class="text-xs font-medium text-neutral-600">{{
                                                intervention.operator.initials }}</span>
                                        </div>
                                        <div class="space-y-1">
                                            <div class="text-sm font-medium text-neutral-900">{{
                                                intervention.operator.name }}</div>
                                            <div class="text-xs text-neutral-500">{{ intervention.operator.role }}</div>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-2 whitespace-nowrap space-y-1">
                                    <div class="text-sm font-medium text-neutral-900">{{ intervention.schedule.time }}
                                    </div>
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

                <div class="px-6 py-4 border-t bg-neutral-50">
                    <div class="flex items-center justify-between">
                        <p class="text-sm text-neutral-700">
                            Affichage de <span class="font-medium">1</span> à <span class="font-medium">{{
                                interventions.length }}</span> sur <span class="font-medium">{{ interventions.length
                                }}</span> résultats
                        </p>
                        <div class="flex items-center space-x-2">
                            <Button variant="outline" size="sm" disabled>
                                <ChevronLeft class="h-4 w-4" />
                                Précédent
                            </Button>
                            <Button variant="outline" size="sm" disabled>
                                Suivant
                                <ChevronRight class="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { Donut } from '@unovis/ts'
import { VisAxis, VisDonut, VisLine, VisSingleContainer, VisTooltip, VisXYContainer } from '@unovis/vue'
import {
    AlertTriangle,
    Calendar,
    CheckCircle,
    ChevronDown,
    ChevronLeft,
    ChevronRight,
    Columns,
    MoreVertical,
    Plus,
    Shredder,
    Target
} from 'lucide-vue-next'
import { ref } from 'vue'

const dateRange = ref({
    from: '01/01/2025',
    to: '31/01/2025'
})

const triggers = {
    [Donut.selectors.segment]: (d) => `${d.data.name || d.data.type}: ${d.data.count}`
}

const weeklyData = ref([
    { semaine: 'S1', creees: 12, faites: 8 },
    { semaine: 'S2', creees: 15, faites: 12 },
    { semaine: 'S3', creees: 9, faites: 11 },
    { semaine: 'S4', creees: 18, faites: 14 },
    { semaine: 'S5', creees: 14, faites: 16 },
    { semaine: 'S6', creees: 11, faites: 9 },
    { semaine: 'S7', creees: 16, faites: 13 }
])

const technicianData = ref([
    { name: 'Pierre Dubois', count: 28, label: 'Pierre Dubois' },
    { name: 'Marie Durant', count: 24, label: 'Marie Durant' },
    { name: 'Jean Rousseau', count: 31, label: 'Jean Rousseau' },
    { name: 'Sophie Leroy', count: 22, label: 'Sophie Leroy' },
    { name: 'Paul Girard', count: 18, label: 'Paul Girard' }
])

const typeData = ref([
    { type: 'Maintenance', count: 45, label: 'Maintenance' },
    { type: 'Dépannage', count: 32, label: 'Dépannage' },
    { type: 'Installation', count: 28, label: 'Installation' },
    { type: 'Contrôle', count: 18, label: 'Contrôle' }
])

const interventions = ref([
    {
        id: 1,
        ref: 'MT4A8L',
        date: '25.07.2025',
        title: 'Maintenance préventive',
        category: 'Contrôle système',
        client: {
            name: 'Restaurant Le Gourmet',
            address: '12 rue de la Paix'
        },
        operator: {
            name: 'Jean Martin',
            role: 'Technicien',
            initials: 'J'
        },
        schedule: {
            time: 'Aujourd\'hui 08:30',
            status: 'Terminée',
            statusColor: 'text-green-600'
        },
        status: {
            label: 'Terminée',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        },
        priority: {
            label: 'Élevée',
            bgColor: 'bg-orange-100',
            textColor: 'text-orange-800'
        },
        isClickable: true
    },
    {
        id: 2,
        ref: 'DP9K3R',
        date: '25.07.2025',
        title: 'Dépannage urgent',
        category: 'Panne électrique',
        client: {
            name: 'Hôtel des Alpes',
            address: '45 avenue du Mont-Blanc'
        },
        operator: {
            name: 'Sophie Dubois',
            role: 'Électricienne',
            initials: 'S'
        },
        schedule: {
            time: 'Aujourd\'hui 11:45',
            status: 'En cours',
            statusColor: 'text-orange-600'
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
        id: 3,
        ref: 'IN2L5P',
        date: '26.07.2025',
        title: 'Installation équipement',
        category: 'Nouvel équipement',
        client: {
            name: 'Café Central',
            address: '8 place de la Bastille'
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
            address: '23 rue de Rivoli'
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
    }
])
</script>