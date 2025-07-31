<template>
    <div v-if="loading" class="text-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
        <p class="text-neutral-600">Chargement de l'historique...</p>
    </div>

    <div v-else-if="error" class="text-center py-8 text-red-500">
        <p>Erreur lors du chargement de l'historique</p>
        <p class="text-sm mt-2">{{ error }}</p>
    </div>

    <div v-else-if="activities.length === 0" class="text-center py-8 text-neutral-500">
        <p>Aucune activité enregistrée</p>
        <p class="text-sm mt-2">L'historique des activités apparaîtra ici</p>
    </div>

    <div v-else class="space-y-6">
        <div v-for="(activity, index) in activities" :key="activity.id" class="relative">
            <div v-if="index < activities.length - 1" class="absolute left-3 top-6 -bottom-10 w-px bg-neutral-200">
            </div>

            <JahCreate :activity="activity" v-if="activity.type === 'tracking_create'" />
            <JahEdit :activity="activity" v-else-if="activity.type === 'tracking_update'" />
            <JahNote :activity="activity" v-else-if="activity.type === 'note'" />

            <div v-else class="flex items-start space-x-4">
                <div
                    class="w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center flex-shrink-0">
                    <component :is="getActivityIcon(activity.type)" class="h-3 w-3" />
                </div>
                <div class="flex-1 min-w-0">
                    <div class="rounded-lg p-4 border">
                        <div class="flex items-center justify-between mb-2">
                            <div class="flex items-center space-x-2">
                                <Avatar class="h-6 w-6">
                                    <AvatarImage v-if="activity.created_by.avatar"
                                        :src="`/storage/download/${activity.created_by.avatar}`" v-fetcher-src.lazy
                                        :alt="activity.created_by?.name" class="h-6 w-6" />
                                    <AvatarFallback>{{ activity.created_by?.name?.charAt(0)?.toUpperCase() || 'U' }}
                                    </AvatarFallback>
                                </Avatar>
                                <h3 class="font-medium">{{ getActivityTitle(activity.type) }} {{
                                    activity.created_by.name }}</h3>
                            </div>
                            <span class="text-xs flex items-center text-neutral-500">
                                <Calendar class="h-3 w-3 mr-2" />
                                {{ formatDate(activity.created_at) }}
                            </span>
                        </div>

                        <div v-if="activity.content" class="text-sm text-neutral-600 mb-2">
                            {{ activity.content }}
                        </div>

                        <div v-if="activity.type === 'tracking_update' && activity.field_name"
                            class="text-xs text-neutral-500 bg-neutral-50 rounded p-2 mt-2">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="font-medium">Champ modifié :</span>
                                <span>{{ activity.field_name }}</span>
                            </div>
                            <div v-if="activity.old_value || activity.new_value" class="grid grid-cols-2 gap-2 text-xs">
                                <div>
                                    <span class="font-medium">Ancienne valeur :</span>
                                    <div class="bg-red-50 text-red-700 rounded px-2 py-1 mt-1">
                                        {{ activity.old_value || 'Vide' }}
                                    </div>
                                </div>
                                <div>
                                    <span class="font-medium">Nouvelle valeur :</span>
                                    <div class="bg-green-50 text-green-700 rounded px-2 py-1 mt-1">
                                        {{ activity.new_value || 'Vide' }}
                                    </div>
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
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useFilters } from '@/common/composables/filters'
import { Calendar, Edit, MessageSquare, Plus, StickyNote } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import JahCreate from './JobActivityHistory/JahCreate.vue'
import JahEdit from './JobActivityHistory/JahEdit.vue'
import JahNote from './JobActivityHistory/JahNote.vue'

const props = defineProps({
    jobId: {
        type: [String, Number],
        required: true
    }
})

const activities = ref([])
const loading = ref(true)
const error = ref(null)

const fetcher = useFetcher()
const { normalizeJson } = useFilters()

useBus(bus, 'job-activity-history-refresh', () => {
    loadActivities()
})

const loadActivities = async () => {
    try {
        loading.value = true
        error.value = null

        const response = await fetcher.get(`/job_activities`, {
            params: {
                job_id: props.jobId,
                limit: 50,
                offset: 0,
                order_by: 'created_at:desc',
            },
            headers: {
                'X-Filter': await normalizeJson('job_activity', ['job', '=', props.jobId]),
                'X-Fields': 'id,type,content,field_name,old_value,new_value,created_at,created_by.id,created_by.name,created_by.avatar,job.reference',
            },
        })

        activities.value = response.data.items || []
    } catch (err) {
        error.value = err.message || 'Erreur lors du chargement'
        console.error('Erreur lors du chargement des activités:', err)
    } finally {
        loading.value = false
    }
}

const getActivityIcon = (type) => {
    switch (type) {
        case 'message':
            return MessageSquare
        case 'note':
            return StickyNote
        case 'tracking_create':
            return Plus
        case 'tracking_update':
            return Edit
        default:
            return StickyNote
    }
}

const getActivityTitle = (type) => {
    switch (type) {
        case 'message':
            return 'Message de'
        case 'note':
            return 'Note interne de'
        case 'tracking_create':
            return 'Création par'
        case 'tracking_update':
            return 'Modification par'
        default:
            return 'Activité de'
    }
}

const getUserName = (userId) => {
    return `Utilisateur ${userId}`
}

const formatDate = (dateString) => {
    if (!dateString) return ''

    const date = new Date(dateString)
    const now = new Date()
    const diffTime = Math.abs(now - date)
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

    const options = {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }

    if (diffDays === 0) {
        return `Aujourd'hui ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`
    } else if (diffDays === 1) {
        return `Hier ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`
    } else {
        return date.toLocaleDateString('fr-FR', options)
    }
}

onMounted(() => {
    loadActivities()
})
</script>
