<template>
    <RelationSelect v-model="selectedValue" :endpoint="endpoint" :display-field="displayField"
        :placeholder="placeholder" :class="className" :disabled="disabled" :params="siteParams"
        @update:model-value="handleChange" />
</template>

<script setup>
import RelationSelect from '@/common/components/form/relation-select/RelationSelect.vue'
import { computed } from 'vue'

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
    }
})

const emit = defineEmits(['update:model-value'])

const endpoint = '/sites'
const displayField = 'name'

const selectedValue = computed({
    get() {
        return props.modelValue
    },
    set(value) {
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
    return params
})

const handleChange = (value) => {
    emit('update:model-value', value)
}
</script>