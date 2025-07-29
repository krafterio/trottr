<template>
    <div class="p-6">
        <div v-if="loading" class="text-center py-8">
            <div class="animate-spin w-8 h-8 border-2 border-neutral-300 border-t-neutral-900 rounded-full mx-auto">
            </div>
            <p class="text-neutral-600 mt-4">Chargement des interventions...</p>
        </div>

        <div v-else-if="jobs.length === 0" class="text-center py-8">
            <Wrench class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
            <h3 class="text-lg font-medium text-neutral-900 mb-2">Aucune intervention</h3>
            <p class="text-neutral-600 mb-4">Cette entreprise n'a pas encore d'interventions associées.</p>
            <Button @click="handleCreateJob" class="inline-flex items-center">
                <Plus class="w-4 h-4" />
                Ajouter une intervention
            </Button>
        </div>

        <div v-else class="space-y-4">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-medium text-neutral-900">Interventions ({{ jobs.length }})</h3>
                <Button @click="handleCreateJob" size="sm" class="inline-flex items-center">
                    <Plus class="w-4 h-4" />
                    Ajouter une intervention
                </Button>
            </div>

            <div>
                <Table>
                    <TableHeader
                        class="bg-neutral-50 text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-5">
                        <TableRow>
                            <TableHead class="py-3 w-12">
                                <Checkbox :checked="isAllSelected" @update:checked="toggleSelectAll" />
                            </TableHead>
                            <TableHead class="py-3">Réf.</TableHead>
                            <TableHead class="py-3">Intervention</TableHead>
                            <TableHead class="py-3">Opérateur</TableHead>
                            <TableHead class="py-3">Date/Heure</TableHead>
                            <TableHead class="py-3">Statut</TableHead>
                            <TableHead class="py-3">Priorité</TableHead>
                            <TableHead class="w-12 py-3"></TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        <TableRow v-for="job in jobs" :key="job.id" class="hover:bg-neutral-50">
                            <TableCell @click.stop>
                                <Checkbox :checked="selectedJobs.includes(job.id)"
                                    @update:checked="toggleJobSelection(job.id)" />
                            </TableCell>
                            <TableCell>
                                <div class="flex flex-col gap-1 py-2">
                                    <div class="text-sm font-medium font-mono underline text-neutral-900 cursor-pointer hover:text-primary"
                                        @click.stop="handleRowClick(job)">{{ job.reference }}</div>
                                    <div class="text-xs text-neutral-500">{{ formatDate(job.created_at) }}</div>
                                </div>
                            </TableCell>
                            <TableCell>
                                <div class="flex flex-col gap-1 py-2">
                                    <div class="text-sm font-medium text-neutral-900 underline cursor-pointer hover:text-primary"
                                        @click="handleRowClick(job)">{{ job.name }}</div>
                                    <div v-if="job.description" class="text-sm text-neutral-500 truncate max-w-xs">
                                        {{ job.description }}
                                    </div>
                                    <div v-if="job.category" class="text-xs text-neutral-500">
                                        {{ job.category.name }}
                                    </div>
                                </div>
                            </TableCell>
                            <TableCell>
                                <div v-if="job.operator" class="flex items-center py-2">
                                    <div class="flex-shrink-0 h-8 w-8">
                                        <div
                                            class="h-8 w-8 rounded-full bg-neutral-100 flex items-center justify-center">
                                            <span class="text-sm font-medium text-neutral-600">
                                                {{ getInitials(job.operator.name) }}
                                            </span>
                                        </div>
                                    </div>
                                    <div class="ml-3">
                                        <div class="text-sm font-medium text-neutral-900">
                                            {{ job.operator.name }}
                                        </div>
                                    </div>
                                </div>
                                <div v-else class="text-sm text-neutral-500">Non assigné</div>
                            </TableCell>
                            <TableCell>
                                <div v-if="job.scheduled_start" class="py-2">
                                    {{ formatDate(job.scheduled_start) }}
                                </div>
                                <div v-else class="text-neutral-500">Non planifié</div>
                            </TableCell>
                            <TableCell>
                                <span v-if="job.status"
                                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800 py-2">
                                    {{ job.status.name }}
                                </span>
                                <span v-else class="text-neutral-500">-</span>
                            </TableCell>
                            <TableCell>
                                <div class="flex items-center gap-2 py-2">
                                    <component :is="getPriorityConfig(job.priority).icon" class="w-4 h-4"
                                        :class="getPriorityConfig(job.priority).color" />
                                    <span class="text-sm">{{ getPriorityConfig(job.priority).label }}</span>
                                </div>
                            </TableCell>
                            <TableCell @click.stop>
                                <DropdownMenu>
                                    <DropdownMenuTrigger as-child>
                                        <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                            <MoreVertical class="h-4 w-4" />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end">
                                        <DropdownMenuItem @click.stop="handleEdit(job)">
                                            <Eye class="mr-2 h-4 w-4" />
                                            Voir
                                        </DropdownMenuItem>
                                        <DropdownMenuItem @click.stop="handleDelete(job)" class="text-red-600">
                                            <Trash class="mr-2 h-4 w-4" />
                                            Supprimer
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import { bus } from '@/common/composables/bus'
import { useJob } from '@/common/composables/useJob'
import { Eye, MoreVertical, Plus, Trash, Wrench } from 'lucide-vue-next'
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
    jobs: {
        type: Array,
        required: true
    },
    company: {
        type: Object,
        required: true
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const router = useRouter()
const { getPriorityConfig } = useJob()

const selectedJobs = ref([])

const isAllSelected = computed(() => {
    return props.jobs.length > 0 && selectedJobs.value.length === props.jobs.length
})

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    })
}

const getInitials = (name) => {
    if (!name) return ''
    return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const handleRowClick = (job) => {
    router.push(`/job/${job.id}`)
}

const handleEdit = (job) => {
    router.push(`/job/${job.id}`)
}

const handleDelete = (job) => {
    // TODO: Implémenter la suppression
}

const handleCreateJob = () => {
    bus.trigger('open-job-dialog', { company: props.company })
}

const toggleJobSelection = (jobId) => {
    const index = selectedJobs.value.indexOf(jobId)
    if (index > -1) {
        selectedJobs.value.splice(index, 1)
    } else {
        selectedJobs.value.push(jobId)
    }
}

const toggleSelectAll = (checked) => {
    if (checked) {
        selectedJobs.value = props.jobs.map(job => job.id)
    } else {
        selectedJobs.value = []
    }
}
</script>