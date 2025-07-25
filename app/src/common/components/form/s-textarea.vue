<template>
  <textarea
    ref="textareaRef"
    :value="modelValue"
    @input="onInput"
    :placeholder="placeholder"
    :class="['s-textarea', textareaClass, { 's-textarea--naked': naked }]"
    :rows="1"
    v-bind="$attrs"
    autocomplete="off"
    spellcheck="false"
  />
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  textareaClass: {
    type: String,
    default: ''
  },
  naked: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])
const textareaRef = ref(null)

const resize = () => {
  const el = textareaRef.value
  if (!el) return
  el.style.height = 'auto'
  el.style.height = el.scrollHeight + 'px'
}

const onInput = (e) => {
  emit('update:modelValue', e.target.value)
  resize()
}

watch(() => props.modelValue, () => nextTick(resize))
onMounted(resize)
</script>