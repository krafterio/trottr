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
                    <Button v-if="showMap" variant="outline" size="sm" @click="toggleMap">
                        <EyeOff class="h-4 w-4" />
                        Masquer carte
                    </Button>
                    <Button v-else variant="outline" size="sm" @click="toggleMap">
                        <Eye class="h-4 w-4" />
                        Afficher la carte
                    </Button>
                    <Button variant="outline" size="sm">
                        <Calendar class="h-4 w-4" />
                        Aujourd'hui
                    </Button>
                    <Button size="sm">
                        <Plus class="h-4 w-4" />
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
                <div v-if="showMap" class="h-80 bg-white border-b relative">
                    <div class="h-full" ref="mapContainer">
                        <!-- La carte sera rendue ici -->
                    </div>
                </div>

                <!-- Planning Gantt -->
                <div class="flex-1 bg-white p-4 overflow-auto">
                    <div class="mb-4 flex justify-between items-center">
                        <h3 class="font-semibold text-gray-900">Planning des opérateurs</h3>
                        <div class="flex items-center space-x-2 text-sm text-gray-600">
                            <span>Aujourd'hui - {{ currentDate }}</span>
                            <Button variant="outline" size="sm" class="h-8 w-8" @click="previousDay">
                                <ChevronLeft class="h-3 w-3" />
                            </Button>
                            <Button variant="outline" size="sm" class="h-8 w-8" @click="nextDay">
                                <ChevronRight class="h-3 w-3" />
                            </Button>
                        </div>
                    </div>

                    <!-- Gantt Chart avec Vue-Ganttastic -->
                    <div class="border rounded-lg overflow-hidden flex" style="height: calc(100% - 50px);">
                        <!-- Colonne des opérateurs -->
                        <div class="w-48 bg-gray-50 border-r flex flex-col">
                            <!-- En-tête -->
                            <div
                                class="h-20.5 bg-gray-100 border-b-2 flex items-center px-3 font-medium text-sm text-gray-700">
                                Opérateurs
                            </div>
                            <!-- Liste des opérateurs -->
                            <div class="flex-1">
                                <div v-for="operator in ganttOperators" :key="operator.id"
                                    class="h-10 border-b-2 border-gray-200 flex items-center px-3 text-sm text-gray-900">
                                    <User class="h-4 w-4 mr-1" />
                                    {{ operator.label }}
                                </div>
                            </div>
                        </div>

                        <!-- Gantt timeline -->
                        <div class="flex-1">
                            <g-gantt-chart chart-start="2021-07-12 12:00" chart-end="2021-07-14 12:00" precision="hour"
                                bar-start="myBeginDate" bar-end="myEndDate" :hide-row-labels="true">
                                <g-gantt-row v-for="operator in ganttOperators" :key="operator.id" :label="''"
                                    :bars="operator.tasks" />
                            </g-gantt-chart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { GGanttChart, GGanttRow } from '@infectoone/vue-ganttastic'
import { Calendar, ChevronLeft, ChevronRight, Eye, EyeOff, MapPin, Plus, User } from 'lucide-vue-next'
import { nextTick, onMounted, ref } from 'vue'

// Données de démo
const currentDate = new Date().toLocaleDateString('fr-FR')
const currentDay = ref(new Date())

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

// Données des opérateurs pour le Gantt selon la documentation
const ganttOperators = ref([
    {
        id: 'row1',
        label: 'Jean Martin',
        tasks: [
            {
                myBeginDate: "2021-07-13 13:00",
                myEndDate: "2021-07-13 19:00",
                ganttBarConfig: {
                    id: "unique-id-1",
                    hasHandles: true,
                    label: "Dépannage urgent",
                    style: {
                        background: "#16190c",
                        color: "white",
                        borderRadius: "20px",
                    }
                }
            }
        ]
    },
    {
        id: 'row2',
        label: 'Sophie Dubois',
        tasks: [
            {
                myBeginDate: "2021-07-13 00:00",
                myEndDate: "2021-07-14 02:00",
                ganttBarConfig: {
                    id: "another-unique-id-2",
                    hasHandles: true,
                    label: "Installation équipement",
                    style: {
                        background: "#16190c",
                        borderRadius: "20px",
                        color: "white"
                    }
                }
            }
        ]
    },
    {
        id: 'row3',
        label: 'Pierre Leclerc',
        tasks: []
    },
    {
        id: 'row4',
        label: 'Marie Rousseau',
        tasks: [
            {
                myBeginDate: "2021-07-12 16:00",
                myEndDate: "2021-07-12 18:00",
                ganttBarConfig: {
                    id: "task-marie-1",
                    label: "Contrôle technique",
                    hasHandles: true,
                    style: {
                        background: "#16190c",
                        borderRadius: "20px",
                        color: "white"
                    }
                }
            }
        ]
    }
])

const mapContainer = ref(null)
let map = null
const showMap = ref(true)

const selectJob = (job) => {
    console.log('Job sélectionné:', job)
}

const previousDay = () => {
    const newDay = new Date(currentDay.value)
    newDay.setDate(newDay.getDate() - 1)
    currentDay.value = newDay
}

const nextDay = () => {
    const newDay = new Date(currentDay.value)
    newDay.setDate(newDay.getDate() + 1)
    currentDay.value = newDay
}

const toggleMap = async () => {
    showMap.value = !showMap.value

    if (showMap.value) {
        await nextTick()
        initMap()
    }
}

const initMap = async () => {
    if (!mapContainer.value) return

    // Initialisation de la carte Leaflet
    const L = await import('leaflet')

    // Import du CSS de Leaflet
    if (!document.querySelector('link[href*="leaflet.css"]')) {
        const leafletLink = document.createElement('link')
        leafletLink.rel = 'stylesheet'
        leafletLink.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'
        document.head.appendChild(leafletLink)
    }

    // Nettoyer la carte existante si elle existe
    if (map) {
        map.remove()
    }

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
}

onMounted(() => {
    initMap()
})
</script>