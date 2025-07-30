<template>
    <RelationSelect v-model="selectedContact" endpoint="/contacts" display-field="full_name" :placeholder="placeholder"
        :search-placeholder="searchPlaceholder" :trigger-class="triggerClass" :clearable="clearable"
        :disabled="disabled" :params="contactParams">
        <!-- Slot pour customiser l'affichage de l'item sélectionné -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <span class="truncate font-medium">{{ item.full_name || `${item.first_name} ${item.last_name}`.trim()
                    }}</span>
            </slot>
        </template>

        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
                    <div class="flex flex-col items-start min-w-0 flex-1">
                        <span class="font-medium text-sm truncate">{{ item.full_name || `${item.first_name}
                            ${item.last_name}`.trim() }}</span>
                        <span v-if="item.function" class="text-xs text-neutral-500 truncate">{{ item.function }}</span>
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
    name: 'ContactSelect'
})

const props = defineProps({
    modelValue: {
        type: [Number, Object],
        default: null
    },
    placeholder: {
        type: String,
        default: 'Sélectionner un contact...'
    },
    searchPlaceholder: {
        type: String,
        default: 'Rechercher un contact...'
    },
    triggerClass: {
        type: String,
        default: ''
    },
    clearable: {
        type: Boolean,
        default: true
    },
    disabled: {
        type: Boolean,
        default: false
    },
    company: {
        type: [Number, null],
        default: null
    }
})

const emit = defineEmits(['update:modelValue', 'select'])

const selectedContact = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
        emit('select', value)
    }
})

const contactParams = computed(() => {
    const params = {}
    if (props.company) {
        params.company = props.company
    }
    return params
})
</script>