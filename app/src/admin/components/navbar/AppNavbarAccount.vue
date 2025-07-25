<template>
    <DropdownMenu>
        <DropdownMenuTrigger as-child>
            <Button variant="ghost" class="h-auto p-2 justify-start">
                <Avatar class="h-8 w-8">
                    <AvatarImage 
                        v-if="authStore.user?.avatar" 
                        v-fetcher-src.lazy 
                        :src="`/storage/download/${authStore.user.avatar}`" 
                        :alt="authStore.user?.name" 
                    />
                    <AvatarFallback class="bg-gray-100">
                        {{ authStore.user?.name?.[0] }}
                    </AvatarFallback>
                </Avatar>
                
                <div class="flex flex-col items-start text-left">
                    <span class="text-sm font-semibold">{{ authStore.user?.name }}</span>
                    <span class="text-xs text-normal text-muted-foreground font-normal">{{ authStore.user?.email }}</span>
                </div>
            </Button>
        </DropdownMenuTrigger>
        
        <DropdownMenuContent align="end" class="w-56">
            <DropdownMenuItem @click="authStore.logout()" class="text-red-600 focus:text-red-600">
                <LogOut :size="16" class="mr-2" />
                Déconnexion
            </DropdownMenuItem>
        </DropdownMenuContent>
    </DropdownMenu>
</template>

<script setup>

import { useAuthStore } from '@/common/stores/auth'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import { Button } from '@/common/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { LogOut } from 'lucide-vue-next'

const authStore = useAuthStore()
</script> 