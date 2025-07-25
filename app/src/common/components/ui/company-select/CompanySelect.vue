<template>
    <RelationSelect 
        v-model="selectedCompany"
        endpoint="/companies"
        display-field="name"
        image-field="logo"
        subtitle-field="domain"
        :extra-fields="['domain']"
        :placeholder="placeholder"
        :search-placeholder="searchPlaceholder"
        :trigger-class="triggerClass"
        :clearable="clearable"
        :disabled="disabled"
    >
        <!-- Slot pour customiser l'affichage de l'item sélectionné -->
        <template #selected-item="{ item }">
            <slot name="selected-item" :item="item">
                <Avatar class="h-4 w-4 rounded-md">
                    <AvatarImage v-if="item.logo" :src="`/storage/download/${item.logo}`" v-fetcher-src.lazy />
                    <AvatarFallback class="text-xs rounded-md">
                        <Building class="h-2 w-2" />
                    </AvatarFallback>
                </Avatar>
                <span class="truncate font-medium">{{ item.name }}</span>
                <Badge v-if="item.domain" variant="secondary" class="text-xs">{{ item.domain }}</Badge>
            </slot>
        </template>
        
        <!-- Slot pour customiser l'affichage dans la liste -->
        <template #list-item="{ item }">
            <slot name="list-item" :item="item">
                <div class="flex items-center gap-2 w-full">
                    <Avatar class="h-6 w-6 rounded-md">
                        <AvatarImage v-if="item.logo" :src="`/storage/download/${item.logo}`" v-fetcher-src.lazy />
                        <AvatarFallback class="rounded-md text-xs">
                            <Building class="h-3 w-3" />
                        </AvatarFallback>
                    </Avatar>
                    <div class="flex flex-col items-start min-w-0 flex-1">
                        <span class="font-medium text-sm truncate">{{ item.name }}</span>
                        <span v-if="item.domain" class="text-xs text-muted-foreground truncate">
                            {{ item.domain }}
                        </span>
                    </div>
                </div>
            </slot>
        </template>
    </RelationSelect>
</template>

<script setup>
import { computed } from 'vue'
import { Building } from 'lucide-vue-next'
import { RelationSelect } from '@/common/components/ui/relation-select'
import { Avatar, AvatarImage, AvatarFallback } from '@/common/components/ui/avatar'
import { Badge } from '@/common/components/ui/badge'

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
