<template>
  <div>
    <Popover v-model:open="menu">
      <PopoverTrigger as-child>
        <Button variant="outline" class="relative h-8">
          <Filter class="w-4 h-4"/>
          Filtres
          <Badge v-if="activeFiltersCount > 0" variant="secondary" class="h-5 min-w-5 text-xs">
            {{ activeFiltersCount }}
          </Badge>
        </Button>
      </PopoverTrigger>

      <PopoverContent class="w-[800px]" align="start">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-semibold">Filtres</h3>
          <Button variant="ghost" size="icon" @click="cancelFilters" class="h-8 w-8">
            <X class="h-5 w-5" />
          </Button>
        </div>

        <div class="bg-accent rounded-md p-4 mt-2">
          <QueryBuilder
            v-model="editedFilters"
            :modelName="props.modelName"
          />
        </div>

        <div class="flex justify-end gap-2 pt-3 ">
          <Button variant="outline" @click="cancelFilters">
            Annuler
          </Button>
          <Button @click="applyFilters">
            Appliquer
          </Button>
        </div>
      </PopoverContent>
    </Popover>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { cloneDeep } from 'lodash'
import { Filter, X } from 'lucide-vue-next'
import { Button } from '@/common/components/ui/button'
import { Badge } from '@/common/components/ui/badge'
import { Popover, PopoverTrigger, PopoverContent } from '@/common/components/ui/popover'
import QueryBuilder from '@/common/components/controlPanel/filters/QueryBuilder.vue'
import { useFilters } from '@/common/composables/filters'

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

const menu = ref(false)
const editedFilters = ref(null)
const filterManager = useFilters()

const activeFiltersCount = computed(() => {
  return countActiveFilters(filterManager.normalize(props.modelValue))
})

const hasActiveFilters = computed(() => activeFiltersCount.value > 0)

watch(() => menu.value, (val) => {
  if (val) {
    editedFilters.value = props.modelValue ? cloneDeep(props.modelValue) : filterManager.createRule()
  }
})

function countActiveFilters(filters) {
  if (!filters) {
    return 0
  }

  if (filterManager.isCondition(filters)) {
    return filters[1].reduce((count, subFilter) => {
      return count + countActiveFilters(subFilter)
    }, 0)
  } else if (filterManager.isRule(filters)) {
    return 1
  }

  return 0
}

function applyFilters() {
  emit('update:modelValue', editedFilters.value)
  menu.value = false
}

function cancelFilters() {
  menu.value = false
  editedFilters.value = null
}
</script>
