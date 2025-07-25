<template>
    <v-menu v-model="isMenuOpen" location="bottom start" :close-on-content-click="false">
        <template #activator="{ props: menuProps }">
            <div v-bind="menuProps" @click="openMenu" class="d-flex align-center w-100">
                <span class="text-truncate">{{ displayValue || '-' }}</span>
            </div>
        </template>
        
        <v-card min-width="200" max-height="300" elevation="5">
            <v-text-field
                v-model="searchTerm"
                :placeholder="placeholder"
                density="compact"
                variant="outlined"
                hide-details
                class="ma-2"
                autofocus
                @input="handleSearch"
                @click.stop
            />
            <v-list density="compact" :loading="loading" style="max-height: 200px; overflow-y: auto;">
                <v-list-item 
                    v-for="item in filteredOptions" 
                    :key="item[valueField]"
                    @click="selectItem(item)"
                    :class="{ 'bg-primary-lighten-4': selectedValue === item[valueField] }">
                    <v-list-item-title>{{ item[displayField] }}</v-list-item-title>
                    <template #append v-if="selectedValue === item[valueField]">
                        <Check :size="16" class="text-success" />
                    </template>
                </v-list-item>
                <v-divider v-if="filteredOptions.length > 0 && selectedValue && allowClear" />
                <v-list-item v-if="selectedValue && allowClear" @click="clearSelection" class="text-error">
                    <v-list-item-title>{{ clearLabel }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-card>
    </v-menu>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { Check } from 'lucide-vue-next';
import { useFetcher } from '@/common/composables/fetcher';
import { debounce } from 'lodash';

const props = defineProps({
    modelValue: {
        type: [String, Number],
        default: null
    },
    displayValue: {
        type: String,
        default: ''
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
    placeholder: {
        type: String,
        default: 'Rechercher...'
    },
    allowClear: {
        type: Boolean,
        default: true
    },
    clearLabel: {
        type: String,
        default: 'Supprimer la sélection'
    },
    limit: {
        type: Number,
        default: 5
    }
});

const emit = defineEmits(['update:modelValue', 'select', 'clear']);

const fetcher = useFetcher();
const isMenuOpen = ref(false);
const searchTerm = ref('');
const options = ref([]);
const filteredOptions = ref([]);
const loading = ref(false);

const selectedValue = computed(() => props.modelValue);

const fetchOptions = async (search = '') => {
    try {
        loading.value = true;
        const params = {
            limit: props.limit
        };
        
        if (search) {
            params.search = search;
        }
        
        const { data } = await fetcher.get(props.endpoint, { params });
        options.value = data.items || [];
        filteredOptions.value = options.value;
    } catch (error) {
        console.error(`Erreur lors du chargement depuis ${props.endpoint}:`, error);
        options.value = [];
        filteredOptions.value = [];
    } finally {
        loading.value = false;
    }
};

const handleSearch = debounce(() => {
    if (searchTerm.value) {
        fetchOptions(searchTerm.value);
    } else {
        filteredOptions.value = options.value;
    }
}, 300);

const openMenu = async () => {
    searchTerm.value = '';
    await fetchOptions();
    isMenuOpen.value = true;
};

const selectItem = (item) => {
    const newValue = item[props.valueField];
    emit('update:modelValue', newValue);
    emit('select', item);
    closeMenu();
};

const clearSelection = () => {
    emit('update:modelValue', null);
    emit('clear');
    closeMenu();
};

const closeMenu = () => {
    isMenuOpen.value = false;
    searchTerm.value = '';
};
</script> 