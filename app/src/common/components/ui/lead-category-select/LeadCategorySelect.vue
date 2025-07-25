<template>
    <RelationSelect 
        v-model="selectedCategory"
        endpoint="/lead_categories"
        display-field="name"
        :extra-fields="['color', 'description']"
        placeholder="Sélectionner une catégorie..."
        search-placeholder="Rechercher une catégorie..."
        empty-message="Aucune catégorie trouvée."
        :clearable="clearable"
        :disabled="disabled"
        :class="triggerClass"
    >
        <!-- Slot pour customiser l'affichage de la catégorie sélectionnée -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: item.color }"></div>
                <span class="truncate">{{ item.name }}</span>
            </slot>
        </template>
        
        <!-- Slot pour customiser l'affichage dans la liste -->
        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
                    <div class="w-4 h-4 rounded-full border border-border" :style="{ backgroundColor: item.color }"></div>
                    <div class="flex flex-col items-start min-w-0 flex-1">
                        <span class="font-medium text-sm truncate">{{ item.name }}</span>
                        <span v-if="item.description" class="text-xs text-muted-foreground truncate">
                            {{ item.description }}
                        </span>
                    </div>
                </div>
            </slot>
        </template>
    </RelationSelect>
</template>

<script setup>
import { computed } from 'vue'
import { RelationSelect } from '@/common/components/ui/relation-select'

defineOptions({
    name: 'LeadCategorySelect'
})

const props = defineProps({
    modelValue: {
        type: [String, Number, Object],
        default: null
    },
    clearable: {
        type: Boolean,
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
    },
    triggerClass: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['update:modelValue', 'select'])

const selectedCategory = computed({
    get: () => props.modelValue,
    set: (value) => {
        emit('update:modelValue', value)
        emit('select', value)
    }
})
</script> 
