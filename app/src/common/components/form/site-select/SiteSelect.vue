<template>
    <RelationSelect v-model="selectedValue" :endpoint="endpoint" :display-field="displayField"
        :placeholder="placeholder" :class="className" :disabled="disabled" :params="siteParams"
        :empty-message="emptyMessage" @update:model-value="handleChange">
        <template #empty-action>
            <Button v-if="!disableCreate" variant="outline" size="sm" class="w-full mt-2" @click="openSiteDialog">
                <Plus class="h-4 w-4 mr-2" />
                Créer un site
            </Button>
        </template>
    </RelationSelect>
</template>

<script setup>
import RelationSelect from '@/common/components/form/relation-select/RelationSelect.vue'
import Button from '@/common/components/ui/button/Button.vue'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { Plus } from 'lucide-vue-next'
import { computed, ref, watch } from 'vue'

const props = defineProps({
    modelValue: {
        type: [Number, String, null],
        default: null
    },
    placeholder: {
        type: String,
        default: 'Sélectionner un site'
    },
    className: {
        type: String,
        default: ''
    },
    disabled: {
        type: Boolean,
        default: false
    },
    companyId: {
        type: [Number, null],
        default: null
    },
    contactId: {
        type: [Number, null],
        default: null
    },
    disableCreate: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['update:model-value'])

const endpoint = '/sites'
const displayField = 'name'
const fetcher = useFetcher()
const hasSites = ref(true)

const selectedValue = computed({
    get() {
        console.log('SiteSelect - get selectedValue:', props.modelValue)
        return props.modelValue
    },
    set(value) {
        console.log('SiteSelect - set selectedValue:', value)
        emit('update:model-value', value)
    }
})

const siteParams = computed(() => {
    const params = {}
    if (props.companyId) {
        params.company = props.companyId
    } else if (props.contactId) {
        params.contact = props.contactId
    }

    console.log('SiteSelect - Props reçues:', {
        companyId: props.companyId,
        contactId: props.contactId,
        params: params
    })

    return params
})

const emptyMessage = computed(() => {
    if (props.disableCreate) {
        return 'Aucun site trouvé'
    }
    return 'Aucun site trouvé'
})

const handleChange = (value) => {
    emit('update:model-value', value)
}

const openSiteDialog = () => {
    const data = {}

    // Déterminer le type d'attachement
    if (props.companyId) {
        data.attachmentType = 'company'
        data.company = props.companyId
    } else if (props.contactId) {
        data.attachmentType = 'contact'
        data.contact = props.contactId
    } else {
        data.attachmentType = 'none'
    }

    bus.trigger('open-site-dialog', data)
}

// Vérifier s'il y a des sites disponibles
const checkSitesAvailability = async () => {
    try {
        const params = { ...siteParams.value, limit: 1 }
        const response = await fetcher.get(endpoint, { params })
        const sites = response.data?.items || response.data?.results || response.data || []
        hasSites.value = sites.length > 0
    } catch (error) {
        console.error('Erreur lors de la vérification des sites:', error)
        hasSites.value = false
    }
}

// Vérifier les sites quand les paramètres changent
watch(() => siteParams.value, () => {
    checkSitesAvailability()
}, { immediate: true })

// Écouter la création d'un nouveau site
useBus(bus, 'site-saved', (siteData) => {
    // Si un site vient d'être créé, le sélectionner automatiquement
    if (siteData && siteData.id) {
        // Vérifier que le site correspond aux filtres actuels
        const isCompatible = (
            (props.companyId && siteData.company === props.companyId) ||
            (props.contactId && siteData.contact === props.contactId) ||
            (!props.companyId && !props.contactId)
        )

        if (isCompatible) {
            emit('update:model-value', siteData.id)
        }
    }

    checkSitesAvailability()
})
</script>