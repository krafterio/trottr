<template>
    <RelationSelect v-model="selectedCompany" endpoint="/companies" display-field="name" :placeholder="placeholder"
        :search-placeholder="searchPlaceholder" :trigger-class="triggerClass" :clearable="clearable"
        :disabled="disabled">
        <!-- Slot pour customiser l'affichage de l'item sélectionné -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <span class="truncate font-medium">{{ item.name }}</span>
            </slot>
        </template>

        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
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
    name: 'CompanySelect'
})

const props = defineProps({
    modelValue: {
        type: [Number, Object],
        default: null
    },
    placeholder: {
        type: String,
        default: 'Sélectionner une société...'
    },
    searchPlaceholder: {
        type: String,
        default: 'Rechercher une société...'
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

const selectedCompany = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
        emit('select', value)
    }
})
</script>
