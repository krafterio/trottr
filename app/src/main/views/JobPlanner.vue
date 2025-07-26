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
                        <div class="flex items-center space-x-3">
                            <!-- Toggle jour/semaine -->
                            <Select v-model="timeScale">
                                <SelectTrigger class="w-32">
                                    <SelectValue placeholder="Échelle" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="hour">Heure</SelectItem>
                                    <SelectItem value="day">Jour</SelectItem>
                                </SelectContent>
                            </Select>

                            <!-- Navigation temporelle -->
                            <div class="flex items-center space-x-2 text-sm text-gray-600">
                                <span>{{ currentDateDisplay }}</span>
                                <Button variant="outline" size="sm" class="h-8 w-8" @click="previousPeriod">
                                    <ChevronLeft class="h-3 w-3" />
                                </Button>
                                <Button variant="outline" size="sm" class="h-8 w-8" @click="nextPeriod">
                                    <ChevronRight class="h-3 w-3" />
                                </Button>
                            </div>
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
                            <g-gantt-chart :chart-start="chartStart" :chart-end="chartEnd" :precision="timeScale"
                                bar-start="myBeginDate" bar-end="myEndDate" :hide-row-labels="true"
                                @mouseenter-bar="onMouseEnterBar" @mouseleave-bar="onMouseLeaveBar">
                                <g-gantt-row v-for="operator in ganttOperators" :key="operator.id" :label="''"
                                    :bars="operator.tasks" @drop="onDropTask" />
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
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/common/components/ui/select'
import { GGanttChart, GGanttRow } from '@infectoone/vue-ganttastic'
import { Calendar, ChevronLeft, ChevronRight, Eye, EyeOff, MapPin, Plus, User } from 'lucide-vue-next'
import { computed, nextTick, onMounted, ref } from 'vue'

// Données de démo et configuration
const currentDate = new Date().toLocaleDateString('fr-FR')
const currentDay = ref(new Date(2025, 0, 26))
const timeScale = ref('hour')

const unplannedJobs = ref([
    {
        id: 8,
        title: 'Réparation urgente',
        description: 'Intervention immédiate nécessaire',
        client: 'Clinique du Parc',
        address: '92 cours Gambetta, Lyon',
        priority: 'Urgente',
        duration: '1h30',
        coordinates: [45.7694, 4.8467]
    },
    {
        id: 9,
        title: 'Installation neuve',
        description: 'Pose équipement complet',
        client: 'Résidence Lumière',
        address: '34 rue de la Paix, Lyon',
        priority: 'Normale',
        duration: '4h',
        coordinates: [45.7621, 4.8251]
    }
])

// Tous les jobs (plannifiés et non plannifiés) pour la carte
const allJobs = computed(() => [
    { id: 1, title: 'Dépannage urgent', coordinates: [45.7640, 4.8357], isPlanned: true },
    { id: 2, title: 'Maintenance clim', coordinates: [45.7589, 4.8414], isPlanned: true },
    { id: 3, title: 'Installation équipement', coordinates: [45.7578, 4.8320], isPlanned: true },
    { id: 4, title: 'Contrôle qualité', coordinates: [45.7484, 4.8467], isPlanned: true },
    { id: 5, title: 'Maintenance préventive', coordinates: [45.7560, 4.8290], isPlanned: true },
    { id: 6, title: 'Contrôle technique', coordinates: [45.7650, 4.8380], isPlanned: true },
    { id: 7, title: 'Intervention urgente', coordinates: [45.7720, 4.8420], isPlanned: true },
    ...unplannedJobs.value.map(job => ({
        id: job.id,
        title: job.title,
        coordinates: job.coordinates,
        isPlanned: false
    }))
])

const hoveredJobId = ref(null)

// Données des opérateurs pour le Gantt selon la documentation
const ganttOperators = ref([
    {
        id: 'row1',
        label: 'Jean Martin',
        tasks: [
            {
                myBeginDate: "2025-01-26 09:00",
                myEndDate: "2025-01-26 11:00",
                ganttBarConfig: {
                    id: "task-jean-1",
                    hasHandles: true,
                    label: "Dépannage urgent",
                    jobId: 1,
                    style: {
                        background: "#16190c",
                        color: "white",
                        borderRadius: "20px",
                    }
                }
            },
            {
                myBeginDate: "2025-01-26 13:00",
                myEndDate: "2025-01-26 15:30",
                ganttBarConfig: {
                    id: "task-jean-2",
                    hasHandles: true,
                    label: "Maintenance clim",
                    jobId: 2,
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
                myBeginDate: "2025-01-26 08:00",
                myEndDate: "2025-01-26 09:00",
                ganttBarConfig: {
                    id: "task-sophie-1",
                    hasHandles: true,
                    label: "Installation équipement",
                    jobId: 3,
                    style: {
                        background: "#16190c",
                        borderRadius: "20px",
                        color: "white"
                    }
                }
            },
            {
                myBeginDate: "2025-01-26 14:00",
                myEndDate: "2025-01-26 15:00",
                ganttBarConfig: {
                    id: "task-sophie-2",
                    hasHandles: true,
                    label: "Contrôle qualité",
                    jobId: 4,
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
        tasks: [
            {
                myBeginDate: "2025-01-26 16:00",
                myEndDate: "2025-01-26 18:00",
                ganttBarConfig: {
                    id: "task-pierre-1",
                    hasHandles: true,
                    label: "Maintenance préventive",
                    jobId: 5,
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
        id: 'row4',
        label: 'Marie Rousseau',
        tasks: [
            {
                myBeginDate: "2025-01-26 10:30",
                myEndDate: "2025-01-26 11:30",
                ganttBarConfig: {
                    id: "task-marie-1",
                    label: "Contrôle technique",
                    hasHandles: true,
                    jobId: 6,
                    style: {
                        background: "#16190c",
                        borderRadius: "20px",
                        color: "white"
                    }
                }
            },
            {
                myBeginDate: "2025-01-26 19:00",
                myEndDate: "2025-01-26 20:30",
                ganttBarConfig: {
                    id: "task-marie-2",
                    label: "Intervention urgente",
                    hasHandles: true,
                    jobId: 7,
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

// Computed properties pour la gestion des dates
const currentDateDisplay = computed(() => {
    if (timeScale.value === 'hour') {
        return `${currentDay.value.toLocaleDateString('fr-FR')} - Vue heure`
    } else {
        return currentDay.value.toLocaleDateString('fr-FR')
    }
})

const chartStart = computed(() => {
    const start = new Date(currentDay.value)

    if (timeScale.value === 'hour') {
        start.setHours(6, 0, 0, 0)
        return start.toISOString().slice(0, 10) + ' 06:00'
    } else {
        start.setHours(0, 0, 0, 0)
        return start.toISOString().slice(0, 10) + ' 00:00'
    }
})

const chartEnd = computed(() => {
    const end = new Date(currentDay.value)

    if (timeScale.value === 'hour') {
        end.setHours(22, 0, 0, 0)
        return end.toISOString().slice(0, 10) + ' 22:00'
    } else {
        end.setDate(end.getDate() + 1)
        end.setHours(23, 59, 0, 0)
        return end.toISOString().slice(0, 10) + ' 23:59'
    }
})

// Navigation functions
const previousPeriod = () => {
    const newDay = new Date(currentDay.value)
    // Pour heure et jour : navigation par jour
    newDay.setDate(newDay.getDate() - 1)
    currentDay.value = newDay
}

const nextPeriod = () => {
    const newDay = new Date(currentDay.value)
    // Pour heure et jour : navigation par jour
    newDay.setDate(newDay.getDate() + 1)
    currentDay.value = newDay
}





// Gestion du hover sur les barres Gantt
const onMouseEnterBar = (event) => {
    const jobId = event.bar?.ganttBarConfig?.jobId
    if (jobId) {
        hoveredJobId.value = jobId
        updateMapMarkers()
    }
}

const onMouseLeaveBar = () => {
    hoveredJobId.value = null
    updateMapMarkers()
}

// Gestion du drop entre lignes
const onDropTask = (event) => {
    console.log('Drop task event:', event)
    // Ici on pourrait gérer le déplacement entre opérateurs
}

let markersMap = new Map()

const updateMapMarkers = () => {
    if (!map) return

    markersMap.forEach(marker => {
        const jobId = marker.jobId
        const isHovered = hoveredJobId.value === jobId

        // Changer la couleur du marqueur selon l'état hover
        marker.setIcon(L.divIcon({
            className: 'custom-marker',
            html: `<div style="
                background: ${isHovered ? '#ff4444' : '#3b82f6'};
                width: 20px;
                height: 20px;
                border-radius: 50%;
                border: 2px solid white;
                box-shadow: 0 0 0 2px rgba(0,0,0,0.2);
            "></div>`,
            iconSize: [15, 15],
            iconAnchor: [7.5, 7.5]
        }))
    })
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

    // Ajouter des marqueurs pour tous les jobs
    markersMap.clear()
    allJobs.value.forEach(job => {
        const marker = L.default.marker(job.coordinates, {
            icon: L.default.divIcon({
                className: 'custom-marker',
                html: `<div style="
                    background: ${job.isPlanned ? '#3b82f6' : '#10b981'};
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    border: 2px solid white;
                    box-shadow: 0 0 0 2px rgba(0,0,0,0.2);
                "></div>`,
                iconSize: [15, 15],
                iconAnchor: [7.5, 7.5]
            })
        }).addTo(map)

        marker.jobId = job.id
        markersMap.set(job.id, marker)

        marker.bindPopup(`
            <div class="p-2">
                <h4 class="font-semibold">${job.title}</h4>
                <p class="text-sm text-gray-600">${job.isPlanned ? 'Planifié' : 'Non planifié'}</p>
                <p class="text-xs text-gray-500">ID: ${job.id}</p>
            </div>
        `)
    })
}

onMounted(() => {
    initMap()
})
</script>