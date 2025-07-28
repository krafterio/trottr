<template>
    <Select v-model="selectedPriority" :disabled="disabled">
        <SelectTrigger class="w-full">
            <SelectValue :placeholder="placeholder">
                <div v-if="selectedPriority" class="flex items-center gap-2">
                    <component :is="getPriorityConfig(selectedPriority).icon" class="w-5 h-4"
                        :class="getPriorityConfig(selectedPriority).color" />
                    <span>{{ getPriorityConfig(selectedPriority).label }}</span>
                </div>
            </SelectValue>
        </SelectTrigger>
        <SelectContent>
            <SelectItem v-for="option in priorityOptions" :key="option.value" :value="option.value">
                <div class="flex items-center gap-2">
                    <component :is="option.icon" class="w-5 h-4" :class="option.color" />
                    <span>{{ option.label }}</span>
                </div>
            </SelectItem>
        </SelectContent>
    </Select>
</template>

<script setup>
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { useJob } from '@/common/composables/useJob'
import { computed } from 'vue'

defineOptions({
    name: 'PrioritySelect'
})

const props = defineProps({
    modelValue: {
        type: String,
        default: 'normal'
    },
    placeholder: {
        type: String,
        default: 'Sélectionner une priorité...'
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue'])

const { getPriorityConfig, getPriorityOptions } = useJob()

const selectedPriority = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
    }
})

const priorityOptions = getPriorityOptions()
</script>