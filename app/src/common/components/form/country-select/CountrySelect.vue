<template>
    <RelationSelect v-model="selectedCountry" endpoint="/countries" display-field="name" search-param="search"
        :placeholder="placeholder" :search-placeholder="searchPlaceholder" :trigger-class="triggerClass"
        :clearable="clearable" :disabled="disabled">
        <!-- Slot pour customiser l'affichage du pays sélectionné -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <span class="truncate">{{ item.name }}</span>
            </slot>
        </template>

        <!-- Slot pour customiser l'affichage dans la liste -->
        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
                    <span class="font-medium text-sm truncate">{{ item.name }}</span>
                </div>
            </slot>
        </template>
    </RelationSelect>
</template>

<script setup>
import { RelationSelect } from '@/common/components/form/relation-select'
import { computed } from 'vue'

defineOptions({
    name: 'CountrySelect'
})

const props = defineProps({
    modelValue: {
        type: [Number, Object],
        default: null
    },
    placeholder: {
        type: String,
        default: 'Sélectionner un pays...'
    },
    searchPlaceholder: {
        type: String,
        default: 'Rechercher un pays...'
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

const selectedCountry = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
        emit('select', value)
    }
})
</script>
