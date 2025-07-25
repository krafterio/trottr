<template>
    <div class="s-field" :class="{ 's-field-horizontal': horizontal }">
        <label v-if="label" class="s-field-label text-body-2 d-block">{{ label }}</label>
        <div :class="horizontal ? 'flex-grow-1' : ''">
            <s-quill-editor
                v-if="fieldType === 'v-textarea' && html"
                :model-value="modelValue"
                @update:model-value="updateModel"
                :placeholder="placeholder"
                :class="[quillClass, getQuillEditorClass()]"
                :rows="rows"
                v-bind="fieldAttrs"
            />
            <component
                v-else
                :is="fieldType"
                :model-value="modelValue"
                @update:model-value="updateModel"
                :placeholder="placeholder"
                :rows="fieldType === 'v-textarea' ? rows : undefined"
                :class="horizontal ? 'bg-grey-lighten-4' : ''"
                v-bind="fieldAttrs"
            >
                <template v-for="(_, name) in $slots" #[name]="slotData">
                    <slot :name="name" v-bind="slotData || {}"></slot>
                </template>
            </component>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useAttrs } from 'vue';
import SQuillEditor from '@/common/components/form/s-quill-editor.vue';
import {hasProps} from "@/common/utils/components";

defineOptions({
    name: 's-field'
});

const props = defineProps({
    modelValue: {
        type: [String, Number, Boolean, Array, Object],
        default: null
    },
    label: {
        type: String,
        default: ''
    },
    fieldType: {
        type: String,
        default: 'v-text-field'
    },
    placeholder: {
        type: String,
        default: ''
    },
    html: {
        type: Boolean,
        default: false
    },
    quillClass: {
        type: String,
        default: ''
    },
    rows: {
        type: [Number, String],
        default: undefined
    },
    horizontal: {
        type: Boolean,
        default: false
    },
    editorStyle: {
        type: String,
        default: ''
    }
});

const emit = defineEmits(['update:modelValue']);

const attrs = useAttrs();

const fieldAttrs = computed(() => {
    const fieldAttributes = { ...attrs };
    if (hasProps(props.fieldType, 'variant') && props.horizontal) {
      fieldAttributes.variant = 'solo-filled';
        fieldAttributes.flat = true;
    }
    return fieldAttributes;
});

const getQuillEditorClass = () => {
    let classes = ['no-border'];
    
    if (props.editorStyle === 'outlined') {
        classes.push('border rounded');
    } else if (props.editorStyle === 'blank') {
        classes.push('bg-white');
    } else {
        classes.push('bg-grey-lighten-4');
    }
    
    if (props.horizontal) {
        classes.push('bg-grey-lighten-4');
    }

    return classes.join(' ');
};

const updateModel = (value) => {
    emit('update:modelValue', value);
};
</script>

<style scoped>
.s-field {
    margin-bottom: 16px;
}
</style> 