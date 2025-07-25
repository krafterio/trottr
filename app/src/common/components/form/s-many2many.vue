<template>
  <div class="s-many2many" :class="{ 's-field-horizontal': horizontal }">
    <label v-if="label" class="s-many2many-label text-body-2 d-block">{{ label }}</label>
    <div :class="horizontal ? 'flex-grow-1' : ''">
      <v-combobox
        ref="comboboxRef"
        :model-value="displayValues"
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
        multiple
        chips
        closable-chips="false"
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
                variant="flat" 
                size="small"
                class="font-weight-medium text-truncate dropdown-chip">
                {{ getDisplayValue(item.raw) }}
              </v-chip>
              <span v-else class="text-truncate d-block">{{ getDisplayValue(item.raw) }}</span>
            </template>
            <template #subtitle v-if="subtitleField">
              <span class="text-caption text-truncate d-block">{{ item.raw[subtitleField] }}</span>
            </template>
          </v-list-item>
        </template>

        <template #chip="{ props: chipProps, item }">
          <v-chip
            :color="item.raw?.[colorField] || 'primary'"
            variant="flat"
            size="small"
            class="font-weight-medium"
            closable
          >
            {{ item.raw?.[displayField] || item.title }}
          </v-chip>
        </template>


      </v-combobox>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useAttrs } from 'vue'
import {useFetcher} from "@/common/composables/fetcher"

defineOptions({
  name: 's-many2many'
})

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
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
  },
  maxChipsVisible: {
    type: Number,
    default: 3
  }
})

const emit = defineEmits(['update:modelValue', 'select', 'remove'])

const fetcher = useFetcher();
const attrs = useAttrs()

const fieldAttrs = computed(() => {
  return {
    ...attrs,
    variant: 'solo-filled',
    flat: true,
  }
})

const comboboxRef = ref(null)
const items = ref([])
const loading = ref(false)
const searchQuery = ref('')
const searchTimeout = ref(null)
const isFocused = ref(false)

const displayValues = computed(() => {
  if (!props.modelValue || props.modelValue.length === 0) {
    return []
  }
  
  return props.modelValue.map(value => {
    if (typeof value === 'object' && value !== null) {
      return value[props.valueField]
    }
    return value
  })
})

const getDisplayValue = (item) => {
  if (typeof props.displayField === 'function') {
    return props.displayField(item)
  }
  return item[props.displayField] || item.name || item.title || 'Sans nom'
}

const getItemFromValue = (value) => {
  if (typeof value === 'object' && value !== null) {
    return value
  }
  
  const foundInModelValue = props.modelValue.find(item => {
    if (typeof item === 'object' && item !== null) {
      return item[props.valueField] === value
    }
    return item === value
  })
  
  if (foundInModelValue && typeof foundInModelValue === 'object') {
    return foundInModelValue
  }
  
  return items.value.find(item => item[props.valueField] === value)
}

const getDisplayValueFromItem = (value) => {
  const item = getItemFromValue(value)
  if (item) {
    return getDisplayValue(item)
  }
  return value?.toString() || 'Inconnu'
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
    const newItems = response.data.results || response.data.items || response.data || []
    
    const existingIds = new Set(items.value.map(item => item[props.valueField]))
    const uniqueNewItems = newItems.filter(item => !existingIds.has(item[props.valueField]))
    
    items.value = [...items.value, ...uniqueNewItems]
    
    if (props.modelValue && props.modelValue.length > 0) {
      props.modelValue.forEach(value => {
        if (typeof value === 'object' && value !== null) {
          const exists = items.value.find(item => 
            item[props.valueField] === value[props.valueField]
          )
          if (!exists) {
            items.value.unshift(value)
          }
        }
      })
    }
  } catch (error) {
    console.error('Erreur lors de la recherche:', error)
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

const onSelect = (values) => {
  if (!Array.isArray(values)) {
    values = []
  }
  
  const selectedItems = values.map(value => {
    const item = items.value.find(item => item[props.valueField] === value)
    return item || value
  }).filter((item, index, self) => {
    if (typeof item === 'object' && item !== null) {
      return self.findIndex(i => 
        typeof i === 'object' && i !== null && i[props.valueField] === item[props.valueField]
      ) === index
    }
    return self.indexOf(item) === index
  })
  
  emit('update:modelValue', selectedItems)
  emit('select', selectedItems)
  
  searchQuery.value = ''
}

const removeItem = (valueToRemove) => {
  const currentValues = props.modelValue || []
  const filteredValues = currentValues.filter(value => {
    if (typeof value === 'object' && value !== null) {
      if (typeof valueToRemove === 'object' && valueToRemove !== null) {
        return value[props.valueField] !== valueToRemove[props.valueField]
      }
      return value[props.valueField] !== valueToRemove
    }
    return value !== valueToRemove
  })
  
  emit('update:modelValue', filteredValues)
  emit('remove', valueToRemove)
}

watch(() => props.modelValue, async (newValue) => {
  if (newValue && newValue.length > 0) {
    newValue.forEach(value => {
      if (typeof value === 'object' && value !== null) {
        const exists = items.value.find(item => 
          item[props.valueField] === value[props.valueField]
        )
        if (!exists) {
          items.value.unshift(value)
        }
      }
    })
  }
}, { immediate: true, deep: true })

const onFocus = async () => {
  isFocused.value = true
  searchQuery.value = ''
  await loadDefaultItems()
}

const onBlur = () => {
  isFocused.value = false
  searchQuery.value = ''
}

const loadDefaultItems = () => {
  if (!props.modelValue || props.modelValue.length === 0) {
    searchItems()
  }
}

onMounted(async () => {
  if (props.preloadData || (props.modelValue && props.modelValue.length > 0)) {
    await searchItems()
  }
})
</script>

<style scoped>
.s-many2many {
  margin-bottom: 16px;
}

.s-many2many :deep(.v-field__input) {
  flex-wrap: nowrap !important;
  overflow: hidden !important;
}

.s-many2many :deep(.v-field__field) {
  overflow: hidden !important;
}

.s-many2many :deep(.v-field__input > .v-chip) {
  flex-shrink: 0 !important;
}
</style> 