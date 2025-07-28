<template>
  <AlertDialog v-model:open="isOpen">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle class="flex items-center gap-2">
          <Trash2 :size="16" />
          {{ dialogData.title }}
        </AlertDialogTitle>
        <AlertDialogDescription class="space-y-2">
          <p>{{ dialogData.message }}</p>
          <p v-if="dialogData.itemName" class="font-semibold text-foreground">{{ dialogData.itemName }}</p>
          <p class="text-sm text-muted-foreground flex items-center">
            <Info :size="14" class=" mr-1" />
            {{ dialogData.confirmationText || 'Cette action est irréversible.' }}
          </p>
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel @click="cancel" :disabled="loading">
          {{ dialogData.cancelText || 'Annuler' }}
        </AlertDialogCancel>
        <AlertDialogAction @click="confirm" :disabled="loading">
          <div v-if="loading"
            class="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2"></div>
          <Trash2 :size="16" />
          {{ dialogData.confirmText || 'Supprimer' }}
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
import { bus, useBus } from '@/common/composables/bus';
import { Info, Trash2 } from 'lucide-vue-next';
import { ref } from 'vue';

const isOpen = ref(false)
const loading = ref(false)
const dialogData = ref({
  title: '',
  message: '',
  itemName: '',
  confirmationText: '',
  confirmText: '',
  cancelText: ''
})

// Écoute l'événement d'ouverture générique
useBus(bus, 'confirm-delete', (event) => {
  const data = event.detail
  dialogData.value = {
    title: data.title || 'Supprimer',
    message: data.message || 'Êtes-vous sûr de vouloir supprimer cet élément ?',
    itemName: data.itemName || '',
    confirmationText: data.confirmationText || '',
    confirmText: data.confirmText || '',
    cancelText: data.cancelText || ''
  }
  isOpen.value = true
})

const confirm = () => {
  loading.value = true
  bus.trigger('confirm-delete-dialog:confirmed')
}

const cancel = () => {
  isOpen.value = false
  loading.value = false
  bus.trigger('confirm-delete-dialog:cancelled')
}

// Écoute pour fermer après action terminée
useBus(bus, 'confirm-delete-dialog:close', () => {
  isOpen.value = false
  loading.value = false
})
</script>