<template>
  <div class="s-quill-editor" :class="$attrs.class">
    <div ref="editorContainer" class="editor-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';

defineOptions({
  inheritAttrs: false
});

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  readonly: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue']);

const editorContainer = ref(null);
const quill = ref(null);
let ignoreChange = false;

const toolbarOptions = [
  ['bold', 'italic', 'underline'],
  [{ 'header': 1 }, { 'header': 2 }],
  [{ 'header': [1, 2, 3, false] }],
  [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'list': 'check' }],
  [{ 'align': [] }],
];

onMounted(() => {
  nextTick(() => {
    quill.value = new Quill(editorContainer.value, {
      modules: {
        toolbar: toolbarOptions
      },
      placeholder: props.placeholder,
      readOnly: props.readonly,
      theme: 'snow'
    });
    
    quill.value.on('text-change', () => {
      if (!ignoreChange) {
        emit('update:modelValue', quill.value.root.innerHTML);
      }
      ignoreChange = false;
    });
    
    if (props.modelValue) {
      quill.value.root.innerHTML = props.modelValue;
    }
  });
});

watch(() => props.modelValue, (newVal) => {
  if (quill.value && newVal !== quill.value.root.innerHTML) {
    ignoreChange = true;
    quill.value.root.innerHTML = newVal || '';
  }
});

watch(() => props.readonly, (newVal) => {
  if (quill.value) {
    quill.value.enable(!newVal);
  }
});

onBeforeUnmount(() => {
  if (quill.value) {
    quill.value = null;
  }
});
</script>