<template>
    <RelationSelect 
        v-model="selectedContact"
        endpoint="/contacts"
        display-field="full_name"
        image-field="photo_url"
        subtitle-field="email"
        :placeholder="placeholder"
        :search-placeholder="searchPlaceholder"
        :trigger-class="triggerClass"
        :clearable="clearable"
        :disabled="disabled"
    >
        <!-- Slot pour customiser l'affichage du contact sélectionné -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <Avatar class="h-4 w-4 rounded-md">
                    <AvatarImage v-if="item.photo_url" :src="`/storage/download/${item.photo_url}`" v-fetcher-src.lazy />
                    <AvatarFallback class="text-xs rounded-md">
                        {{ item.full_name?.charAt(0) || 'C' }}
                    </AvatarFallback>
                </Avatar>
                <span class="truncate font-medium">{{ item.full_name }}</span>
            </slot>
        </template>
        
        <!-- Slot pour customiser l'affichage dans la liste -->
        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
                    <Avatar class="h-6 w-6 rounded-md">
                        <AvatarImage v-if="item.photo_url" :src="`/storage/download/${item.photo_url}`" v-fetcher-src.lazy />
                        <AvatarFallback class="rounded-md text-xs">
                            {{ item.full_name?.charAt(0) || 'C' }}
                        </AvatarFallback>
                    </Avatar>
                    <div class="flex flex-col items-start min-w-0 flex-1">
                        <span class="font-medium text-sm truncate">{{ item.full_name }}</span>
                        <span v-if="item.email" class="text-xs text-muted-foreground truncate">
                            {{ item.email }}
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
import { Avatar, AvatarImage, AvatarFallback } from '@/common/components/ui/avatar'

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
        default: false
    },
    disabled: {
        type: Boolean,
        default: false
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
</script> 
