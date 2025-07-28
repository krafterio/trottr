<template>
    <RelationSelect v-model="selectedStatus" endpoint="/job-status" display-field="name" :placeholder="placeholder"
        :search-placeholder="searchPlaceholder" :trigger-class="triggerClass" :clearable="clearable"
        :disabled="disabled">
        <!-- Slot pour customiser l'affichage de l'item sélectionné -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <div class="flex items-center gap-2">
                    <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: item.color }"></div>
                    <span class="truncate font-medium">{{ item.name }}</span>
                </div>
            </slot>
        </template>

        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
                    <div class="w-3 h-3 rounded-full" :style="{ backgroundColor: item.color }"></div>
                    <div class="flex flex-col items-start min-w-0 flex-1">
                        <span class="font-medium text-sm truncate">{{ item.name }}</span>
                    </div>
                </div>
            </slot>
        </template>
    </RelationSelect>
</template>

<script setup>
import { RelationSelect } from '@/common/components/form/relation-select'
import { computed } from 'vue'

defineOptions({
    name: 'StatusSelect'
})

const props = defineProps({
    modelValue: {
        type: [Number, Object],
        default: null
    },
    placeholder: {
        type: String,
        default: 'Sélectionner un statut...'
    },
    searchPlaceholder: {
        type: String,
        default: 'Rechercher un statut...'
    },
    triggerClass: {
        type: String,
        default: ''
    },
    clearable: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'select'])

const selectedStatus = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
        emit('select', value)
    }
})
</script>