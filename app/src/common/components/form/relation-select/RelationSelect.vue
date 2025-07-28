<template>
    <Popover v-model:open="open">
        <PopoverTrigger as-child>
            <Button variant="outline" role="combobox" :aria-expanded="open" class="w-full flex-1 justify-between"
                :class="triggerClass" :disabled="disabled">
                <div v-if="selectedItem" class="flex items-center gap-2 truncate">
                    <slot name="selected-item" :item="selectedItem">
                        <Avatar v-if="imageField && selectedItem[imageField]" class="h-4 w-4 rounded-md">
                            <AvatarImage :src="getImageUrl(selectedItem[imageField])" v-fetcher-src.lazy />
                            <AvatarFallback class="text-xs rounded-md">
                                {{ selectedItem[displayField]?.charAt(0) || '?' }}
                            </AvatarFallback>
                        </Avatar>
                        <span class="truncate">{{ selectedItem[displayField] || 'Sans nom' }}</span>
                    </slot>
                </div>
                <span v-else class="text-muted-foreground">
                    {{ placeholder }}
                </span>
                <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
            </Button>
        </PopoverTrigger>
        <PopoverContent class="w-[300px] p-0">
            <Command>
                <CommandInput :placeholder="searchPlaceholder" v-model="searchQuery"
                    @update:model-value="onSearchChange" />
                <CommandEmpty>{{ emptyMessage }}</CommandEmpty>
                <CommandList>
                    <CommandGroup>
                        <CommandItem v-if="clearable && selectedItem" :value="'clear'" @click="clearSelection"
                            class="h-auto cursor-pointer py-2 text-muted-foreground">
                            <div class="flex items-center gap-2 w-full">
                                <X class="h-4 w-4" />
                                <span class="text-sm">Effacer la sélection</span>
                            </div>
                        </CommandItem>
                        <CommandItem v-for="item in items" :key="item.id" :value="item.id"
                            @click="() => selectItem(item)" class="h-auto cursor-pointer py-2">
                            <slot name="list-item" :item="item">
                                <div class="flex items-center gap-2 w-full">
                                    <Avatar v-if="imageField && item[imageField]" class="h-6 w-6 rounded-md">
                                        <AvatarImage :src="getImageUrl(item[imageField])" v-fetcher-src.lazy />
                                        <AvatarFallback class="rounded-md text-xs">
                                            {{ item[displayField]?.charAt(0) || '?' }}
                                        </AvatarFallback>
                                    </Avatar>
                                    <div class="flex flex-col items-start min-w-0 flex-1">
                                        <span class="font-medium text-sm truncate">{{ item[displayField] || 'Sans nom'
                                            }}</span>
                                        <span v-if="subtitleField && item[subtitleField]"
                                            class="text-xs text-muted-foreground truncate">
                                            {{ item[subtitleField] }}
                                        </span>
                                    </div>
                                </div>
                            </slot>
                        </CommandItem>
                    </CommandGroup>
                </CommandList>
            </Command>
        </PopoverContent>
    </Popover>
</template>

<script setup>
import { useFetcher } from '@/common/composables/fetcher'
import { debounce } from 'lodash'
import { ChevronsUpDown, X } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Button } from '@/common/components/ui/button'
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from '@/common/components/ui/command'
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/common/components/ui/popover'

defineOptions({
    name: 'RelationSelect'
})

const props = defineProps({
    modelValue: {
        type: [String, Number, Object],
        default: null
    },
    // Configuration de l'endpoint
    endpoint: {
        type: String,
        required: true
    },
    // Champ à afficher comme texte principal
    displayField: {
        type: String,
        default: 'name'
    },
    // Champ image (optionnel)
    imageField: {
        type: String,
        default: null
    },
    // Champ sous-titre (optionnel)
    subtitleField: {
        type: String,
        default: null
    },
    // Champs supplémentaires à récupérer dans les requests
    extraFields: {
        type: Array,
        default: () => []
    },
    // Paramètre de recherche dans l'API
    searchParam: {
        type: String,
        default: null
    },
    // Interface utilisateur
    placeholder: {
        type: String,
        default: 'Sélectionner...'
    },
    searchPlaceholder: {
        type: String,
        default: 'Rechercher...'
    },
    emptyMessage: {
        type: String,
        default: 'Aucun résultat trouvé.'
    },
    triggerClass: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    },
    // Paramètres de recherche
    minSearchLength: {
        type: Number,
        default: 1
    },
    limit: {
        type: Number,
        default: 50
    },
    defaultLimit: {
        type: Number,
        default: 10
    },
    clearable: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:modelValue', 'select'])

const fetcher = useFetcher()
const open = ref(false)
const searchQuery = ref('')
const items = ref([])
const loading = ref(false)

const selectedItemCache = ref(null)

const selectedItem = computed(() => {
    if (!props.modelValue) return null

    if (typeof props.modelValue === 'object') {
        return props.modelValue
    }

    const foundInList = items.value.find(item => item.id === props.modelValue)
    if (foundInList) {
        return foundInList
    }

    if (selectedItemCache.value && selectedItemCache.value.id === props.modelValue) {
        return selectedItemCache.value
    }

    return null
})

const getImageUrl = (imagePath) => {
    if (!imagePath) return ''
    if (imagePath.startsWith('http')) return imagePath
    return `/storage/download/${imagePath}`
}

const fetchSelectedItem = async (itemId) => {
    if (!itemId || typeof itemId !== 'number') return

    try {
        const { data } = await fetcher.get(`${props.endpoint}/${itemId}`)
        selectedItemCache.value = data
    } catch (error) {
        console.error('Erreur lors du chargement de l\'item sélectionné:', error)
        selectedItemCache.value = null
    }
}

const fetchItems = async (search = '') => {
    if (search && search.length < props.minSearchLength) {
        return
    }

    try {
        const fields = ['id', props.displayField]

        if (props.imageField) {
            fields.push(props.imageField)
        }

        if (props.subtitleField) {
            fields.push(props.subtitleField)
        }

        if (props.extraFields.length > 0) {
            fields.push(...props.extraFields)
        }

        loading.value = true
        const params = {}
        const headers = {
            'X-Fields': fields.join(','),
        }

        if (search) {
            params.limit = props.limit.toString()

            if (props.searchParam) {
                params[props.searchParam] = search
            } else {
                headers['X-Filter'] = JSON.stringify([props.displayField, 'icontains', search])
            }
        } else {
            params.limit = props.defaultLimit.toString()
        }

        const { data } = await fetcher.get(props.endpoint, {
            headers,
            params,
        })
        items.value = data.items || data.results || data || []

        if (props.modelValue && typeof props.modelValue === 'object') {
            const exists = items.value.find(item => item.id === props.modelValue.id)
            if (!exists) {
                items.value.unshift(props.modelValue)
            }
        }
    } catch (error) {
        console.error('Erreur lors du chargement:', error)
        items.value = []
    } finally {
        loading.value = false
    }
}

const debouncedFetchItems = debounce((query) => {
    fetchItems(query).then()
}, 0)

const onSearchChange = (query) => {
    searchQuery.value = query
    debouncedFetchItems(query)
}

const selectItem = (item) => {
    emit('update:modelValue', item)
    emit('select', item)
    open.value = false
}

const clearSelection = () => {
    emit('update:modelValue', null)
    emit('select', null)
    open.value = false
}

onMounted(() => {
    fetchItems().then()
})

watch(() => props.modelValue, (newValue) => {
    if (newValue && typeof newValue === 'number') {
        const foundInList = items.value.find(item => item.id === newValue)
        const foundInCache = selectedItemCache.value && selectedItemCache.value.id === newValue

        if (!foundInList && !foundInCache) {
            fetchSelectedItem(newValue)
        }
    } else if (!newValue) {
        selectedItemCache.value = null
    } else if (newValue && typeof newValue === 'object') {
        const exists = items.value.find(item => item.id === newValue.id)
        if (!exists) {
            items.value.unshift(newValue)
        }
    }
}, { immediate: true })

watch(open, (newOpen) => {
    if (newOpen && items.value.length === 0) {
        fetchItems()
    }
})
</script>
