<template>
    <div class="flex items-start space-x-4">
        <div
            class="w-6 h-6 bg-primary text-primary-foreground border border-primary rounded-full flex items-center justify-center flex-shrink-0">
            <MessageSquareText class="h-3 w-3" />
        </div>
        <div class="flex flex-col flex-1">
            <div class="flex justify-between">
                <div class="flex items-center space-x-2">
                    <Avatar class="h-6 w-6 rounded-sm">
                        <AvatarImage v-if="activity.created_by.avatar"
                            :src="`/storage/download/${activity.created_by.avatar}`" v-fetcher-src.lazy
                            :alt="activity.created_by?.name" class="h-6 w-6" />
                        <AvatarFallback>{{ activity.created_by?.name?.charAt(0)?.toUpperCase() || 'U' }}
                        </AvatarFallback>
                    </Avatar>
                    <p class="text-sm"><strong>{{ activity.created_by.name }}</strong> a ajouté une note interne
                        à l'intervention
                    </p>
                </div>
                <span class="text-xs flex items-center text-neutral-500">
                    <Calendar class="h-3 w-3 mr-2" />
                    {{ formatDate(activity.created_at) }}
                </span>
            </div>
            <Card class="mt-2 p-0 relative group">
                <CardContent class="p-4">
                    <p>{{ activity.content }}</p>
                </CardContent>
                <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                        <Button variant="outline" class="absolute top-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity 
                    w-8 h-8">
                            <MoreVertical class="h-3 w-3" />
                        </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                        <DropdownMenuItem @click="editNote">
                            <Edit class="h-3 w-3" />
                            Éditer
                        </DropdownMenuItem>
                        <DropdownMenuItem @click="deleteNote">
                            <Trash class="h-3 w-3 text-destructive" />
                            Supprimer
                        </DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
            </Card>
        </div>
    </div>
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Button } from '@/common/components/ui/button'
import Card from '@/common/components/ui/card/Card.vue'
import CardContent from '@/common/components/ui/card/CardContent.vue'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { bus } from '@/common/composables/bus'
import { Calendar, Edit, MessageSquareText, MoreVertical, Trash } from 'lucide-vue-next'

const props = defineProps({
    activity: {
        type: Object,
        required: true
    }
})

const editNote = () => {
    bus.trigger('open-note-dialog', {
        mode: 'edit',
        activity: props.activity,
        content: props.activity.content
    })
}

const deleteNote = () => {
    bus.trigger('open-note-dialog', {
        mode: 'delete',
        activity: props.activity
    })
}

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