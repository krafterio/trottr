<script setup>
import { ref, computed, watch } from 'vue'
import { ChevronsUpDown, Check, X } from 'lucide-vue-next'
import { debounce } from 'lodash'
import { useFetcher } from "@/common/composables/fetcher"
import {
  Combobox,
  ComboboxAnchor,
  ComboboxEmpty,
  ComboboxGroup,
  ComboboxItem,
  ComboboxItemIndicator,
  ComboboxList,
  ComboboxTrigger,
} from '@/common/components/ui/combobox'
import { ComboboxInput } from 'reka-ui'
import { cn } from '@/common/lib/utils'
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'

const props = defineProps({
  modelValue: { type: Object, default: null },
  endpoint: { type: String, required: true },
  displayField: { type: String, default: 'name' },
  valueField: { type: String, default: 'id' },
  imageField: { type: String, default: null },
  colorField: { type: String, default: null },
  searchParam: { type: String, default: 'q' },
  placeholder: { type: String, default: 'Rechercher...' },
  emptyText: { type: String, default: 'Aucun résultat trouvé.' },
  loadingText: { type: String, default: 'Recherche...' },
  minSearchLength: { type: Number, default: 2 },
  limit: { type: Number, default: 50 },
  by: { type: String, default: 'id' },
  allowClear: { type: Boolean, default: true },
  clearText: { type: String, default: 'Aucune sélection' },
  class: { type: null, required: false },
})

const emits = defineEmits(['update:modelValue', 'select'])

const fetcher = useFetcher()
const selectedItem = ref(props.modelValue)
const searchQuery = ref('')
const items = ref([])
const loading = ref(false)

// API de recherche
const searchItemsApi = async (query) => {
  if (!query || query.length < props.minSearchLength) {
    items.value = []
    loading.value = false
    return
  }

  try {
    const response = await fetcher.get(props.endpoint, {
      params: {
        [props.searchParam]: query,
        limit: props.limit
      }
    })
    items.value = response.data.items || []
  } catch (error) {
    console.error('Erreur lors de la recherche:', error)
    items.value = []
  } finally {
    loading.value = false
  }
}

const searchItems = debounce(searchItemsApi, 300)

// Gestionnaire de recherche
const handleSearch = (event) => {
  const query = event.target.value?.trim()
  searchQuery.value = query
  
  if (!query) {
    selectedItem.value = null
    items.value = []
    return
  }
  
  if (query.length >= props.minSearchLength) {
    loading.value = true
  }
  
  searchItems(query)
}

// Fonction d'affichage
const displayValue = (item) => {
  if (!item) return ''
  return typeof props.displayField === 'function' 
    ? props.displayField(item) 
    : item[props.displayField]
}

// Fonction pour obtenir l'image
const getImageUrl = (item) => {
  if (!props.imageField || !item) return null
  return item[props.imageField]
}

// Fonction pour obtenir la couleur
const getColor = (item) => {
  if (!props.colorField || !item) return null
  return item[props.colorField]
}

// Fonction pour obtenir les initiales
const getInitials = (item) => {
  if (!item) return '?'
  const name = displayValue(item)
  return name.split(' ').map(word => word.charAt(0).toUpperCase()).slice(0, 2).join('')
}

// Fonction pour vider la sélection
const clearSelection = () => {
  selectedItem.value = null
  searchQuery.value = ''
  items.value = []
}

// Watchers
watch(() => props.modelValue, (newValue) => {
  selectedItem.value = newValue
})

watch(selectedItem, (newValue) => {
  emits('update:modelValue', newValue)
  emits('select', newValue)
})
</script>

<template>
  <Combobox v-model="selectedItem" :by="by">
    <ComboboxAnchor class="w-full">
      <div class="relative w-full">
        <ComboboxInput 
          :display-value="displayValue"
          :placeholder="placeholder"
          @input="handleSearch"
          :class="cn(
            'file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input flex h-9 w-full min-w-0 rounded-md border bg-transparent py-1 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive',
            selectedItem && (imageField || colorField) ? 'pl-10' : 'px-3',
            props.class
          )"
        />
        
        <!-- Avatar/Image à gauche dans l'input -->
        <div v-if="selectedItem && (imageField || colorField)" class="absolute left-2 inset-y-0 flex items-center">
          <!-- Pastille colorée pour les statuts -->
          <div 
            v-if="colorField && getColor(selectedItem)"
            class="w-3 h-3 rounded-full" 
            :style="{ backgroundColor: getColor(selectedItem) }"
          ></div>
          <!-- Avatar pour les utilisateurs/contacts/sociétés -->
          <Avatar v-else-if="imageField" class="h-6 w-6">
            <AvatarImage :src="getImageUrl(selectedItem)" v-fetcher-src.lazy />
            <AvatarFallback class="text-xs">{{ getInitials(selectedItem) }}</AvatarFallback>
          </Avatar>
        </div>
        <button 
          v-if="selectedItem"
          @click="clearSelection"
          type="button"
          class="absolute end-8 inset-y-0 flex items-center justify-center px-1 hover:text-foreground text-muted-foreground"
        >
          <X class="size-4" />
        </button>
        <ComboboxTrigger class="absolute end-0 inset-y-0 flex items-center justify-center px-3">
          <ChevronsUpDown class="size-4 text-muted-foreground" />
        </ComboboxTrigger>
      </div>
    </ComboboxAnchor>

    <ComboboxList>
      <ComboboxEmpty>
        {{ loading ? loadingText : emptyText }}
      </ComboboxEmpty>

      <ComboboxGroup>
        <ComboboxItem v-if="allowClear" :value="null">
          <span class="text-muted-foreground">{{ clearText }}</span>
          <ComboboxItemIndicator>
            <Check class="ml-auto h-4 w-4" />
          </ComboboxItemIndicator>
        </ComboboxItem>
        
        <ComboboxItem 
          v-for="item in items" 
          :key="item[valueField]" 
          :value="item"
        >
          <div class="flex items-center gap-2">
            <!-- Pastille colorée -->
            <div 
              v-if="colorField && getColor(item)"
              class="w-3 h-3 rounded-full flex-shrink-0" 
              :style="{ backgroundColor: getColor(item) }"
            ></div>
            <!-- Avatar -->
            <Avatar v-else-if="imageField" class="h-6 w-6 flex-shrink-0">
              <AvatarImage :src="getImageUrl(item)" v-fetcher-src.lazy />
              <AvatarFallback class="text-xs">{{ getInitials(item) }}</AvatarFallback>
            </Avatar>
            <span>{{ displayValue(item) }}</span>
          </div>
          <ComboboxItemIndicator>
            <Check class="ml-auto h-4 w-4" />
          </ComboboxItemIndicator>
        </ComboboxItem>
      </ComboboxGroup>
    </ComboboxList>
  </Combobox>
</template> 