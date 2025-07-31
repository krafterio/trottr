<template>
    <div class="flex items-start space-x-4">
        <div class="w-6 h-6 bg-white text-primary border rounded-full flex items-center justify-center flex-shrink-0">
            <Pen class="h-3 w-3" />
        </div>
        <div class="flex-1 min-w-0 flex justify-between">
            <div class="flex items-center space-x-2">
                <Avatar class="h-6 w-6 rounded-sm">
                    <AvatarImage v-if="activity.created_by.avatar"
                        :src="`/storage/download/${activity.created_by.avatar}`" v-fetcher-src.lazy
                        :alt="activity.created_by?.name" class="h-6 w-6" />
                    <AvatarFallback>{{ activity.created_by?.name?.charAt(0)?.toUpperCase() || 'U' }}
                    </AvatarFallback>
                </Avatar>
                <p class="text-sm"><strong>{{ activity.created_by.name }}</strong> {{
                    getActivitySentence(activity.field_name) }} <strong>{{ activity?.new_status?.name || activity?.new_operator?.name || activity.new_value }}</strong></p>
            </div>
            <span class="text-xs flex items-center text-neutral-500">
                <Calendar class="h-3 w-3 mr-2" />
                {{ formatDate(activity.created_at) }}
            </span>
        </div>
    </div>
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Calendar, Pen } from 'lucide-vue-next'

const props = defineProps({
    activity: {
        type: Object,
        required: true
    }
})

const getActivitySentence = (type) => {
    switch (type) {
        case 'operator':
            return 'a assigné l\'intervention à'
        case 'status':
            return 'a mis à jour le statut de l\'intervention à'
        case 'priority':
            return 'a défini la priorité de l\'intervention sur'
        case 'description':
    }
}

const formatDate = (dateString) => {
    if (!dateString) return ''

    const date = new Date(dateString)
    const now = new Date()

    const dateDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
    const nowDate = new Date(now.getFullYear(), now.getMonth(), now.getDate())

    const diffTime = nowDate.getTime() - dateDate.getTime()
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 0) {
        return `Aujourd'hui ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`
    } else if (diffDays === 1) {
        return `Hier ${date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}`
    } else {
        const options = {
            weekday: 'short',
            day: '2-digit',
            month: 'short',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }
        return date.toLocaleDateString('fr-FR', options)
    }
}
</script>