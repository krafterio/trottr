<template>
  <AlertDialog v-model:open="localShow">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle class="flex items-center gap-2">
          <Trash2 :size="16" />
          {{ title }}
        </AlertDialogTitle>
        <AlertDialogDescription class="space-y-2">
          <p>{{ message }}</p>
          <p v-if="itemName" class="font-semibold text-foreground">{{ itemName }}</p>
          <p class="text-sm text-muted-foreground flex items-center">
            <Info :size="14" class=" mr-1" />
            {{ confirmationText || 'Cette action est irréversible.' }}
          </p>
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel @click="cancel" :disabled="loading">
          {{ cancelText || 'Annuler' }}
        </AlertDialogCancel>
        <AlertDialogAction @click="confirm" :disabled="loading">
          <div v-if="loading"
            class="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2"></div>
          <Trash2 :size="16" />
          {{ confirmText || 'Supprimer' }}
        </AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>

<script setup>
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle
} from '@/common/components/ui/alert-dialog';
import { bus } from '@/common/composables/bus';
import { Info, Trash2 } from 'lucide-vue-next';
import { computed } from 'vue';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  itemName: {
    type: String,
    default: ''
  },
  confirmationText: {
    type: String,
    default: ''
  },
  confirmText: {
    type: String,
    default: ''
  },
  cancelText: {
    type: String,
    default: ''
  },
  loading: {
    type: Boolean,
    default: false
  }
});

const localShow = computed({
  get: () => props.show,
  set: (value) => bus.trigger('confirm-delete-dialog:update-show', value)
});

const confirm = () => {
  bus.trigger('confirm-delete-dialog:confirm');
};

const cancel = () => {
  bus.trigger('confirm-delete-dialog:cancel');
  localShow.value = false;
};
</script>