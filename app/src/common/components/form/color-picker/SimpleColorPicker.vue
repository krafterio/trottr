<template>
  <div class="flex flex-wrap gap-2">
    <div v-for="color in colorOptions" :key="color" class="color-option" :class="{ 'selected': modelValue === color }"
      :style="{ backgroundColor: color }" @click="selectColor(color)" />
  </div>
</template>

<script setup>
import { defineEmits, defineProps } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: '#a7c7e7'
  }
});

const emit = defineEmits(['update:modelValue']);

const colorOptions = [
  '#A7E00A', '#714F82', '#F54740', '#E7D58D', '#343731',
  '#E2B93B', '#775C44', '#8CC167', '#bfbfbf', '#3B5C26',
  '#BC4927', '#6187B4', '#C96693', '#7D8086', '#965447',
  '#9D9A0C', '#5DB451', '#C2433A', '#e59303', '#51363D'
];

const selectColor = (color) => {
  emit('update:modelValue', color);
};
</script>

<style scoped>
.color-option {
  width: 32px;
  height: 32px;
  border-radius: 100%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.color-option.selected {
  border-color: #fff;
  box-shadow: 0 0 0 2px #1976d2;
}
</style>