<template>
    <div class="p-4">
        <div class="flex items-center justify-between mb-4">
            <h2 class="text-lg font-semibold text-neutral-900">Tâches associées à l'intervention
            </h2>
            <Button @click="openTaskDialog">
                <Plus class="h-4 w-4" />
                Ajouter une tâche
            </Button>
        </div>

        <div v-if="tasksLoading" class="flex-1 flex items-center justify-center py-12">
            <div class="text-center">
                <div
                    class="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto mb-4">
                </div>
                <p class="text-neutral-600">Chargement des tâches...</p>
            </div>
        </div>

        <div v-else-if="jobTasks.length === 0" class="text-center py-8 text-neutral-500">
            <p>Aucune tâche ajoutée</p>
            <p class="text-sm mt-2">Ajoutez des tâches pour décomposer l'intervention en actions spécifiques</p>
        </div>

        <div v-else>
            <VueDraggable v-model="jobTasks" :animation="200" handle=".drag-handle" @end="onTaskReorder"
                class="grid grid-cols-1 gap-4">
                <div v-for="task in jobTasks" :key="task.id"
                    class="bg-white border rounded-lg p-4 pb-3 flex flex-row items-start">
                    <Switch v-model="task.is_done" class="mt-2 mr-4"
                        @update:model-value="(value) => handleTaskStatusChange(task, value)" />
                    <div class="flex flex-col flex-1">
                        <div class="flex items-start justify-between">
                            <div class="flex items-center space-x-2">
                                <h3 class="font-medium text-neutral-900">{{
                                    task.job_task.name }}</h3>
                            </div>
                            <div class="flex items-center gap-2">
                                <DropdownMenu>
                                    <DropdownMenuTrigger asChild>
                                        <Button variant="outline" size="sm">
                                            Modifier
                                            <ChevronDown class="h-4 w-4" />
                                        </Button>
                                    </DropdownMenuTrigger>
                                    <DropdownMenuContent align="end">
                                        <DropdownMenuItem @click="handleEditTask(task)">
                                            <Pen class="h-4 w-4" />
                                            Modifier
                                        </DropdownMenuItem>
                                        <DropdownMenuItem @click="handleDeleteTask(task)">
                                            <Trash class="text-destructive h-4 w-4" />
                                            Supprimer
                                        </DropdownMenuItem>
                                    </DropdownMenuContent>
                                </DropdownMenu>
                                <Button variant="ghost" size="sm" class="h-6 w-6 p-0 drag-handle cursor-move">
                                    <GripVertical class="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                        <p class="text-sm text-neutral-600 mb-3">{{ task.description }}</p>
                        <div class="flex items-center justify-between text-xs text-neutral-500">
                            <div class="flex items-center gap-2" v-if="task.is_done">
                                <Avatar class="h-4 w-4 rounded-sm mb-0.5" v-if="task.done_by && task.done_by.avatar">
                                    <AvatarImage :src="`/storage/download/${task.done_by?.avatar}`" v-fetcher-src.lazy
                                        :alt="task.done_by?.name" class="h-4 w-4" />
                                </Avatar>
                                <span v-if="task.done_by">{{ task.done_by.name || task.done_by.email
                                }}</span>
                                <span v-if="task.done_at">Terminée le {{ formatDate(task.done_at)
                                }}</span>
                            </div>
                            <div v-else class="flex items-center gap-1 text-neutral-400">
                                <Info class="h-3 w-3" />
                                <span>Tâche à réaliser</span>
                            </div>
                        </div>
                    </div>
                </div>
            </VueDraggable>
        </div>

        <!-- Dialog pour ajouter une tâche -->
        <Dialog :open="taskDialogOpen" @update:open="taskDialogOpen = false">
            <DialogContent class="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>{{ isEditTask ? 'Modifier la tâche' : 'Ajouter une tâche' }}</DialogTitle>
                    <DialogDescription>Modifiez la tâche et sa description</DialogDescription>
                </DialogHeader>
                <form @submit.prevent="handleTaskSubmit" class="space-y-4">
                    <div class="grid gap-2">
                        <Label for="task">Tâche *</Label>
                        <Select v-model="taskForm.job_task" @update:model-value="handleTaskChange">
                            <SelectTrigger class="w-full">
                                <SelectValue placeholder="Sélectionnez une tâche" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="task in availableTasks" :key="task.id" :value="task.id">
                                    {{ task.name }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                    </div>

                    <div class="grid gap-2">
                        <Label for="description">Description</Label>
                        <Textarea v-model="taskForm.description" placeholder="Description détaillée de la tâche..."
                            rows="4" />
                    </div>

                    <div class="flex items-center space-x-2">
                        <Switch v-model="taskForm.is_done" />
                        <Label for="is_done">Tâche réalisée ?</Label>
                    </div>

                    <div v-if="taskForm.is_done" class="grid gap-4">
                        <div class="grid gap-2">
                            <Label for="done_by">Réalisée par</Label>
                            <UserSelect v-model="taskForm.done_by" placeholder="Sélectionner un utilisateur" />
                        </div>

                        <div class="grid gap-2">
                            <Label for="done_at">Date de réalisation</Label>
                            <Popover>
                                <PopoverTrigger as-child>
                                    <Button variant="outline" class="justify-start text-left font-normal">
                                        <CalendarIcon class="mr-2 h-4 w-4" />
                                        {{ dateValue ? df.format(toDate(dateValue)) : 'Sélectionner une date' }}
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent class="w-auto p-0">
                                    <Calendar v-model:placeholder="placeholder" :model-value="dateValue"
                                        calendar-label="Date de réalisation" initial-focus
                                        :min-value="new CalendarDate(2020, 1, 1)" :max-value="today(getLocalTimeZone())"
                                        @update:model-value="(v) => {
                                            if (v) {
                                                taskForm.done_at = v.toString()
                                            } else {
                                                taskForm.done_at = null
                                            }
                                        }" />
                                </PopoverContent>
                            </Popover>
                        </div>
                    </div>
                </form>
                <DialogFooter>
                    <Button variant="outline" @click="taskDialogOpen = false">Annuler</Button>
                    <Button @click="handleTaskSubmit" :disabled="loading">
                        {{ loading ? 'Enregistrement...' : (isEditTask ? 'Modifier' : 'Ajouter') }}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import UserSelect from '@/common/components/form/user-select/UserSelect.vue'
import Avatar from '@/common/components/ui/avatar/Avatar.vue'
import AvatarImage from '@/common/components/ui/avatar/AvatarImage.vue'
import { Button } from '@/common/components/ui/button'
import { Calendar } from '@/common/components/ui/calendar'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import { Label } from '@/common/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/common/components/ui/popover'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Switch } from '@/common/components/ui/switch'
import { Textarea } from '@/common/components/ui/textarea'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { CalendarDate, DateFormatter, getLocalTimeZone, parseDate, today } from '@internationalized/date'
import { toDate } from 'reka-ui/date'

import { Calendar as CalendarIcon, ChevronDown, GripVertical, Info, Pen, Plus, Trash } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { toast } from 'vue-sonner'

const props = defineProps({
    jobId: {
        type: [String, Number],
        required: true
    }
})

const fetcher = useFetcher()

const jobTasks = ref([])
const taskDialogOpen = ref(false)
const isEditTask = ref(false)
const editingTaskId = ref(null)
const selectedTaskForDelete = ref(null)
const loading = ref(false)
const tasksLoading = ref(true)
const taskForm = ref({
    job_task: null,
    description: '',
    is_done: false,
    done_by: null,
    done_at: null
})
const availableTasks = ref([])

const df = new DateFormatter('fr-FR', {
    dateStyle: 'long',
})

const placeholder = ref()

const dateValue = computed({
    get: () => {
        if (!taskForm.value.done_at) return undefined
        try {
            return parseDate(taskForm.value.done_at)
        } catch (error) {
            console.error('Erreur parsing date:', error)
            return undefined
        }
    },
    set: (val) => {
        if (val) {
            taskForm.value.done_at = val.toString()
        } else {
            taskForm.value.done_at = null
        }
    }
})

const fetchJobTasks = async () => {
    try {
        tasksLoading.value = true
        const response = await fetcher.get('/job-job-tasks', { params: { job: props.jobId } })
        jobTasks.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des tâches:', error)
    } finally {
        tasksLoading.value = false
    }
}

const fetchAvailableTasks = async () => {
    try {
        const response = await fetcher.get('/job-tasks')
        availableTasks.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des tâches disponibles:', error)
    }
}

const openTaskDialog = () => {
    isEditTask.value = false
    taskForm.value = {
        job_task: null,
        description: '',
        is_done: false,
        done_by: null,
        done_at: null
    }
    taskDialogOpen.value = true
}

const handleTaskSubmit = async () => {
    if (!taskForm.value.job_task) {
        toast.error('Veuillez sélectionner une tâche')
        return
    }

    try {
        loading.value = true
        const selectedTask = availableTasks.value.find(t => t.id === taskForm.value.job_task)

        const payload = {
            job: props.jobId,
            job_task: taskForm.value.job_task,
            name: selectedTask.name,
            description: taskForm.value.description,
            is_done: taskForm.value.is_done,
            done_by: taskForm.value.done_by && typeof taskForm.value.done_by === 'object' ? taskForm.value.done_by.id : taskForm.value.done_by,
            done_at: taskForm.value.done_at ? new Date(taskForm.value.done_at).toISOString() : null
        }

        if (isEditTask.value && editingTaskId.value) {
            await fetcher.patch(`/job-job-tasks/${editingTaskId.value}`, payload)
            toast.success('Tâche modifiée avec succès')
        } else {
            payload.sequence = jobTasks.value.length + 1
            await fetcher.post('/job-job-tasks', payload)
            toast.success('Tâche ajoutée avec succès')
        }
        taskDialogOpen.value = false
        await fetchJobTasks()
    } catch (error) {
        console.error('Erreur lors de l\'ajout/modification de la tâche:', error)
        toast.error('Erreur lors de l\'ajout/modification de la tâche')
    } finally {
        loading.value = false
    }
}

const handleTaskChange = () => {
    if (taskForm.value.job_task) {
        const selectedTask = availableTasks.value.find(t => t.id === taskForm.value.job_task)
        if (selectedTask) {
            taskForm.value.description = selectedTask.description || ''
        }
    }
}

const handleEditTask = (task) => {
    isEditTask.value = true
    editingTaskId.value = task.id
    taskForm.value = {
        job_task: task.job_task.id,
        description: task.description || '',
        is_done: task.is_done,
        done_by: task.done_by && task.done_by.id ? task.done_by.id : null,
        done_at: task.done_at ? new Date(task.done_at).toISOString().split('T')[0] : null
    }
    taskDialogOpen.value = true
}

const handleDeleteTask = (task) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer la tâche',
        message: 'Êtes-vous sûr de vouloir supprimer cette tâche ?',
        itemName: task.job_task.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-task:confirmed'
    })
    selectedTaskForDelete.value = task
}

const deleteTask = async () => {
    if (!selectedTaskForDelete.value) return

    try {
        await fetcher.delete(`/job-job-tasks/${selectedTaskForDelete.value.id}`)
        toast.success('Tâche supprimée avec succès')
        bus.trigger('confirm-delete-dialog:close')
        await fetchJobTasks()
        selectedTaskForDelete.value = null
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const handleTaskStatusChange = async (task, isDone) => {
    try {
        const response = await fetcher.patch(`/job-job-tasks/${task.id}/toggle_done_state`)

        // Mettre à jour localement la tâche avec les données retournées
        Object.assign(task, response.data)

        toast.success(task.is_done ? 'Tâche marquée comme terminée' : 'Tâche marquée comme en cours')
    } catch (error) {
        console.error('Erreur lors de la mise à jour du statut:', error)
        toast.error('Erreur lors de la mise à jour du statut')
        // Remettre l'ancienne valeur en cas d'erreur
        task.is_done = !isDone
    }
}

const onTaskReorder = async () => {
    try {
        const reorderData = jobTasks.value.map((task, index) => ({
            id: task.id,
            sequence: index + 1
        }))

        await fetcher.put('/job-job-tasks/reorder', { job_tasks: reorderData })
        toast.success('Tâches réorganisées avec succès')
    } catch (error) {
        console.error('Erreur lors du réordonnancement:', error)
        toast.error('Erreur lors du réordonnancement')
        await fetchJobTasks() // Recharger l'ordre original
    }
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

useBus(bus, 'confirm-delete-task:confirmed', () => {
    deleteTask()
})

onMounted(() => {
    fetchJobTasks()
    fetchAvailableTasks()
})
</script>