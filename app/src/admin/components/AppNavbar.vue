<template>
    <div class="border-b bg-white px-6 py-4" v-if="authStore.isAuthenticated">
        <div class="container px-5 mx-auto flex items-center justify-between">
            <div class="flex items-center space-x-6">
                <img src="@/common/assets/img/logo.svg" alt="Trottr" width="80" height="auto" />

                <Menubar>
                    <MenubarMenu>
                        <MenubarTrigger>
                            <Home :size="16" class="mr-2" />
                            Accueil
                        </MenubarTrigger>
                        <MenubarContent>
                            <MenubarItem @click="$router.push({ name: 'home' })">
                                <Home :size="16" class="mr-2" />
                                Tableau de bord
                            </MenubarItem>
                        </MenubarContent>
                    </MenubarMenu>

                    <MenubarMenu>
                        <MenubarTrigger>
                            <Users :size="16" class="mr-2" />
                            Gestion
                        </MenubarTrigger>
                        <MenubarContent>
                            <MenubarItem @click="$router.push({ name: 'workspaces' })">
                                <Building2 :size="16" class="mr-2" />
                                Espaces de travail
                            </MenubarItem>
                            <MenubarItem @click="$router.push({ name: 'user-invitations' })">
                                <UserCheck :size="16" class="mr-2" />
                                Demande d'accès
                            </MenubarItem>
                        </MenubarContent>
                    </MenubarMenu>

                    <MenubarMenu>
                        <MenubarTrigger>
                            <Settings :size="16" class="mr-2" />
                            Configuration
                        </MenubarTrigger>
                        <MenubarContent>
                            <MenubarItem @click="$router.push({ name: 'service-plans' })">
                                <Crown :size="16" class="mr-2" />
                                Plans d'abonnement
                            </MenubarItem>
                            <MenubarItem @click="$router.push({ name: 'countries' })">
                                <Globe :size="16" class="mr-2" />
                                Pays
                            </MenubarItem>
                            <MenubarItem @click="$router.push({ name: 'interaction-types' })">
                                <MessageCircle :size="16" class="mr-2" />
                                Types d'interactions
                            </MenubarItem>
                            <MenubarItem @click="$router.push({ name: 'service-taxes' })">
                                <Percent weight="light" :size="16" class="mr-2" />
                                Taxes des services
                            </MenubarItem>
                        </MenubarContent>
                    </MenubarMenu>

                    <MenubarMenu>
                        <MenubarTrigger>
                            <Headset weight="light" :size="16" class="mr-2" />
                            Support
                        </MenubarTrigger>
                        <MenubarContent>
                            <MenubarItem>
                                <Headset weight="light" :size="16" class="mr-2" />
                                Tickets
                            </MenubarItem>
                            <MenubarSeparator />
                            <MenubarItem>
                                <BookOpenText weight="light" :size="16" class="mr-2" />
                                Documentation
                            </MenubarItem>
                            <MenubarItem>
                                <Lightbulb weight="light" :size="16" class="mr-2" />
                                Idées
                            </MenubarItem>
                        </MenubarContent>
                    </MenubarMenu>

                    <MenubarMenu>
                        <MenubarTrigger>
                            <Megaphone weight="light" :size="16" class="mr-2" />
                            Marketing
                        </MenubarTrigger>
                        <MenubarContent>
                            <MenubarItem @click="$router.push({ name: 'service-credit-coupons' })">
                                <Ticket weight="light" :size="16" class="mr-2" />
                                Coupons
                            </MenubarItem>
                            <MenubarItem @click="$router.push({ name: 'service-credit-packs' })">
                                <Coins weight="light" :size="16" class="mr-2" />
                                Packs enrichissement
                            </MenubarItem>
                        </MenubarContent>
                    </MenubarMenu>
                </Menubar>
            </div>

            <div class="flex items-center justify-end space-x-4">
                <AppNavbarAccount />
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from '@/common/stores/auth'
import AppNavbarAccount from '@/admin/components/navbar/AppNavbarAccount.vue'
import {
    Menubar,
    MenubarContent,
    MenubarItem,
    MenubarMenu,
    MenubarSeparator,
    MenubarTrigger,
} from '@/common/components/ui/menubar'
import {
    Home,
    Users,
    UserCheck,
    Settings,
    Globe,
    MessageCircle,
    Percent,
    Crown,
    Headset,
    BookOpenText,
    Lightbulb,
    Megaphone,
    Ticket,
    Coins,
    Building2,
} from 'lucide-vue-next'

const authStore = useAuthStore()
</script>
