<template>
    <div>
        <QueryBuilderCondition
            v-if="filterManager.isCondition(normalizedFilters)"
            :modelName="props.modelName"
            v-model="normalizedFilters"
        />

        <QueryBuilderRule
            v-else-if="filterManager.isRule(normalizedFilters)"
            :modelName="props.modelName"
            v-model="normalizedFilters"
            @delete="clearAllFilters"
        />

        <div v-else class="text-center py-4">
      <span class="text-muted-foreground">Aucun filtre</span>
        </div>

    <div class="flex items-center gap-2 mt-4">
      <Button size="sm" variant="outline" @click="addFilter">
        <Plus class="w-4 h-4 mr-1" />
                Ajouter filtre
      </Button>

      <div class="flex-1"></div>

      <Button size="sm" variant="outline" @click="clearAllFilters">
        <Trash2 class="w-4 h-4 mr-1 text-destructive" />
                Effacer tous les filtres
      </Button>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { Plus, Trash2 } from 'lucide-vue-next'
import { Button } from '@/common/components/ui/button'
import { useFilters } from '@/common/composables/filters'
import QueryBuilderRule from '@/common/components/controlPanel/filters/QueryBuilderRule.vue'
import QueryBuilderCondition from '@/common/components/controlPanel/filters/QueryBuilderCondition.vue'

const props = defineProps({
    modelName: {
        type: String,
        required: true,
    },
    modelValue: {
        type: [Array, null],
        required: false,
        default: () => null,
    },
})

const emit = defineEmits([
    'update:modelValue',
])

const filterManager = useFilters()
const normalizedFilters = ref(null)

watch(() => props.modelValue, (value) => {
  normalizedFilters.value = filterManager.normalize(value)
}, { immediate: true, deep: true })

function addFilter() {
    if (!normalizedFilters.value) {
    normalizedFilters.value = filterManager.createRule()
    emit('update:modelValue', normalizedFilters.value)
    return
    }

    if (filterManager.isCondition(normalizedFilters.value)) {
    const updatedCondition = [...normalizedFilters.value]
    updatedCondition[1] = [...updatedCondition[1], filterManager.createRule()]
    normalizedFilters.value = updatedCondition
    emit('update:modelValue', normalizedFilters.value)
    return
    }

    normalizedFilters.value = filterManager.createCondition('&', [
        normalizedFilters.value,
        filterManager.createRule(),
  ])
  emit('update:modelValue', normalizedFilters.value)
}

function clearAllFilters() {
  normalizedFilters.value = null
  emit('update:modelValue', null)
}
</script>
