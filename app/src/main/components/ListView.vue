<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="kpis && kpis.length > 0 ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">{{ config.title }}</h1>
                    <p class="text-neutral-600">{{ config.subtitle }}</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button v-if="config.enableExport" variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button v-if="config.enableCreate" @click="$emit('create')">
                        <Plus class="h-4 w-4" />
                        {{ config.createButtonText }}
                    </Button>
                </div>
            </div>

            <div v-if="kpis && kpis.length > 0" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div v-for="kpi in kpis" :key="kpi.key" class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <component :is="kpi.icon" class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">{{ kpi.label }}</p>
                        <p class="text-lg font-semibold text-neutral-900">{{ kpi.value }}</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div v-if="filterFields && filterFields.length > 0" :class="[
                'bg-neutral-50 border-r overflow-y-auto',
                showFilters ? 'w-64 p-4' : 'w-16 p-2 pt-4 cursor-pointer hover:bg-neutral-100'
            ]" @click="!showFilters && toggleFilters()">

                <div v-if="showFilters" class="flex items-center justify-between mb-4">
                    <h3 class="font-semibold text-neutral-900">Filtres</h3>
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0 cursor-pointer" @click.stop="toggleFilters">
                        <PanelLeftClose class="h-4 w-4" />
                    </Button>
                </div>

                <div v-else class="flex flex-col items-center mb-4">
                    <Button variant="ghost" size="sm" class="h-6 w-6 p-0 mb-2 cursor-pointer"
                        @click.stop="toggleFilters">
                        <PanelLeftOpen class="h-4 w-4" />
                    </Button>
                    <h3 class="font-semibold text-neutral-900 transform -rotate-90 origin-center mt-4">
                        Filtres
                    </h3>
                </div>

                <div v-show="showFilters" class="space-y-6">
                    <div v-for="filter in filterFields" :key="filter.key" class="mb-6">
                        <h4 class="text-sm font-medium text-neutral-700 mb-2">{{ filter.label }}</h4>
                        <div class="space-y-2">
                            <label v-for="option in filter.options" :key="option.value" class="flex items-center">
                                <Checkbox :checked="selectedFilters[filter.key]?.includes(option.value) || false"
                                    @update:checked="toggleFilter(filter.key, option.value)" />
                                <span class="ml-2 text-sm text-neutral-600">{{ option.label }}</span>
                                <span v-if="option.count" class="ml-auto text-xs text-neutral-400">{{ option.count
                                }}</span>
                            </label>
                        </div>
                    </div>

                    <Button variant="outline" size="sm" class="w-full" @click="resetFilters">
                        <RotateCcw class="h-4 w-4 mr-2" />
                        Réinitialiser
                    </Button>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto pb-16">
                <div class="px-6 py-4 border-b">
                    <div class="flex items-center justify-between">
                        <div v-if="searchFields" class="relative">
                            <Search
                                class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                            <Input type="text" :placeholder="config.searchPlaceholder || 'Recherche rapide...'"
                                class="h-9 pl-10 pr-4 py-2 w-64" v-model="searchQuery"
                                @input="$emit('search', searchQuery)" />
                        </div>
                        <div v-else></div>

                        <div class="flex items-center space-x-3">
                            <span class="text-sm text-muted-foreground">{{ totalItems }} {{ config.itemsLabel }}</span>
                            <Button variant="outline" size="sm" class="w-8">
                                <MoreVertical class="h-4 w-4" />
                            </Button>
                            <DropdownMenu>
                                <DropdownMenuTrigger as-child>
                                    <Button variant="outline">
                                        <Columns class="h-4 w-4" />
                                        Colonnes
                                        <ChevronDown class="h-4 w-4" />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end" class="w-56">
                                    <DropdownMenuLabel>Afficher les colonnes</DropdownMenuLabel>
                                    <DropdownMenuSeparator />
                                    <DropdownMenuCheckboxItem v-for="column in hideableColumns" :key="column.key"
                                        v-model:model-value="visibleColumns[column.key]">
                                        {{ column.label }}
                                    </DropdownMenuCheckboxItem>
                                </DropdownMenuContent>
                            </DropdownMenu>
                        </div>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full">
                        <thead class="bg-neutral-50 border-b">
                            <tr>
                                <th v-if="config.enableSelection"
                                    class="px-3 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-5">
                                    <Checkbox :checked="allSelected" @update:checked="toggleSelectAll" />
                                </th>
                                <th v-for="column in visibleColumnsArray" :key="column.key"
                                    class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                    {{ column.label }}
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-neutral-200">
                            <tr v-if="!loading && items.length === 0">
                                <td :colspan="visibleColumnsArray.length + (config.enableSelection ? 1 : 0)"
                                    class="px-6 py-12 text-center">
                                    <slot name="empty-state">
                                        <div class="text-neutral-500">
                                            <p class="text-lg font-medium">Aucun élément trouvé</p>
                                            <p class="text-sm">Il n'y a aucun élément à afficher pour le moment.</p>
                                        </div>
                                    </slot>
                                </td>
                            </tr>
                            <tr v-else-if="loading" class="hover:bg-neutral-50">
                                <td :colspan="visibleColumnsArray.length + (config.enableSelection ? 1 : 0)"
                                    class="px-6 py-12 text-center">
                                    <div class="flex items-center justify-center">
                                        <div
                                            class="w-7 h-7 border-[3px] border-neutral-200 border-t-neutral-900 rounded-full animate-spin">
                                        </div>
                                    </div>
                                </td>
                            </tr>
                            <ContextMenu v-else v-for="item in items" :key="item.id">
                                <ContextMenuTrigger as-child>
                                    <tr class="hover:bg-neutral-50">

                                        <td v-if="config.enableSelection" class="px-3 py-2 whitespace-nowrap max-w-5"
                                            @click.stop>
                                            <Checkbox :checked="selectedItems.includes(item.id)"
                                                @update:checked="toggleSelectItem(item.id)" />
                                        </td>

                                        <td v-for="column in visibleColumnsArray" :key="column.key"
                                            class="px-6 py-2 whitespace-nowrap">

                                            <component v-if="column.component" :is="column.component"
                                                v-bind="column.componentProps" :item="item"
                                                :value="getColumnValue(item, column)" />

                                            <Badge v-else-if="column.type === 'badge'"
                                                :variant="getColumnVariant(item, column)">
                                                {{ getColumnValue(item, column) }}
                                            </Badge>

                                            <span v-else-if="column.type === 'status'"
                                                :class="getColumnStatusClasses(item, column)">
                                                {{ getColumnValue(item, column) }}
                                            </span>

                                            <div v-else class="text-sm" :class="column.classes">
                                                {{ getColumnValue(item, column) }}
                                            </div>
                                        </td>
                                    </tr>
                                </ContextMenuTrigger>
                                <ContextMenuContent v-if="contextMenuActions && contextMenuActions.length > 0">
                                    <ContextMenuItem v-for="action in contextMenuActions" :key="action.key"
                                        @click="$emit('context-menu-action', action.key, item)" :class="action.class">
                                        <component v-if="action.icon" :is="action.icon" class="w-4 h-4 mr-2" />
                                        {{ action.label }}
                                    </ContextMenuItem>
                                </ContextMenuContent>
                            </ContextMenu>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <TablePagination :current-page="currentPage" :total-pages="totalPages" :total-items="totalItems"
            :items-per-page="itemsPerPage" :position-classes="`bottom-0 ${getFilterPanelClass()} right-0`"
            @page-change="$emit('page-change', $event)"
            @items-per-page-change="$emit('items-per-page-change', $event)" />
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import {
    ContextMenu,
    ContextMenuContent,
    ContextMenuItem,
    ContextMenuTrigger
} from '@/common/components/ui/context-menu'
import {
    DropdownMenu,
    DropdownMenuCheckboxItem,
    DropdownMenuContent,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger
} from '@/common/components/ui/dropdown-menu'
import Input from '@/common/components/ui/input/Input.vue'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    ChevronDown,
    Columns,
    Download,
    MoreVertical,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    RotateCcw,
    Search
} from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'

const props = defineProps({
    config: {
        type: Object,
        required: true
    },
    columns: {
        type: Array,
        required: true
    },
    items: {
        type: Array,
        default: () => []
    },
    filterFields: {
        type: Array,
        default: () => []
    },
    searchFields: {
        type: String,
        default: null
    },
    kpis: {
        type: Array,
        default: () => []
    },
    currentPage: {
        type: Number,
        default: 1
    },
    totalPages: {
        type: Number,
        default: 1
    },
    totalItems: {
        type: Number,
        default: 0
    },
    itemsPerPage: {
        type: Number,
        default: 20
    },
    loading: {
        type: Boolean,
        default: false
    },
    contextMenuActions: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits([
    'create',
    'row-click',
    'search',
    'page-change',
    'items-per-page-change',
    'filter-change',
    'selection-change',
    'context-menu-action'
])

const showFilters = ref(true)
const searchQuery = ref('')
const selectedFilters = ref({})
const selectedItems = ref([])
const visibleColumns = ref({})

const toggleFilters = () => {
    showFilters.value = !showFilters.value
}

const allSelected = computed(() => {
    return props.items.length > 0 && selectedItems.value.length === props.items.length
})

const hideableColumns = computed(() => {
    return props.columns.filter(column => column.hideable !== false)
})

const visibleColumnsArray = computed(() => {
    return props.columns.filter(column => {
        // Les colonnes non masquables sont toujours visibles
        if (column.hideable === false) return true
        // Les colonnes masquables dépendent de l'état visibleColumns
        return visibleColumns.value[column.key] !== false
    })
})

const toggleSelectAll = (checked) => {
    if (checked) {
        selectedItems.value = props.items.map(item => item.id)
    } else {
        selectedItems.value = []
    }
    emit('selection-change', selectedItems.value)
}

const toggleSelectItem = (itemId) => {
    const index = selectedItems.value.indexOf(itemId)
    if (index > -1) {
        selectedItems.value.splice(index, 1)
    } else {
        selectedItems.value.push(itemId)
    }
    emit('selection-change', selectedItems.value)
}

const toggleFilter = (filterKey, value) => {
    if (!selectedFilters.value[filterKey]) {
        selectedFilters.value[filterKey] = []
    }

    const index = selectedFilters.value[filterKey].indexOf(value)
    if (index > -1) {
        selectedFilters.value[filterKey].splice(index, 1)
    } else {
        selectedFilters.value[filterKey].push(value)
    }

    emit('filter-change', selectedFilters.value)
}

const resetFilters = () => {
    selectedFilters.value = {}
    emit('filter-change', selectedFilters.value)
}



const getColumnValue = (item, column) => {
    if (column.accessor) {
        return column.accessor(item)
    }

    const keys = column.key.split('.')
    let value = item
    for (const key of keys) {
        value = value?.[key]
    }
    return value
}

const getColumnVariant = (item, column) => {
    if (column.variantAccessor) {
        return column.variantAccessor(item)
    }
    return column.variant || 'outline'
}

const getColumnStatusClasses = (item, column) => {
    if (column.classAccessor) {
        return column.classAccessor(item)
    }
    return column.classes || ''
}

const getFilterPanelClass = () => {
    if (!props.filterFields || props.filterFields.length === 0) {
        return 'left-0'
    }
    return showFilters.value ? 'left-80' : 'left-32'
}

watch(selectedFilters, () => {
    emit('filter-change', selectedFilters.value)
}, { deep: true })

// Initialiser toutes les colonnes masquables comme visibles par défaut
watch(() => props.columns, (newColumns) => {
    if (newColumns) {
        const newVisibleColumns = { ...visibleColumns.value }
        newColumns.forEach(column => {
            // N'initialiser que les colonnes masquables
            if (column.hideable !== false && newVisibleColumns[column.key] === undefined) {
                newVisibleColumns[column.key] = true
            }
        })
        visibleColumns.value = newVisibleColumns
    }
}, { immediate: true })
</script>