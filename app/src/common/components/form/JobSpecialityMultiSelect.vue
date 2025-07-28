<template>
    <div class="w-full space-y-2">
        <div class="flex flex-wrap gap-2" v-if="selectedSpecialities.length">
            <div v-for="speciality in selectedSpecialities" :key="speciality.id" class="flex items-center gap-1">
                <Badge variant="outline" class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: speciality.color }"></div>
                    {{ speciality.name }}
                </Badge>
                <button type="button"
                    class="flex items-center justify-center w-4 h-4 rounded-full hover:bg-destructive/10 cursor-pointer"
                    @click="removeSpeciality(speciality)">
                    <X class="h-3 w-3 text-muted-foreground hover:text-destructive" />
                </button>
            </div>
        </div>

        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" class="h-5 !ps-1 !pe-2 !gap-0 cursor-pointer"
                    :disabled="availableToAdd.length === 0" style="font-size: 11px;">
                    <Plus class="h-4 w-4" />
                    Ajouter une spécialité
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" class="w-56">
                <DropdownMenuItem v-for="speciality in availableToAdd" :key="speciality.id"
                    @click="addSpeciality(speciality)" class="cursor-pointer">
                    <div class="flex items-center gap-2">
                        <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: speciality.color }"></div>
                        {{ speciality.name }}
                    </div>
                </DropdownMenuItem>
                <div v-if="availableToAdd.length === 0" class="px-2 py-1.5 text-sm text-muted-foreground">
                    Toutes les spécialités sont sélectionnées
                </div>
            </DropdownMenuContent>
        </DropdownMenu>
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import { Plus, X } from 'lucide-vue-next'
import { computed } from 'vue'

const props = defineProps({
    specialities: {
        type: Array,
        default: () => []
    },
    modelValue: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['update:modelValue'])

const selectedSpecialities = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const availableToAdd = computed(() => {
    const selectedIds = selectedSpecialities.value.map(s => s.id)
    return props.specialities.filter(speciality => !selectedIds.includes(speciality.id))
})

const addSpeciality = (speciality) => {
    const newValue = [...selectedSpecialities.value, speciality]
    emit('update:modelValue', newValue)
}

const removeSpeciality = (speciality) => {
    const newValue = selectedSpecialities.value.filter(s => s.id !== speciality.id)
    emit('update:modelValue', newValue)
}
</script>