<template>
  <Dialog :open="opened">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle class="flex items-center gap-2">
          <AlertTriangle class="w-5 h-5 text-amber-500" />
          Espace de travail invalide
        </DialogTitle>
        <DialogDescription>
          Votre espace de travail n'est pas valide. Pour continuer à utiliser toutes les fonctionnalités de Trottr, veuillez mettre à jour votre plan d'abonnement.
        </DialogDescription>
      </DialogHeader>
      
      <DialogFooter class="gap-2">
        <Button @click="goToBilling">
          <CreditCard class="w-4 h-4 mr-2" />
          Mettre à jour mon plan
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { AlertTriangle, CreditCard } from 'lucide-vue-next'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Button } from '@/common/components/ui/button'
import {useAuthStore} from '@/common/stores/auth'
import {useWorkspaceStore} from '@/main/stores/workspace'
import {ref, watch} from 'vue';

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const workspaceStore = useWorkspaceStore()
const opened = ref(false)

watch(() => [authStore.isAuthenticated, workspaceStore.workspace, workspaceStore.workspace?.valid, route.fullPath], () => {
  if (authStore.isAuthenticated && workspaceStore.workspace && !workspaceStore.isValid) {
    if (route.name && route.name !== 'settings-billing' && route.name !== 'settings-users') {
      opened.value = true
    }
  }
})

function goToBilling() {
  router.push({ name: 'settings-billing' })
  opened.value = false
}
</script> 
