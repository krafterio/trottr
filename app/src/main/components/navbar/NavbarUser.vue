<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" class="relative h-8 w-8 rounded-full">
                <Avatar class="h-6 w-6">
                    <AvatarImage :src="user?.avatar" :alt="user?.name || 'Utilisateur'" />
                    <AvatarFallback class="text-primary">
                        {{ user?.name?.charAt(0)?.toUpperCase() || 'U' }}
                    </AvatarFallback>
                </Avatar>
            </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent class="w-56" align="end" :side-offset="4">
            <DropdownMenuLabel class="p-0 font-normal">
                <div class="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                    <Avatar class="h-8 w-8">
                        <AvatarImage :src="user?.avatar" :alt="user?.name || 'Utilisateur'" />
                        <AvatarFallback>
                            {{ user?.name?.charAt(0)?.toUpperCase() || 'U' }}
                        </AvatarFallback>
                    </Avatar>
                    <div class="grid flex-1 text-left text-sm leading-tight">
                        <span class="truncate font-semibold">{{ user?.name || 'Utilisateur' }}</span>
                        <span class="truncate text-xs">{{ user?.email || '' }}</span>
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

    <UserEditDialog :is-open="isDialogOpen" :user="user" @update:open="isDialogOpen = $event"
        @user-updated="onUserUpdated" />
</template>

<script setup>
import {
    BadgeCheck,
    Bell,
    LogOut
} from 'lucide-vue-next';
import { computed, ref } from 'vue';

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
import { useAuthStore } from '@/common/stores/auth';
import UserEditDialog from './UserEditDialog.vue';

const authStore = useAuthStore()

const user = computed(() => authStore.user)

const isDialogOpen = ref(false)

const handleLogout = async () => {
    await authStore.logout()
}

const openEditDialog = () => {
    isDialogOpen.value = true
}

const onUserUpdated = () => {
    // L'utilisateur a été mis à jour via authStore dans UserEditDialog
}
</script>