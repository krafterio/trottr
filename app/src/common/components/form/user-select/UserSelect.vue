<template>
    <RelationSelect v-model="selectedValue" :endpoint="endpoint" :display-field="displayField"
        :placeholder="placeholder" :class="className" @update:model-value="handleChange" />
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
        default: 'Sélectionner un utilisateur'
    },
    className: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['update:model-value'])

const endpoint = '/users'
const displayField = 'name'

const selectedValue = computed({
    get() {
        return props.modelValue
    },
    set(value) {
        emit('update:model-value', value)
    }
})

const handleChange = (value) => {
    emit('update:model-value', value)
}
</script>