<template>
  <div class="flex items-center gap-2">
    <Select v-model="ruleField">
      <SelectTrigger class="w-48 bg-white">
        <SelectValue placeholder="Champ" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem v-for="field in availableFields" :key="field.name" :value="field.name">
          {{ field.label }}
        </SelectItem>
      </SelectContent>
    </Select>

    <Select v-model="ruleOperator" :disabled="!ruleField">
      <SelectTrigger class="w-32 bg-white">
        <SelectValue placeholder="Opérateur" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem v-for="operator in ruleFieldOperators" :key="operator" :value="operator">
          {{ FILTER_OPERATORS[operator] }}
        </SelectItem>
      </SelectContent>
    </Select>

    <template v-if="!ruleValueDisplay">
      <div class="flex-1"></div>
    </template>

    <template v-if="ruleValueDisplay">
      <Select v-if="ruleFieldType === 'boolean'" v-model="ruleValue">
        <SelectTrigger class="w-24 bg-white">
          <SelectValue placeholder="Valeur" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem :value="true">Oui</SelectItem>
          <SelectItem :value="false">Non</SelectItem>
        </SelectContent>
      </Select>

      <Input v-else-if="ruleFieldType === 'date' || ruleFieldType === 'datetime'" v-model="ruleValue"
        :placeholder="ruleFieldType === 'date' ? 'YYYY-MM-DD' : 'YYYY-MM-DD HH:MM:SS'" type="text" class="w-48" />

      <Input v-else-if="ruleFieldType === 'integer'" v-model="ruleValue" placeholder="Valeur" type="number"
        class="w-32 bg-white" />

      <Input v-else-if="ruleFieldType === 'float'" v-model="ruleValue" placeholder="Valeur" type="number" step="0.01"
        class="w-32 bg-white" />

      <Input v-else v-model="ruleValue" placeholder="Valeur" type="text" class="w-48 bg-white" />
    </template>

    <Button size="icon" variant="ghost" @click="$emit('delete')" class="h-9 w-9">
      <MinusCircle class="h-4 w-4" />
    </Button>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { MinusCircle } from 'lucide-vue-next'
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { useMetadataStore } from '@/common/stores/metadata'
import { FILTER_OPERATORS, NO_VALUE_FILTERS } from "@/common/composables/filters"

const metadataStore = useMetadataStore()

const props = defineProps({
  modelName: {
    type: String,
    required: true,
  },
  modelValue: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits([
  'update:modelValue',
  'delete',
])

const metadata = ref(null)

const availableFields = computed(() => {
  return Object.entries(metadata.value?.fields || {})
    .filter(([_, field]) => field.searchable === true)
    .map(([name, field]) => ({
      name,
      label: field.label || name
    }))
})

const ruleField = computed({
  get: () => props.modelValue.length > 0 ? props.modelValue[0] : '',
  set: (value) => {
    props.modelValue[0] = value || ''
  },
})

const ruleFieldMetadata = computed(() => {
  return metadata.value?.fields?.[ruleField.value] || null
})

const ruleFieldType = computed(() => {
  return ruleFieldMetadata.value?.type || null
})

const ruleFieldOperators = computed(() => {
  return (ruleFieldMetadata.value?.filter_operators || []).filter((operator) => FILTER_OPERATORS[operator])
})

const ruleOperator = computed({
  get: () => props.modelValue.length > 1 ? props.modelValue[1] : '',
  set: (value) => {
    props.modelValue[1] = value || ''
  },
})

const ruleValueDisplay = computed(() => {
  return ruleField && ruleOperator && !NO_VALUE_FILTERS.includes(ruleOperator.value)
})

const ruleValue = computed({
  get: () => props.modelValue.length > 2 ? props.modelValue[2] : null,
  set: (value) => {
    if (value) {
      props.modelValue[2] = value
    } else {
      if (props.modelValue.length > 2) {
        props.modelValue.splice(2, 1)
      }
    }
  },
})

watch(ruleField, async () => {
  ruleOperator.value = ruleFieldOperators.value?.[0] || ''
})

watch(ruleOperator, async () => {
  ruleValue.value = null
})

async function initialize() {
  if (!metadata.value) {
    metadata.value = await metadataStore.getMetadata(props.modelName)
  }

  if (!ruleField.value) {
    ruleField.value = availableFields.value?.[0]?.name || ''
  }
}

onMounted(async () => {
  await initialize()
})
</script>
