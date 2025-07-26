<template>
    <div class="h-full flex flex-col bg-neutral-50">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Planning des interventions</h1>
                    <p class="text-neutral-600">Semaine du 26 Juillet - 1er Août 2025</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <Switch v-model="showWeekend" />
                        <Label class="text-sm">Afficher week-end</Label>
                    </div>
                    <Button variant="outline">
                        <ChevronLeft class="h-4 w-4" />
                        Semaine précédente
                    </Button>
                    <Button variant="outline">
                        Semaine suivante
                        <ChevronRight class="h-4 w-4" />
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Nouvelle intervention
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 overflow-auto">
            <div class="min-w-full">
                <div :class="['grid border-b bg-white', showWeekend ? 'grid-cols-8' : 'grid-cols-6']">
                    <div class="p-4 border-r font-medium text-neutral-700">Technicien</div>
                    <div v-for="day in visibleDays" :key="day.id" class="p-4 border-r text-center">
                        <div class="font-medium text-neutral-900">{{ day.name }}</div>
                        <div class="text-sm text-neutral-400">{{ day.date }}</div>
                    </div>
                </div>

                <div class="bg-white">
                    <div v-for="technician in technicians" :key="technician.id"
                        :class="['grid border-b hover:bg-neutral-50', showWeekend ? 'grid-cols-8' : 'grid-cols-6']">
                        <div class="p-4 border-r relative">
                            <div class="flex items-start space-x-3">
                                <div
                                    class="w-6 h-6 bg-neutral-200 rounded-full flex items-center justify-center font-medium text-sm mt-1">
                                    {{ technician.initials }}
                                </div>
                                <div class="flex-1">
                                    <div class="font-medium text-neutral-900">{{ technician.name }}</div>
                                    <div class="text-sm text-neutral-500">{{ technician.role }}</div>
                                    <div
                                        class=" px-4 py-3 bg-neutral-100 absolute bottom-4 left-4 right-4 rounded-md flex items-center gap-2">
                                        <span class="text-xs text-neutral-500">{{
                                            Math.round(getTechnicianWorkload(technician.id)) }}%</span>
                                        <ProgressRoot :model-value="getTechnicianWorkload(technician.id)"
                                            class="h-1.5 bg-white rounded-full flex-1">
                                            <ProgressIndicator class="bg-primary h-full rounded-full transition-all"
                                                :style="`width: ${getTechnicianWorkload(technician.id)}%`" />
                                        </ProgressRoot>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div v-for="day in visibleDays" :key="`${technician.id}-${day.id}`" :class="[
                            'p-2 border-r min-h-34',
                            isNonWorkingDay(technician.id, day.id) ? 'bg-neutral-100 bg-stripes opacity-50' : ''
                        ]">
                            <template v-if="isNonWorkingDay(technician.id, day.id)">
                                <div class="flex items-center justify-center h-28 text-xs text-neutral-400">
                                    Jour non travaillé
                                </div>
                            </template>
                            <template v-else>
                                <VueDraggable :model-value="getJobsForTechnicianAndDay(technician.id, day.id)"
                                    @update:model-value="(newJobs) => updateJobsForCell(technician.id, day.id, newJobs)"
                                    group="jobs" :animation="200" class="space-y-1 min-h-28">
                                    <div v-for="job in getJobsForTechnicianAndDay(technician.id, day.id)" :key="job.id"
                                        @click="openJobDialog(job)"
                                        class="px-2 py-1 rounded text-xs font-medium cursor-pointer hover:opacity-80 transition-opacity"
                                        :class="getJobCategoryClass(job.category)">
                                        <div class="font-medium">{{ getJobTimeRange(job) }}</div>
                                        <div class="truncate">{{ job.title }}</div>
                                        <div class="text-xs opacity-75">{{ job.client }} - {{ getJobCity(job.address) }}
                                        </div>
                                    </div>
                                </VueDraggable>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <Dialog :open="showJobDialog" @update:open="showJobDialog = $event">
            <DialogContent class="!w-6xl !h-[90vh] !max-w-none p-0 overflow-auto bg-accent">
                <JobView :inDialog="true" />
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import Dialog from '@/common/components/ui/dialog/Dialog.vue'
import DialogContent from '@/common/components/ui/dialog/DialogContent.vue'
import Switch from '@/common/components/ui/switch/Switch.vue'
import JobView from '@/main/views/JobView.vue'
import { ChevronLeft, ChevronRight, Plus } from 'lucide-vue-next'
import { ProgressIndicator, ProgressRoot } from 'reka-ui'
import { computed, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'

const showJobDialog = ref(false)
const selectedJob = ref(null)
const showWeekend = ref(false)

const weekDays = [
    { id: 1, name: 'Lundi', date: '26/07' },
    { id: 2, name: 'Mardi', date: '27/07' },
    { id: 3, name: 'Mercredi', date: '28/07' },
    { id: 4, name: 'Jeudi', date: '29/07' },
    { id: 5, name: 'Vendredi', date: '30/07' },
    { id: 6, name: 'Samedi', date: '31/07' },
    { id: 7, name: 'Dimanche', date: '01/08' }
]

const visibleDays = computed(() => {
    return showWeekend.value ? weekDays : weekDays.slice(0, 5)
})

const technicians = [
    {
        id: 1,
        name: 'Jean Martin',
        role: 'Technicien',
        initials: 'J',
        nonWorkingDays: [7] // Dimanche
    },
    {
        id: 2,
        name: 'Sophie Dubois',
        role: 'Technicienne',
        initials: 'S',
        nonWorkingDays: [3, 6] // Mercredi et Samedi
    },
    {
        id: 3,
        name: 'Pierre Leclerc',
        role: 'Installateur',
        initials: 'P',
        nonWorkingDays: [5] // Vendredi
    },
    {
        id: 4,
        name: 'Marie Rousseau',
        role: 'Technicienne',
        initials: 'M',
        nonWorkingDays: [6, 7] // Samedi et Dimanche
    },
    {
        id: 5,
        name: 'Antoine Bernard',
        role: 'Contrôleur',
        initials: 'A',
        nonWorkingDays: [2, 7] // Mardi et Dimanche
    },
    {
        id: 6,
        name: 'François Lambert',
        role: 'Diagnostiqueur',
        initials: 'F',
        nonWorkingDays: [1, 5] // Lundi et Vendredi
    }
]

const jobs = ref([
    // Jean Martin - Lundi
    {
        id: 1,
        ref: 'TR42K8',
        title: 'Panne électrique',
        category: 'Dépannage simple',
        client: 'SARL Martin',
        address: '15 rue de la République',
        time: '08:00',
        duration: '2h',
        status: 'En cours',
        technicianId: 1,
        dayId: 1,
        technician: 'Jean Martin'
    },
    {
        id: 2,
        ref: 'EL9K2M',
        title: 'Diagnostic électrique',
        category: 'Contrôle technique',
        client: 'Bureau Central',
        address: '45 rue de Rivoli',
        time: '14:00',
        duration: '1h30',
        status: 'Planifiée',
        technicianId: 1,
        dayId: 1,
        technician: 'Jean Martin'
    },

    // Jean Martin - Mardi
    {
        id: 3,
        ref: 'RQ4L8P',
        title: 'Remplacement fusibles',
        category: 'Maintenance',
        client: 'Pharmacie du Centre',
        address: '33 place de la République',
        time: '09:00',
        duration: '45min',
        status: 'Planifiée',
        technicianId: 1,
        dayId: 2,
        technician: 'Jean Martin'
    },
    {
        id: 4,
        ref: 'CT5B7Q',
        title: 'Contrôle technique',
        category: 'Vérification annuelle',
        client: 'Garage Moderne',
        address: '67 boulevard Voltaire',
        time: '15:00',
        duration: '1h',
        status: 'Terminée',
        technicianId: 1,
        dayId: 2,
        technician: 'Jean Martin'
    },

    // Sophie Dubois - Lundi
    {
        id: 5,
        ref: 'MP7X3L',
        title: 'Maintenance préventive',
        category: 'Contrôle mensuel',
        client: 'Hotel Plaza',
        address: '42 av. Champs-Élysées',
        time: '09:00',
        duration: '3h',
        status: 'Planifiée',
        technicianId: 2,
        dayId: 1,
        technician: 'Sophie Dubois'
    },
    {
        id: 6,
        ref: 'MN6Y2R',
        title: 'Maintenance chaudière',
        category: 'Entretien saisonnier',
        client: 'Résidence Les Jardins',
        address: '45 avenue de la Liberté',
        time: '15:30',
        duration: '2h',
        status: 'Planifiée',
        technicianId: 2,
        dayId: 1,
        technician: 'Sophie Dubois'
    },



    // Pierre Leclerc - Mardi
    {
        id: 8,
        ref: 'IN9R4V',
        title: 'Installation équipement',
        category: 'Nouvel équipement',
        client: 'Café Central',
        address: '8 place de la Bastille',
        time: '08:30',
        duration: '1h30',
        status: 'Planifiée',
        technicianId: 3,
        dayId: 2,
        technician: 'Pierre Leclerc'
    },
    {
        id: 9,
        ref: 'PL2M9X',
        title: 'Pose compteur',
        category: 'Installation',
        client: 'Épicerie Bio',
        address: '78 rue de la Paix',
        time: '14:00',
        duration: '2h',
        status: 'Planifiée',
        technicianId: 3,
        dayId: 2,
        technician: 'Pierre Leclerc'
    },

    // Pierre Leclerc - Jeudi
    {
        id: 10,
        ref: 'QR5T3N',
        title: 'Raccordement gaz',
        category: 'Installation',
        client: 'Boulangerie Paul',
        address: '23 rue de Rivoli',
        time: '09:30',
        duration: '3h',
        status: 'Planifiée',
        technicianId: 3,
        dayId: 4,
        technician: 'Pierre Leclerc'
    },

    // Marie Rousseau - Lundi
    {
        id: 11,
        ref: 'GZ4R8T',
        title: 'Contrôle gaz',
        category: 'Diagnostic Gaz',
        client: 'Restaurant Le Petit Zinc',
        address: '32 rue Saint-Antoine',
        time: '08:30',
        duration: '2h30',
        status: 'En retard',
        technicianId: 4,
        dayId: 1,
        technician: 'Marie Rousseau'
    },
    {
        id: 12,
        ref: 'WX7K9M',
        title: 'Réparation urgente',
        category: 'Dépannage',
        client: 'Clinique Pasteur',
        address: '156 rue de Vaugirard',
        time: '16:00',
        duration: '1h',
        status: 'À assigner',
        technicianId: 4,
        dayId: 1,
        technician: 'Marie Rousseau'
    },

    // Marie Rousseau - Vendredi
    {
        id: 13,
        ref: 'YZ8L4P',
        title: 'Contrôle sécurité',
        category: 'Audit sécurité',
        client: 'École Primaire',
        address: '90 boulevard Voltaire',
        time: '10:00',
        duration: '2h',
        status: 'Planifiée',
        technicianId: 4,
        dayId: 5,
        technician: 'Marie Rousseau'
    },

    // Antoine Bernard - Mercredi
    {
        id: 14,
        ref: 'DP3X9K',
        title: 'Diagnostic complet',
        category: 'Analyse système',
        client: 'Clinique Pasteur',
        address: '156 rue de Vaugirard',
        time: '09:00',
        duration: '4h',
        status: 'Planifiée',
        technicianId: 5,
        dayId: 3,
        technician: 'Antoine Bernard'
    },

    // Antoine Bernard - Vendredi
    {
        id: 15,
        ref: 'AB1C2D',
        title: 'Contrôle annuel',
        category: 'État des lieux',
        client: 'Immeuble Résidentiel',
        address: '125 avenue des Champs',
        time: '08:00',
        duration: '3h',
        status: 'Planifiée',
        technicianId: 5,
        dayId: 5,
        technician: 'Antoine Bernard'
    },
    {
        id: 16,
        ref: 'EF3G4H',
        title: 'Mise en conformité',
        category: 'Travaux réglementaires',
        client: 'Cabinet Médical',
        address: '67 rue de la Santé',
        time: '14:30',
        duration: '2h30',
        status: 'Planifiée',
        technicianId: 5,
        dayId: 5,
        technician: 'Antoine Bernard'
    },

    // François Lambert - Mardi
    {
        id: 17,
        ref: 'IJ5K6L',
        title: 'Expertise technique',
        category: 'Diagnostic',
        client: 'Usine Textile',
        address: '234 rue de l\'Industrie',
        time: '08:00',
        duration: '5h',
        status: 'En cours',
        technicianId: 6,
        dayId: 2,
        technician: 'François Lambert'
    },

    // François Lambert - Jeudi
    {
        id: 18,
        ref: 'MN7O8P',
        title: 'Analyse vibrations',
        category: 'Diagnostic spécialisé',
        client: 'Centre Commercial',
        address: '456 avenue du Commerce',
        time: '10:00',
        duration: '3h',
        status: 'Planifiée',
        technicianId: 6,
        dayId: 4,
        technician: 'François Lambert'
    },
    {
        id: 19,
        ref: 'QR9S0T',
        title: 'Rapport conformité',
        category: 'Audit final',
        client: 'Hôtel de Ville',
        address: '1 place de la Mairie',
        time: '15:00',
        duration: '2h',
        status: 'Planifiée',
        technicianId: 6,
        dayId: 4,
        technician: 'François Lambert'
    },

    // François Lambert - Samedi
    {
        id: 20,
        ref: 'UV1W2X',
        title: 'Urgence weekend',
        category: 'Dépannage urgent',
        client: 'Hôpital Saint-Louis',
        address: '10 avenue de la Santé',
        time: '09:00',
        duration: '3h',
        status: 'En retard',
        technicianId: 6,
        dayId: 6,
        technician: 'François Lambert'
    }
])

const getJobsForTechnicianAndDay = (technicianId, dayId) => {
    return jobs.value
        .filter(job => job.technicianId === technicianId && job.dayId === dayId)
        .sort((a, b) => {
            const timeA = a.time.split(':').map(Number)
            const timeB = b.time.split(':').map(Number)
            const minutesA = timeA[0] * 60 + timeA[1]
            const minutesB = timeB[0] * 60 + timeB[1]
            return minutesA - minutesB
        })
}

const parseDuration = (duration) => {
    // Convertit "2h", "1h30", "45min" en heures décimales
    if (duration.includes('h')) {
        const parts = duration.split('h')
        let hours = parseInt(parts[0])
        if (parts[1] && parts[1].includes('min')) {
            const minutes = parseInt(parts[1].replace('min', ''))
            hours += minutes / 60
        }
        return hours
    } else if (duration.includes('min')) {
        const minutes = parseInt(duration.replace('min', ''))
        return minutes / 60
    }
    return 0
}

const getTechnicianWorkHours = (technicianId) => {
    const technicianJobs = jobs.value.filter(job => job.technicianId === technicianId)
    const totalHours = technicianJobs.reduce((total, job) => {
        return total + parseDuration(job.duration)
    }, 0)
    return Math.round(totalHours * 10) / 10 // Arrondi à 1 décimale
}

const getTechnicianWorkload = (technicianId) => {
    const workHours = getTechnicianWorkHours(technicianId)
    return Math.min((workHours / 35) * 100, 100) // Limité à 100%
}

const isNonWorkingDay = (technicianId, dayId) => {
    const technician = technicians.find(t => t.id === technicianId)
    return technician?.nonWorkingDays?.includes(dayId) || false
}

const updateJobsForCell = (technicianId, dayId, newJobs) => {
    // Supprimer tous les jobs existants pour cette cellule
    for (let i = jobs.value.length - 1; i >= 0; i--) {
        if (jobs.value[i].technicianId === technicianId && jobs.value[i].dayId === dayId) {
            jobs.value.splice(i, 1)
        }
    }

    // Trier les nouveaux jobs par heure de début
    const sortedJobs = newJobs.sort((a, b) => {
        const timeA = a.time.split(':').map(Number)
        const timeB = b.time.split(':').map(Number)
        const minutesA = timeA[0] * 60 + timeA[1]
        const minutesB = timeB[0] * 60 + timeB[1]
        return minutesA - minutesB
    })

    // Ajouter les nouveaux jobs avec les bonnes assignations
    sortedJobs.forEach(job => {
        const updatedJob = {
            ...job,
            technicianId,
            dayId,
            technician: technicians.find(t => t.id === technicianId)?.name || job.technician
        }
        jobs.value.push(updatedJob)
    })
}

const getJobStatusClass = (status) => {
    const statusClasses = {
        'En cours': 'bg-orange-100 text-orange-800',
        'Planifiée': 'bg-neutral-100 text-neutral-800',
        'Terminée': 'bg-green-100 text-green-800',
        'En retard': 'bg-red-100 text-red-800',
        'À assigner': 'bg-yellow-100 text-yellow-800'
    }
    return statusClasses[status] || 'bg-neutral-100 text-neutral-800'
}

const getJobCategoryClass = (category) => {
    const categoryClasses = {
        'Dépannage simple': 'bg-blue-100 text-blue-800',
        'Dépannage urgent': 'bg-red-100 text-red-800',
        'Dépannage': 'bg-red-100 text-red-800',
        'État des lieux': 'bg-orange-100 text-orange-800',
        'Diagnostic Gaz': 'bg-green-100 text-green-800',
        'Audit Gaz': 'bg-violet-100 text-violet-800',
        'Contrôle technique': 'bg-blue-100 text-blue-800',
        'Maintenance': 'bg-green-100 text-green-800',
        'Vérification annuelle': 'bg-blue-100 text-blue-800',
        'Contrôle mensuel': 'bg-green-100 text-green-800',
        'Entretien saisonnier': 'bg-green-100 text-green-800',
        'Nouvel équipement': 'bg-violet-100 text-violet-800',
        'Installation': 'bg-violet-100 text-violet-800',
        'Audit sécurité': 'bg-orange-100 text-orange-800',
        'Analyse système': 'bg-violet-100 text-violet-800',
        'Travaux réglementaires': 'bg-orange-100 text-orange-800',
        'Diagnostic': 'bg-green-100 text-green-800',
        'Diagnostic spécialisé': 'bg-green-100 text-green-800',
        'Audit final': 'bg-orange-100 text-orange-800'
    }
    return categoryClasses[category] || 'bg-neutral-100 text-neutral-800'
}

const calculateEndTime = (startTime, duration) => {
    const [hours, minutes] = startTime.split(':').map(Number)
    const durationHours = parseDuration(duration)

    const totalMinutes = hours * 60 + minutes + (durationHours * 60)
    const endHours = Math.floor(totalMinutes / 60)
    const endMins = Math.round(totalMinutes % 60)

    return `${endHours.toString().padStart(2, '0')}:${endMins.toString().padStart(2, '0')}`
}

const getJobTimeRange = (job) => {
    const endTime = calculateEndTime(job.time, job.duration)
    return `${job.time} → ${endTime} (${job.duration})`
}

const getJobCity = (address) => {
    // Extrait la ville de l'adresse (dernier élément après la virgule, ou mot après les chiffres)
    if (address.includes(',')) {
        const parts = address.split(',')
        return parts[parts.length - 1].trim()
    }
    // Si pas de virgule, essaie d'extraire après les chiffres et rue
    const match = address.match(/\d+\s+.*?\s+(.+)/)
    return match ? match[1] : address
}

const openJobDialog = (job) => {
    selectedJob.value = job
    showJobDialog.value = true
}

const editJob = () => {
    console.log('Modifier intervention:', selectedJob.value.ref)
    showJobDialog.value = false
}
</script>