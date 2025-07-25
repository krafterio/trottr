<template>
  <component :is="iconComponent" :class="cn('h-4 w-4', props.class)" />
</template>

<script setup>
import { cn } from '@/common/lib/utils'
import { computed } from 'vue'
import { 
  Bold, 
  Italic, 
  Strikethrough, 
  List, 
  ListOrdered, 
  Heading1, 
  Heading2, 
  Heading3,
  Minus,
  Undo,
  Redo,
  Quote
} from 'lucide-vue-next'

const props = defineProps({
  name: { type: String, required: true },
  class: { type: String, default: '' }
})

const iconMap = {
  'mdi:format-bold': Bold,
  'mdi:format-italic': Italic,
  'mdi:format-strikethrough': Strikethrough,
  'mdi:format-list-bulleted': List,
  'mdi:format-list-numbered': ListOrdered,
  'mdi:format-header-1': Heading1,
  'mdi:format-header-2': Heading2,
  'mdi:format-header-3': Heading3,
  'mdi:minus': Minus,
  'mdi:undo': Undo,
  'mdi:redo': Redo,
  'mdi:format-quote-close': Quote
}

const iconComponent = computed(() => {
  return iconMap[props.name] || Bold
})
</script> 