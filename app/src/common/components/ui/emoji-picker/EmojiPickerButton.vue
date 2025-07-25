<template>
  <Popover v-model:open="open">
    <PopoverTrigger>
      <Button
        type="button"
        variant="outline"
        size="sm"
        class="w-12 h-12 p-0 text-lg"
      >
        {{ selectedEmoji }}
      </Button>
    </PopoverTrigger>
    <PopoverContent class="w-80 p-0" align="start">
      <EmojiPicker @select="onEmojiSelect" />
    </PopoverContent>
  </Popover>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button } from '@/common/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/common/components/ui/popover'
import EmojiPicker from './EmojiPicker.vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '📁'
  }
})

const emit = defineEmits(['update:modelValue'])

const open = ref(false)

const selectedEmoji = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const onEmojiSelect = (emoji) => {
  console.log('Emoji selected:', emoji) // Debug
  selectedEmoji.value = emoji
  open.value = false
}
</script> 