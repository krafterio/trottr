<template>
    <Dialog :open="open" @update:open="$emit('update:open', $event)">
        <DialogContent class="!w-[90vw] !h-[90vh] !max-w-none p-0 overflow-auto !gap-0 overflow-y-hidden">
            <DialogHeader class="px-4 pt-3  pb-0 border-b bg-white h-20">
                <div class="flex items-start justify-between">
                    <ScanSearch class="h-10 w-10 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                    <div class="flex-1">
                        <DialogTitle class="text-xl mb-1">{{ job?.name || 'Intervention à assigner' }}</DialogTitle>
                        <div class="flex items-center gap-3">
                            <Badge v-if="job?.reference" variant="outline" class="font-mono">
                                #{{ job.reference }}
                            </Badge>
                            <div class="flex items-center gap-2 text-sm text-neutral-600">
                                <MapPin class="h-4 w-4" />
                                <span>{{ getClientAddress() }}</span>
                            </div>

                            <Badge v-if="job?.priority" :class="getPriorityClass(job.priority)">
                                <component :is="getPriorityConfig(job?.priority).icon" class="h-3 w-3" />
                                {{ getPriorityLabel(job.priority) }}
                            </Badge>
                            <Badge v-if="job?.category" variant="outline">
                                <Folder class="h-3 w-3 mr-1" />
                                {{ job.category.name }}
                            </Badge>
                            <Badge v-if="job?.status"
                                :style="{ backgroundColor: job.status.color + '20', color: job.status.color }">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                {{ job.status.name }}
                            </Badge>
                        </div>
                    </div>
                </div>
            </DialogHeader>

            <div class="flex h-[calc(90vh-80px)]">
                <div class="w-70 border-r bg-white p-3 overflow-y-auto">
                    <div class="space-y-4">
                        <div>
                            <h3 class="text-md font-semibold text-neutral-900 mb-3">Techniciens</h3>
                            <div class="mb-3">
                                <Select v-model="selectedSpeciality" @update:model-value="filterOperators">
                                    <SelectTrigger class="w-full">
                                        <SelectValue placeholder="Toutes les spécialités" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="all">Toutes les spécialités</SelectItem>
                                        <SelectItem v-for="speciality in availableSpecialities" :key="speciality.id"
                                            :value="speciality.id">
                                            {{ speciality.name }}
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                            <div v-if="loadingOperators" class="text-center py-4">
                                <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary mx-auto mb-2">
                                </div>
                                <p class="text-sm text-neutral-500">Chargement des techniciens...</p>
                            </div>
                            <div v-else class="space-y-2">
                                <div v-for="operator in filteredOperators" :key="operator.id"
                                    @click="selectOperator(operator)" :class="[
                                        'p-2 rounded-md cursor-pointer border transition-colors',
                                        selectedOperator?.id === operator.id
                                            ? 'bg-primary text-primary-foreground border-neutral-300'
                                            : 'bg-neutral-100 hover:bg-muted text-neutral-600'
                                    ]">
                                    <div class="flex items-center space-x-3">
                                        <div class="flex-1 min-w-0">
                                            <p class="font-medium truncate text-sm">{{ operator.name }}</p>
                                            <p class="text-xs text-neutral-500 truncate">{{ operator.speciality }}</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="flex-1 flex flex-col">
                    <div v-if="selectedOperator" class="flex-1">
                        <div class="h-full">
                            <VueCal :events="selectedOperatorEvents" view="week" :hide-weekends="false"
                                :editable-events="{ create: !isEditMode && !selectedSlot, resize: true, drag: true, delete: false }"
                                :snap-to-interval="30" :time-step="60" :cell-height="40" :time-from="6 * 60" locale="fr"
                                :hide-view-selector="true" :disable-views="['years', 'year', 'month', 'day', 'days']"
                                @event-created="onEventCreated" @event-change="onEventChange" class="h-full" />
                        </div>
                    </div>
                    <div v-else class="flex-1 flex items-center justify-center">
                        <div class="text-center">
                            <User class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                            <p class="text-neutral-600">Sélectionnez un technicien pour voir son planning</p>
                        </div>
                    </div>

                    <div v-if="selectedSlot"
                        class="bg-white border-t border-neutral-200 p-4 max-h-24 transition-all duration-300 ease-in-out">
                        <div class="flex items-center justify-between">
                            <div class="flex-1">
                                <div class="flex items-center gap-4">
                                    <div class="flex items-center gap-2">
                                        <User class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm font-medium text-neutral-900">
                                            {{ selectedSlot.operator?.name }}
                                        </span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <Calendar class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-700">
                                            {{ formatSlotDate(selectedSlot.start) }}
                                        </span>
                                    </div>
                                    <div class="flex items-center gap-2">
                                        <Clock class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-700">
                                            De {{ formatSlotTime(selectedSlot.start) }} à {{
                                                formatSlotTime(selectedSlot.end) }}
                                        </span>
                                    </div>
                                    <div class="flex items-center gap-2 text-neutral-500 text-sm">
                                        <Clock class="h-4 w-4 text-neutral-500" />
                                        <span>Durée:</span>
                                        <span class="text-primary font-semibold">
                                            {{ getSlotDuration(selectedSlot) }}
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="flex items-center gap-2">
                                <Button v-if="!isEditMode" variant="outline" @click="cancelSlot" class="mr-2">
                                    Annuler
                                </Button>
                                <Button @click="assignJob">
                                    <CalendarCheck class="h-4 w-4" />
                                    {{ isEditMode ? 'Modifier l\'assignation' : 'Planifier sur ce créneau' }}
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div v-else-if="selectedOperator && !selectedSlot">
                        <div class="flex-1 flex items-center h-14 px-4">
                            <LucideSquareDashedMousePointer class="h-8 w-8 text-neutral-400 me-2" />
                            <div class="flex flex-col">
                                <p class="text-xs text-neutral-400">Dessinez un créneau sur le calendrier pour planifier
                                    l'intervention. Le créneau n'est entregistré qu'à la validation après cette fenêtre.
                                </p>
                                <p class="text-sm text-neutral-600">
                                    Opérateur sélectionné:
                                    <span class="text-primary font-semibold">
                                        {{ selectedOperator.name }}
                                    </span>
                                </p>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import Button from '@/common/components/ui/button/Button.vue'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { useFetcher } from '@/common/composables/fetcher'
import { useJob } from '@/common/composables/useJob'
import { useWorkspaceStore } from '@/main/stores/workspace'
import { Calendar, CalendarCheck, Circle, Clock, Folder, LucideSquareDashedMousePointer, MapPin, ScanSearch, User } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'
import { VueCal } from 'vue-cal'
import 'vue-cal/style.css'

const props = defineProps({
    open: {
        type: Boolean,
        default: false
    },
    job: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['update:open', 'assigned'])

const fetcher = useFetcher()
const { getPriorityConfig } = useJob()
const workspaceStore = useWorkspaceStore()

const selectedOperator = ref(null)
const currentDate = ref(new Date())

const operators = ref([])
const loadingOperators = ref(true)
const loadingEvents = ref(false)
const jobSpecialities = ref([])
const loadingSpecialities = ref(false)

const fetchJobSpecialities = async () => {
    loadingSpecialities.value = true
    try {
        const response = await fetcher.get('/job-speciality')
        jobSpecialities.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des spécialités:', error)
    } finally {
        loadingSpecialities.value = false
    }
}

const fetchOperators = async () => {
    loadingOperators.value = true
    try {
        const response = await fetcher.get('/operators', {
            params: {
                workspace: workspaceStore.workspace?.id
            }
        })

        const allUsers = response.data?.items || []

        const operatorsOnly = allUsers.filter(user => user.role === 'Operator')

        operators.value = operatorsOnly.map(user => ({
            id: user.id,
            name: user.name || user.email,
            speciality: user.job_specialities?.map(s => s.name).join(', ') || 'Opérateur',
            speciality_ids: user.job_specialities?.map(s => s.id) || [],
            available: true,
            events: []
        }))

        if (operators.value.length > 0) {
            if (isEditMode.value && props.job?.operator) {
                const existingOperator = operators.value.find(op => op.id === props.job.operator.id)
                if (existingOperator) {
                    selectedOperator.value = existingOperator
                    await fetchOperatorEvents(existingOperator)
                    createExistingSlot()
                } else {
                    selectedOperator.value = operators.value[0]
                    await fetchOperatorEvents(operators.value[0])
                }
            } else if (hasScheduledDateButNoOperator.value) {
                selectedOperator.value = operators.value[0]
                await fetchOperatorEvents(operators.value[0])
                createToAssignSlot()
                assignToAssignSlot()
            } else {
                selectedOperator.value = operators.value[0]
                await fetchOperatorEvents(operators.value[0])
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement des opérateurs:', error)
    } finally {
        loadingOperators.value = false
    }
}

const createExistingSlot = () => {
    if (isEditMode.value && props.job?.operator && props.job?.scheduled_start && props.job?.scheduled_end) {
        selectedSlot.value = {
            start: new Date(props.job.scheduled_start),
            end: new Date(props.job.scheduled_end),
            title: props.job.name,
            class: 'creation-slot-calendar',
            operator: selectedOperator.value
        }
    }
}

const createToAssignSlot = () => {
    if (props.job?.scheduled_start && props.job?.scheduled_end) {
        selectedSlot.value = {
            start: new Date(props.job.scheduled_start),
            end: new Date(props.job.scheduled_end),
            title: props.job.name,
            class: 'toassign-slot-calendar',
            operator: null
        }
    }
}

const fetchOperatorEvents = async (operator) => {
    if (!operator) return

    operator.events = []

    try {
        const now = new Date()
        const startOfWeek = new Date(now)
        startOfWeek.setDate(now.getDate() - now.getDay() + 1)
        startOfWeek.setHours(0, 0, 0, 0)

        const endOfWeek = new Date(startOfWeek)
        endOfWeek.setDate(startOfWeek.getDate() + 6)
        endOfWeek.setHours(23, 59, 59, 999)

        const response = await fetcher.get(`/jobs/by-operator/${operator.id}`, {
            params: {
                start_date: startOfWeek.toISOString(),
                end_date: endOfWeek.toISOString()
            }
        })

        const events = response.data
            .filter(job => !isEditMode.value || job.id !== props.job?.id)
            .map(job => ({
                start: new Date(job.scheduled_start),
                end: new Date(job.scheduled_end),
                title: job.name,
                class: 'bg-blue-500 text-white',
                job: job
            }))

        operator.events = events

    } catch (error) {
        console.error('Erreur lors du chargement des événements:', error)
    }
}

const selectedOperatorEvents = computed(() => {
    if (!selectedOperator.value) return []
    const events = [...selectedOperator.value.events]

    if (selectedSlot.value) {
        events.push(selectedSlot.value)
    }

    return events.map(event => {
        if (event.class === 'creation-slot-calendar' || event.class === 'toassign-slot-calendar') {
            return event
        } else {
            return {
                ...event,
                draggable: false,
                resizable: false,
                deletable: false
            }
        }
    })
})


const previousWeek = () => {
    currentDate.value = new Date(currentDate.value.getTime() - 7 * 24 * 60 * 60 * 1000)
}

const nextWeek = () => {
    currentDate.value = new Date(currentDate.value.getTime() + 7 * 24 * 60 * 60 * 1000)
}

const getPriorityClass = (priority) => {
    const config = getPriorityConfig(priority)
    return config.bgColor + ' ' + config.color
}

const getPriorityLabel = (priority) => {
    const config = getPriorityConfig(priority)
    return config.label
}

const getDuration = () => {
    if (props.job?.scheduled_start && props.job?.scheduled_end) {
        const start = new Date(props.job.scheduled_start)
        const end = new Date(props.job.scheduled_end)
        const diffMs = end - start
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
        return `${diffHours}h ${diffMinutes}min`
    }
    return 'Durée non définie'
}

const getClientAddress = () => {
    if (props.job?.site) {
        const parts = [
            props.job.site.name,
            props.job.site.street,
            props.job.site.zip,
            props.job.site.city
        ].filter(Boolean)
        return parts.join(', ')
    }
    return 'Adresse non définie'
}

const selectedSlot = ref(null)

const onEventCreated = (event) => {
    if (event.start && event.end) {
        const startDate = new Date(event.start)
        const endDate = new Date(event.end)

        selectedSlot.value = {
            start: startDate,
            end: endDate,
            title: props.job?.name || 'Intervention à assigner',
            class: 'creation-slot-calendar',
            operator: selectedOperator.value
        }
    }
}

const assignToAssignSlot = () => {
    if (selectedSlot.value && selectedSlot.value.class === 'toassign-slot-calendar' && selectedOperator.value) {
        selectedSlot.value.class = 'creation-slot-calendar'
        selectedSlot.value.operator = selectedOperator.value
    }
}

const selectOperator = (operator) => {
    selectedOperator.value = operator
    fetchOperatorEvents(operator)

    if (selectedSlot.value) {
        selectedSlot.value = {
            ...selectedSlot.value,
            operator: operator
        }

        assignToAssignSlot()
    }
}

const onEventChange = (event) => {
    if (selectedSlot.value) {
        const startDate = new Date(event.start)
        const endDate = new Date(event.end)

        selectedSlot.value = {
            ...selectedSlot.value,
            start: startDate,
            end: endDate
        }

        assignToAssignSlot()
    }
}

const formatSlotDate = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleDateString('fr-FR', {
        weekday: 'long',
        day: 'numeric',
        month: 'long'
    })
}

const formatSlotTime = (date) => {
    if (!date) return ''
    return new Date(date).toLocaleTimeString('fr-FR', {
        hour: '2-digit',
        minute: '2-digit'
    })
}

const getSlotDuration = (slot) => {
    if (!slot?.start || !slot?.end) return ''
    const start = new Date(slot.start)
    const end = new Date(slot.end)
    const diffMs = end - start
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))

    if (diffHours > 0) {
        return `${diffHours}h${diffMinutes > 0 ? ` ${diffMinutes}min` : ''}`
    }
    return `${diffMinutes}min`
}

const assignJob = async () => {
    if (selectedSlot.value && selectedOperator.value && props.job) {
        try {
            const jobId = props.job.id

            const updateData = {
                operator: selectedSlot.value.operator.id,
                scheduled_start: selectedSlot.value.start.toISOString(),
                scheduled_end: selectedSlot.value.end.toISOString()
            }

            const response = await fetcher.patch(`/jobs/${jobId}`, updateData)

            const toastMessage = getToastMessage()

            emit('assigned', {
                operator: selectedSlot.value.operator,
                job: props.job,
                slot: selectedSlot.value,
                updatedJob: response.data,
                toastMessage: toastMessage
            })

            selectedSlot.value = null
            emit('update:open', false)

        } catch (error) {
            console.error('Erreur lors de la mise à jour du job:', error)
        }
    }
}

const getToastMessage = () => {

    if (!isEditMode.value) {
        const date = formatSlotDate(selectedSlot.value.start)
        const time = formatSlotTime(selectedSlot.value.start)
        return `Intervention planifiée au ${date} à ${time} et assignée à ${selectedSlot.value.operator.name}`
    }

    const originalOperator = props.job.operator?.id
    const currentOperator = selectedSlot.value.operator.id
    const originalStart = new Date(props.job.scheduled_start)
    const currentStart = selectedSlot.value.start
    const operatorChanged = originalOperator !== currentOperator
    const slotChanged = Math.abs(originalStart.getTime() - currentStart.getTime()) > 1000

    if (operatorChanged && slotChanged) {
        const date = formatSlotDate(selectedSlot.value.start)
        const time = formatSlotTime(selectedSlot.value.start)
        return `Intervention replanifiée au ${date} à ${time} et assignée à ${selectedSlot.value.operator.name}`
    } else if (slotChanged) {
        return `Intervention modifiée pour le ${formatSlotDate(selectedSlot.value.start)} à ${formatSlotTime(selectedSlot.value.start)}`
    } else {
        return `Intervention assignée à ${selectedSlot.value.operator.name}`
    }
}

const cancelSlot = () => {
    selectedSlot.value = null
}

const filterOperators = () => {
    if (!selectedSpeciality.value || selectedSpeciality.value === 'all') {
        operators.value = operators.value.map(op => ({ ...op, available: true }))
    } else {
        operators.value = operators.value.map(op => ({
            ...op,
            available: op.speciality_ids.includes(selectedSpeciality.value)
        }))
    }
}

const isEditMode = computed(() => {
    return props.job?.operator && props.job?.scheduled_start && props.job?.scheduled_end
})

const hasScheduledDateButNoOperator = computed(() => {
    return props.job?.scheduled_start && props.job?.scheduled_end && !props.job?.operator
})

const availableSpecialities = computed(() => {
    return jobSpecialities.value
})

const filteredOperators = computed(() => {
    if (!selectedSpeciality.value || selectedSpeciality.value === 'all') {
        return operators.value
    }
    return operators.value.filter(op => op.speciality_ids.includes(selectedSpeciality.value))
})

const selectedSpeciality = ref('')

watch(() => props.open, (newValue) => {
    if (newValue) {
        fetchJobSpecialities()
        fetchOperators()
    }
})
</script>