<template>
    <nav class="w-full bg-primary text-white px-6 py-3">
        <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <img src="/trottr-favicon-white.svg" alt="Trottr" class="h-6" />

                <div class="w-px ms-2 h-6 bg-neutral-700"></div>

                <NavigationMenu>
                    <NavigationMenuList class="space-x-1">
                        <NavigationMenuItem>
                            <NavigationMenuLink href="/home"
                                class="text-neutral-200 hover:text-white hover:bg-neutral-800 px-3 py-2 rounded-md text-sm font-medium transition-colors focus:bg-neutral-800 focus:text-white">
                                Toutes les interventions
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                        <NavigationMenuItem>
                            <NavigationMenuLink href="/job-planner"
                                class="text-neutral-400 hover:text-white hover:bg-neutral-800 px-3 py-2 rounded-md text-sm font-medium transition-colors focus:bg-neutral-800 focus:text-white">
                                Planificateur d'interventions
                            </NavigationMenuLink>
                        </NavigationMenuItem>
                    </NavigationMenuList>
                </NavigationMenu>
            </div>

            <div class="flex items-center space-x-1">
                <div class="flex items-center space-x-2 text-sm text-gray-300 hover:text-white cursor-pointer">
                    <HelpCircle class="h-4 w-4" />
                    <span>Besoin d'aide ?</span>
                </div>

                <div class="w-px ms-2 me-3   h-6 bg-neutral-700"></div>

                <!-- Barre de recherche -->
                <div class="relative me-3">
                    <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                    <Input type="text" placeholder="Recherche rapide..."
                        class="h-8 pl-10 pr-4 py-2 w-64 bg-neutral-800 border-none text-white placeholder:text-neutral-400 focus:bg-neutral-700 focus:placeholder:text-neutral-400 transition-colors !focus:outline-none focus:ring-0 !focus:ring-offset-0 !focus:border-none" />
                </div>

                <div class="w-px mx-2  h-6 bg-neutral-700"></div>

                <Button variant="ghost" size="sm"
                    class="h-8 w-8 p-0 text-neutral-200 hover:text-white hover:bg-neutral-800">
                    <Bell class="h-4 w-4" />
                </Button>

                <NavbarUser />

                <Button
                    class="h-8 w-8 p-0 text-black hover:bg-neutral-800 bg-secondary cursor-pointer hover:bg-secondary/80">
                    <Plus class="h-4 w-4" />
                </Button>
            </div>
        </div>
    </nav>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import Input from '@/common/components/ui/input/Input.vue'
import {
    NavigationMenu,
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
} from '@/common/components/ui/navigation-menu'
import { Bell, HelpCircle, Plus, Search } from 'lucide-vue-next'
import NavbarUser from './NavbarUser.vue'
</script>