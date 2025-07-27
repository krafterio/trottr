<template>
    <nav class="w-full bg-primary text-white px-6 py-3">
        <div class="flex items-center justify-between h-full">
            <div class="flex items-center space-x-3">
                <img src="/trottr-favicon-white.svg" alt="Trottr" class="h-6" />

                <div class="w-px ms-2 h-6 bg-neutral-700"></div>

                <NavigationMenu v-if="currentModuleLinks.length > 0">
                    <NavigationMenuList class="space-x-1">
                        <NavigationMenuItem v-for="link in currentModuleLinks" :key="link.href">
                            <NavigationMenuLink :href="link.href" v-if="!link.disabled" :class="[
                                'px-3 py-2 rounded-md text-sm font-medium transition-colors focus:bg-neutral-800 focus:text-white',
                                isActiveLink(link.href)
                                    ? 'text-white bg-neutral-800'
                                    : 'text-neutral-200 hover:text-white hover:bg-neutral-800'
                            ]">
                                {{ link.label }}
                            </NavigationMenuLink>
                            <span v-else
                                class="text-neutral-500 px-3 py-2 rounded-md text-sm font-medium cursor-not-allowed">
                                {{ link.label }}
                            </span>
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
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavbarUser from './NavbarUser.vue'

const route = useRoute()

const moduleLinks = {
    interventions: [
        { href: '/', label: 'Toutes les interventions' },
        { href: '/job-planner', label: 'Planificateur d\'interventions' }
    ],
    crm: [
        { href: '/companies', label: 'Sociétés' },
        { href: '/contacts', label: 'Contacts' },
        { href: '/sites', label: 'Sites d\'intervention' },
        { href: '/lots', label: 'Lots' }
    ],
    vente: [
        { href: '/devis', label: 'Devis' },
        { href: '/contrats', label: 'Contrats' }
    ],
    planning: [],
    dashboard: [],
    documents: [
        { href: '#', label: 'Bientôt disponible', disabled: true }
    ],
    gestion: [
        { href: '/stock', label: 'Stock pièces détachées' },
        { href: '/operations', label: 'Opérations' },
        { href: '/produits', label: 'Fiches produit' },
        { href: '/flotte', label: 'Flotte' }
    ],
    rh: [
        { href: '/techniciens', label: 'Techniciens' },
        { href: '/absences', label: 'Absences / congés' }
    ]
}

const currentModule = computed(() => {
    const name = route.name

    if (name === 'jobs' || name === 'job' || name === 'job-planner') {
        return 'interventions'
    } else if (name === 'companies' || name === 'company' || name === 'contacts' || name === 'sites' || name === 'lots') {
        return 'crm'
    } else if (name === 'devis' || name === 'contrats') {
        return 'vente'
    } else if (name === 'planning') {
        return 'planning'
    } else if (name === 'dashboard') {
        return 'dashboard'
    } else if (name === 'documents') {
        return 'documents'
    } else if (name === 'stock' || name === 'operations' || name === 'produits' || name === 'flotte' || name === 'gestion') {
        return 'gestion'
    } else if (name === 'techniciens' || name === 'absences' || name === 'rh') {
        return 'rh'
    }

    return null
})

const currentModuleLinks = computed(() => {
    return currentModule.value ? moduleLinks[currentModule.value] || [] : []
})

const isActiveLink = (href) => {
    if (href === '/') {
        return route.path === '/'
    }
    return route.path.startsWith(href)
}
</script>