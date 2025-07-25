<template>
    <div class="h-full flex flex-col">
        <!-- Bandeau supérieur -->
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-gray-900">Planificateur d'interventions</h1>
                    <p class="text-gray-600">Optimisez l'attribution et la planification des interventions</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline" size="sm">
                        <Calendar class="h-4 w-4 mr-2" />
                        Aujourd'hui
                    </Button>
                    <Button size="sm">
                        <Plus class="h-4 w-4 mr-2" />
                        Planifier sélection
                    </Button>
                </div>
            </div>
        </div>

        <!-- Contenu principal -->
        <div class="flex-1 flex overflow-hidden">
            <!-- Liste des jobs non planifiés (gauche) -->
            <div class="w-80 bg-gray-50 border-r p-4 overflow-y-auto">
                <div class="mb-4">
                    <h3 class="font-semibold text-gray-900 mb-2">Jobs à planifier</h3>
                    <p class="text-sm text-gray-600">{{ unplannedJobs.length }} interventions en attente</p>
                </div>

                <div class="space-y-3">
                    <div v-for="job in unplannedJobs" :key="job.id"
                        class="bg-white rounded-lg border p-4 cursor-pointer hover:border-primary transition-colors"
                        @click="selectJob(job)">
                        <div class="flex items-start justify-between mb-2">
                            <div class="flex-1">
                                <h4 class="font-medium text-gray-900 text-sm">{{ job.title }}</h4>
                                <p class="text-xs text-gray-500 mt-1">{{ job.description }}</p>
                            </div>
                            <span :class="[
                                'inline-flex items-center px-2 py-1 rounded text-xs font-medium',
                                job.priority === 'Urgente' ? 'bg-red-100 text-red-800' :
                                    job.priority === 'Élevée' ? 'bg-orange-100 text-orange-800' :
                                        'bg-gray-100 text-gray-800'
                            ]">
                                {{ job.priority }}
                            </span>
                        </div>

                        <div class="flex items-center text-xs text-gray-600 mb-2">
                            <MapPin class="h-3 w-3 mr-1" />
                            {{ job.address }}
                        </div>

                        <div class="flex items-center justify-between text-xs">
                            <span class="text-gray-500">{{ job.client }}</span>
                            <span class="text-gray-500">{{ job.duration }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Zone principale (droite) -->
            <div class="flex-1 flex flex-col">
                <!-- Carte OpenStreetMap -->
                <div class="h-96 bg-white border-b">
                    <div class="h-full" ref="mapContainer">
                        <!-- La carte sera rendue ici -->
                    </div>
                </div>

                <!-- Planning Gantt -->
                <div class="flex-1 bg-white p-4 overflow-auto">
                    <div class="mb-4">
                        <h3 class="font-semibold text-gray-900 mb-2">Planning des opérateurs</h3>
                        <div class="flex items-center space-x-4 text-sm text-gray-600">
                            <span>Aujourd'hui - {{ currentDate }}</span>
                            <Button variant="ghost" size="sm" class="h-6 px-2">
                                <ChevronLeft class="h-3 w-3" />
                            </Button>
                            <Button variant="ghost" size="sm" class="h-6 px-2">
                                <ChevronRight class="h-3 w-3" />
                            </Button>
                        </div>
                    </div>

                    <!-- Grille Gantt -->
                    <div class="border rounded-lg overflow-hidden">
                        <!-- En-tête des heures -->
                        <div class="flex bg-gray-50 border-b">
                            <div class="w-48 p-3 border-r font-medium text-sm text-gray-700">
                                Opérateur
                            </div>
                            <div class="flex-1 grid grid-cols-12 text-xs text-gray-600">
                                <div v-for="hour in hours" :key="hour" class="p-2 border-r text-center">
                                    {{ hour }}h
                                </div>
                            </div>
                        </div>

                        <!-- Lignes des opérateurs -->
                        <div v-for="operator in operators" :key="operator.id" class="flex border-b hover:bg-gray-50">
                            <!-- Nom de l'opérateur -->
                            <div class="w-48 p-3 border-r flex items-center">
                                <div
                                    class="w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center text-white text-xs font-medium mr-3">
                                    {{ operator.initials }}
                                </div>
                                <div>
                                    <div class="font-medium text-sm text-gray-900">{{ operator.name }}</div>
                                    <div class="text-xs text-gray-500">{{ operator.zone }}</div>
                                </div>
                            </div>

                            <!-- Timeline des créneaux -->
                            <div class="flex-1 relative h-16">
                                <div class="grid grid-cols-12 h-full">
                                    <div v-for="hour in hours" :key="hour" class="border-r border-gray-100"></div>
                                </div>

                                <!-- Jobs planifiés -->
                                <div v-for="task in operator.tasks" :key="task.id" :style="{
                                    left: `${(task.startHour - 8) * 8.33}%`,
                                    width: `${task.duration * 8.33}%`
                                }" :class="[
                                    'absolute top-2 bottom-2 rounded px-2 text-xs text-white flex items-center justify-center',
                                    task.status === 'confirmed' ? 'bg-blue-500' : 'bg-green-500'
                                ]">
                                    <span class="truncate">{{ task.title }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Calendar, ChevronLeft, ChevronRight, MapPin, Plus } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'

// Données de démo
const currentDate = new Date().toLocaleDateString('fr-FR')

const unplannedJobs = ref([
    {
        id: 1,
        title: 'Panne électrique',
        description: 'Dépannage urgent système électrique',
        client: 'SARL Martin',
        address: '15 rue de la République, Lyon',
        priority: 'Urgente',
        duration: '2h',
        coordinates: [45.7640, 4.8357]
    },
    {
        id: 2,
        title: 'Maintenance climatisation',
        description: 'Contrôle et nettoyage système clim',
        client: 'Hotel Plaza',
        address: '42 av. Champs-Élysées, Lyon',
        priority: 'Élevée',
        duration: '1h30',
        coordinates: [45.7589, 4.8414]
    },
    {
        id: 3,
        title: 'Installation équipement',
        description: 'Pose nouveau matériel',
        client: 'Café Central',
        address: '8 place Bellecour, Lyon',
        priority: 'Normale',
        duration: '3h',
        coordinates: [45.7578, 4.8320]
    },
    {
        id: 4,
        title: 'Contrôle technique',
        description: 'Vérification annuelle obligatoire',
        client: 'Garage Moderne',
        address: '67 boulevard Voltaire, Lyon',
        priority: 'Normale',
        duration: '1h',
        coordinates: [45.7484, 4.8467]
    }
])

const operators = ref([
    {
        id: 1,
        name: 'Jean Martin',
        initials: 'JM',
        zone: 'Centre-ville',
        tasks: [
            { id: 1, title: 'Dépannage urgent', startHour: 9, duration: 2, status: 'confirmed' },
            { id: 2, title: 'Maintenance', startHour: 14, duration: 1.5, status: 'planned' }
        ]
    },
    {
        id: 2,
        name: 'Sophie Dubois',
        initials: 'SD',
        zone: 'Part-Dieu',
        tasks: [
            { id: 3, title: 'Installation', startHour: 10, duration: 3, status: 'confirmed' }
        ]
    },
    {
        id: 3,
        name: 'Pierre Leclerc',
        initials: 'PL',
        zone: 'Vieux Lyon',
        tasks: []
    },
    {
        id: 4,
        name: 'Marie Rousseau',
        initials: 'MR',
        zone: 'Presqu\'île',
        tasks: [
            { id: 4, title: 'Contrôle', startHour: 8, duration: 1, status: 'confirmed' },
            { id: 5, title: 'Réparation', startHour: 16, duration: 2, status: 'planned' }
        ]
    }
])

const hours = ref([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

const mapContainer = ref(null)
let map = null

const selectJob = (job) => {
    console.log('Job sélectionné:', job)
    // Ici on pourrait centrer la carte sur le job ou l'highlight
}

onMounted(async () => {
    // Initialisation de la carte Leaflet
    const L = await import('leaflet')

    // Import du CSS de Leaflet
    const link = document.createElement('link')
    link.rel = 'stylesheet'
    link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
    document.head.appendChild(link)

    // Initialiser la carte centrée sur Lyon
    map = L.default.map(mapContainer.value).setView([45.7640, 4.8357], 12)

    // Ajouter les tuiles OpenStreetMap
    L.default.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map)

    // Ajouter des marqueurs pour les jobs non planifiés
    unplannedJobs.value.forEach(job => {
        const marker = L.default.marker(job.coordinates).addTo(map)
        marker.bindPopup(`
      <div class="p-2">
        <h4 class="font-semibold">${job.title}</h4>
        <p class="text-sm text-gray-600">${job.client}</p>
        <p class="text-xs text-gray-500">${job.address}</p>
      </div>
    `)
    })
})
</script>