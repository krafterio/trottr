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
          <p v-if="dialogData.confirmationText" class="text-sm text-muted-foreground flex items-center">
            <Info :size="14" class=" mr-1" />
            {{ dialogData.confirmationText }}
          </p>
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel @click="cancel" :disabled="loading">
          Annuler
        </AlertDialogCancel>
        <AlertDialogAction @click="confirm" :disabled="loading">
          <div v-if="loading"
            class="h-4 w-4 border-2 border-current border-t-transparent rounded-full animate-spin mr-2"></div>
          <Trash2 :size="16" />
          Supprimer
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
const dialogData = ref({})

// Écoute l'événement d'ouverture générique
useBus(bus, 'confirm-delete', (event) => {
  const data = event.detail
  dialogData.value = data
  isOpen.value = true
})

const confirm = () => {
  loading.value = true
  bus.trigger(dialogData.value.confirmEvent, dialogData.value)
}

const cancel = () => {
  isOpen.value = false
  loading.value = false
  if (dialogData.value.cancelEvent) {
    bus.trigger(dialogData.value.cancelEvent, dialogData.value)
  }
}

// Écoute pour fermer après action terminée
useBus(bus, 'confirm-delete-dialog:close', () => {
  isOpen.value = false
  loading.value = false
})
</script>