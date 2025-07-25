<template>
  <img 
    v-bind="$attrs" 
    :src="src" 
    :class="['max-w-full', 'h-auto', { 'object-cover': cover }]"
    :alt="alt || ''"
  />
</template>

<script setup>
defineProps({
  src: {
    type: String,
    default: ''
  },
  withApi: {
    type: Boolean,
    default: false
  },
  cover: {
    type: Boolean,
    default: false
  },
  alt: {
    type: String,
    default: ''
  }
})
</script>
