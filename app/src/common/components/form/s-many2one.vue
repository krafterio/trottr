<template>
  <div class="s-many2one" :class="{ 's-field-horizontal': horizontal }">
    <label v-if="label" class="s-many2one-label text-body-2 d-block">{{ label }}</label>
    <div :class="horizontal ? 'flex-grow-1' : ''">
      <v-autocomplete
        ref="autocompleteRef"
        :model-value="displayValue"
        @update:model-value="onSelect"
        :items="items"
        :item-title="displayField"
        :item-value="valueField"
        :loading="loading"
        :search="searchQuery"
        @update:search="onSearch"
        @focus="onFocus"
        @blur="onBlur"
        :placeholder="placeholder"
        :clearable="clearable"
        :disabled="disabled"
        :readonly="readonly"
        :class="horizontal ? 'bg-grey-lighten-4' : ''"
        density="compact"
        hide-details="auto"
        no-filter
        v-bind="fieldAttrs"
      >
        <template #no-data>
          <v-list-item>
            <v-list-item-title>
              {{ searchQuery ? 'Aucun résultat trouvé' : 'Tapez pour rechercher...' }}
            </v-list-item-title>
          </v-list-item>
        </template>
        
        <template #item="{ props: itemProps, item }">
          <v-list-item v-bind="itemProps">
            <template #title>
              <v-chip v-if="showAsChip && item.raw[colorField]" 
                :color="item.raw[colorField]" 
                variant="tonal" 
                size="small"
                class="font-weight-medium text-truncate">
                {{ getDisplayValue(item.raw) }}
              </v-chip>
              <span v-else class="text-truncate d-block">{{ getDisplayValue(item.raw) }}</span>
            </template>
            <template #subtitle v-if="subtitleField">
              <span class="text-caption text-truncate d-block">{{ item.raw[subtitleField] }}</span>
            </template>
          </v-list-item>
        </template>

        <template #selection="{ item }">
          <template v-if="!isFocused">
            <template v-if="showAsChip && selectedItemForDisplay && selectedItemForDisplay[colorField]">
              <v-chip 
                :color="selectedItemForDisplay[colorField]" 
                variant="tonal" 
                size="small"
                class="font-weight-medium text-truncate">
                {{ getDisplayValue(selectedItemForDisplay) }}
              </v-chip>
            </template>
            <span v-else-if="selectedItemForDisplay" class="text-truncate d-block">{{ getDisplayValue(selectedItemForDisplay) }}</span>
            <span v-else class="text-truncate d-block">{{ getDisplayValue(item.raw) }}</span>
          </template>
        </template>
      </v-autocomplete>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useAttrs } from 'vue'
import {useFetcher} from "@/common/composables/fetcher"

defineOptions({
  name: 's-many2one'
})

const props = defineProps({
  modelValue: {
    type: [String, Number, Object],
    default: null
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Rechercher...'
  },
  endpoint: {
    type: String,
    required: true
  },
  displayField: {
    type: String,
    default: 'name'
  },
  valueField: {
    type: String,
    default: 'id'
  },
  subtitleField: {
    type: String,
    default: ''
  },
  searchParam: {
    type: String,
    default: 'search'
  },
  minSearchLength: {
    type: Number,
    default: 2
  },
  clearable: {
    type: Boolean,
    default: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  preloadData: {
    type: Boolean,
    default: false
  },
  defaultLimit: {
    type: Number,
    default: 5
  },
  limit: {
    type: Number,
    default: 50
  },
  showAsChip: {
    type: Boolean,
    default: false
  },
  colorField: {
    type: String,
    default: 'color'
  },
  horizontal: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'select', 'clear'])

const fetcher = useFetcher();
const attrs = useAttrs()

const fieldAttrs = computed(() => {
  return {
    ...attrs,
    variant: 'solo-filled',
    flat: true,
  }
})

const autocompleteRef = ref(null)
const items = ref([])
const loading = ref(false)
const searchQuery = ref('')
const searchTimeout = ref(null)
const isFocused = ref(false)
const previousValue = ref(null)

const selectedItem = computed({
  get() {
    if (typeof props.modelValue === 'object' && props.modelValue !== null) {
      return props.modelValue[props.valueField]
    }
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})

const displayValue = computed({
  get() {
    if (isFocused.value) {
      return searchQuery.value
    }
    return selectedItem.value
  },
  set(value) {
    return value
  }
})

const selectedItemForDisplay = computed(() => {
  if (typeof props.modelValue === 'object' && props.modelValue !== null) {
    return props.modelValue
  }
  return items.value.find(item => item[props.valueField] === props.modelValue)
})

const getDisplayValue = (item) => {
  if (typeof props.displayField === 'function') {
    return props.displayField(item)
  }
  return item[props.displayField] || item.name || item.title || 'Sans nom'
}

const searchItems = async (query = '') => {
  if (query && query.length < props.minSearchLength) {
    return
  }

  loading.value = true
  
  try {
    const params = {
      limit: query ? props.limit : props.defaultLimit
    }
    
    if (query) {
      params[props.searchParam] = query
    }

    const response = await fetcher.get(props.endpoint, { params })
    items.value = response.data.results || response.data.items || response.data || []
    
    if (props.modelValue && typeof props.modelValue === 'object') {
      const currentItem = items.value.find(item => 
        item[props.valueField] === props.modelValue[props.valueField]
      )
      if (!currentItem) {
        items.value.unshift(props.modelValue)
      }
    }
  } catch (error) {
    console.error('Erreur lors de la recherche:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

const onSearch = (query) => {
  searchQuery.value = query
  
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  
  searchTimeout.value = setTimeout(() => {
    searchItems(query)
  }, 300)
}

const onSelect = (value) => {
  const selectedRecord = items.value.find(item => item[props.valueField] === value)
  
  if (selectedRecord) {
    emit('update:modelValue', selectedRecord)
    emit('select', selectedRecord)
    isFocused.value = false
    searchQuery.value = ''
    if (autocompleteRef.value) {
      autocompleteRef.value.blur()
    }
  } else if (value === null || value === undefined) {
    emit('update:modelValue', null)
    emit('clear')
    isFocused.value = false
    searchQuery.value = ''
    if (autocompleteRef.value) {
      autocompleteRef.value.blur()
    }
  }
}

watch(() => props.modelValue, async (newValue) => {
  if (newValue && typeof newValue === 'object') {
    const exists = items.value.find(item => 
      item[props.valueField] === newValue[props.valueField]
    )
    if (!exists) {
      items.value.unshift(newValue)
    }
  } else if (newValue && items.value.length === 0) {
    await searchItems()
  }
}, { immediate: true })

const onFocus = async () => {
  isFocused.value = true
  previousValue.value = props.modelValue
  searchQuery.value = ''
  await loadDefaultItems()
}

const onBlur = () => {
  isFocused.value = false
  searchQuery.value = ''
}

const loadDefaultItems = () => {
  if (!props.modelValue) {
    searchItems()
  }
}

onMounted(async () => {
  if (props.preloadData || props.modelValue) {
    await searchItems()
  } else if (props.modelValue && typeof props.modelValue === 'object') {
    items.value = [props.modelValue]
  }
})
</script>

<style scoped>
.s-many2one {
  margin-bottom: 16px;
}
</style>
