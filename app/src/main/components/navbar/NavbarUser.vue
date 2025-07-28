<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" class="relative h-8 w-8 rounded-sm hover:bg-neutral-80 cursor-pointer">
                <Avatar class="h-8 w-8 rounded-sm">
                    <AvatarImage v-if="authStore.user?.avatar" :src="`/storage/download/${authStore.user.avatar}`"
                        v-fetcher-src.lazy :alt="authStore.user.name" />
                    <AvatarFallback class="bg-neutral-800 text-neutral-300 rounded-sm">
                        {{ authStore.user?.name?.[0]?.toUpperCase() || 'U' }}
                    </AvatarFallback>
                </Avatar>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56" align="end" :side-offset="4">
            <DropdownMenuLabel class="p-0 font-normal">
                <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                    <Avatar class="h-8 w-8 rounded-sm">
                        <AvatarImage v-if="authStore.user?.avatar" :src="`/storage/download/${authStore.user.avatar}`"
                            v-fetcher-src.lazy :alt="authStore.user.name" />
                        <AvatarFallback class="rounded-sm">
                            {{ authStore.user?.name?.[0]?.toUpperCase() || 'U' }}
                        </AvatarFallback>
                    </Avatar>
                    <div class="grid flex-1 text-left text-sm leading-tight">
                        <span class="truncate font-semibold">{{ authStore.user?.name || 'Utilisateur' }}</span>
                        <span class="truncate text-xs">{{ authStore.user?.email || '' }}</span>
                    </div>
                </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
                <DropdownMenuItem @click="openEditDialog">
                    <BadgeCheck class="mr-2 h-4 w-4" />
                    Compte
                </DropdownMenuItem>
                <DropdownMenuItem>
                    <Bell class="mr-2 h-4 w-4" />
                    Notifications
                </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="handleLogout">
                <LogOut class="mr-2 h-4 w-4" />
                Se déconnecter
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>

    <AccountDialog :is-open="isDialogOpen" :user="authStore.user" />
</template>

<script setup>
import {
    BadgeCheck,
    Bell,
    LogOut
} from 'lucide-vue-next';
import { ref } from 'vue';

import {
    Avatar,
    AvatarFallback,
    AvatarImage,
} from '@/common/components/ui/avatar';
import { Button } from '@/common/components/ui/button';
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuGroup,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu';
import { bus, useBus } from '@/common/composables/bus';
import { useAuthStore } from '@/common/stores/auth';
import AccountDialog from '@/main/components/dialogs/AccountDialog.vue';

const authStore = useAuthStore()

const isDialogOpen = ref(false)

const handleLogout = async () => {
    await authStore.logout()
}

const openEditDialog = () => {
    isDialogOpen.value = true
}

useBus(bus, 'account-dialog:update-open', (event) => {
    isDialogOpen.value = event.detail
})

useBus(bus, 'account-dialog:user-updated', () => {
    // L'utilisateur a été mis à jour via authStore dans AccountDialog
    // Déclencher aussi l'événement pour SettingsUsers si ouvert
    bus.trigger('user-edit-dialog:user-updated', { user: authStore.user })
})
</script>