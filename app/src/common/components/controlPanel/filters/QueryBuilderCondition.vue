<template>
    <div class="query-builder-condition">
    <div class="flex items-center gap-2 mb-2">
      <Select v-model="conditionOperator">
        <SelectTrigger class="w-20">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          <SelectItem v-for="operator in conditionOperators" :key="operator.value" :value="operator.value">
            {{ operator.title }}
          </SelectItem>
        </SelectContent>
      </Select>

      <Button size="sm" variant="outline" @click="addRule">
        <Plus class="w-4 h-4 mr-1" />
                Ajouter règle
      </Button>

      <Button size="sm" variant="outline" @click="addNestedCondition">
        <Rows class="w-4 h-4 mr-1" />
                Ajouter sous-condition
      </Button>
        </div>

    <draggable 
      v-model="conditionRules" 
      :group="{ name: 'query-builder-condition-rules' }" 
      item-key="index"
      class="query-builder-condition-rules" 
      handle=".query-builder-drag-handle"
    >
            <template #item="{ element: rule, index }">
                <div :key="index" class="mb-2 rule-item">
          <div class="flex rule-container">
            <div 
              :class="{
                            'query-builder-drag-handle': true,
                            'nested-condition': filterManager.isCondition(rule)
              }" 
            />

            <div class="flex-1">
              <QueryBuilderCondition 
                v-if="filterManager.isCondition(rule)" 
                :modelValue="rule"
                :modelName="modelName" 
                class="nested-condition" 
                @delete="removeRule(index)" 
              />

              <QueryBuilderRule 
                v-else 
                :modelValue="rule" 
                :modelName="modelName"
                @delete="removeRule(index)" 
              />
                        </div>
                    </div>
                </div>
            </template>
        </draggable>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import draggable from 'vuedraggable'
import { Plus, Rows } from 'lucide-vue-next'
import { Button } from '@/common/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { useFilters } from '@/common/composables/filters'
import QueryBuilderRule from '@/common/components/controlPanel/filters/QueryBuilderRule.vue'

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

const filterManager = useFilters()

const conditionOperators = [
    { title: 'ET', value: '&' },
    { title: 'OU', value: '|' }
]

const conditionOperator = computed({
    get: () => props.modelValue[0] || '&',
    set: (value) => {
    props.modelValue[0] = value || '&'
    },
})

const conditionRules = computed({
    get: () => props.modelValue[1] || [],
    set: (value) => {
    props.modelValue[1] = value || []
    },
})

function addNestedCondition() {
  conditionRules.value.push(filterManager.createCondition('&', [filterManager.createRule()]))
}

function addRule() {
  conditionRules.value.push(filterManager.createRule())
}

function removeRule(index) {
    if (index >= conditionRules.value.length) {
    return
    }

  conditionRules.value.splice(index, 1)

    if (conditionRules.value.length === 0) {
    emit('delete')
    }
}
</script>