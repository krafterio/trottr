<template>
    <nav class="w-full bg-primary text-white px-6 py-3">
        <div class="flex items-center justify-between h-full">
            <div class="flex items-center space-x-3">
                <img src="@/common/assets/img/icon-white.svg" alt="Trottr"
                    class="h-6 transition-all duration-500 [transform-style:preserve-3d] hover:[transform:rotateY(180deg)]" />

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

            <div class="flex items-center space-x-2">
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

                <Button @click="handleCreateJob"
                    class="h-8 w-8 p-0 text-black hover:bg-neutral-800 bg-secondary cursor-pointer hover:bg-secondary/80 rounded-sm">
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
import { bus } from '@/common/composables/bus'
import { useWorkspaceStore } from '@/main/stores/workspace'
import { Bell, HelpCircle, Plus, Search } from 'lucide-vue-next'
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavbarUser from './NavbarUser.vue'

const route = useRoute()
const workspaceStore = useWorkspaceStore()

const moduleLinks = {
    interventions: [
        { href: '/', label: 'Toutes les interventions' },
        { href: '/job-planner', label: 'Planificateur d\'interventions' },
        { href: '/jobs-proto', label: 'Interventions (proto)' },
        { href: '/job-proto', label: 'Intervention (proto)' }
    ],
    crm: computed(() => {
        const baseLinks = [
            { href: '/companies', label: 'Sociétés' },
            { href: '/contacts', label: 'Contacts' },
            { href: '/sites', label: 'Sites' }
        ]

        if (workspaceStore.workspace?.use_subsites) {
            baseLinks.push({ href: '/subsites', label: 'Lots' })
        }

        return baseLinks
    }),
    vente: [
        { href: '/devis', label: 'Devis' },
        { href: '/contrats', label: 'Contrats' }
    ],
    planning: [
        { href: '/planning', label: 'Planning' },
    ],
    dashboard: [
        { href: '/dashboard', label: 'Tableau de bord' },
    ],
    documents: [
        { href: '#', label: 'Bientôt disponible', disabled: true }
    ],
    gestion: computed(() => {
        const baseLinks = [
            { href: '/tasks', label: 'Tâches d\'intervention' },
            { href: '/stock', label: 'Stock' },
            { href: '/produits', label: 'Fiches produit' },
        ]

        if (workspaceStore.workspace?.use_diagnostics) {
            baseLinks.splice(1, 0, { href: '/diagnostics', label: 'Diagnostics' })
        }

        return baseLinks
    }),
    rh: [
        { href: '/operateurs', label: 'Opérateurs' },
        { href: '/absences', label: 'Absences / congés' }
    ]
}

const currentModule = computed(() => {
    const name = route.name

    if (name === 'jobs' || name === 'job' || name === 'job-planner' || name === 'jobs-proto' || name === 'job-proto') {
        return 'interventions'
    } else if (name === 'companies' || name === 'company' || name === 'contacts' || name === 'contact' || name === 'sites' || name === 'site' || name === 'subsites' || name === 'subsite') {
        return 'crm'
    } else if (name === 'devis' || name === 'contrats') {
        return 'vente'
    } else if (name === 'planning') {
        return 'planning'
    } else if (name === 'dashboard') {
        return 'dashboard'
    } else if (name === 'documents') {
        return 'documents'
    } else if (name === 'stock' || name === 'tasks' || name === 'produits' || name === 'flotte' || name === 'gestion' || name === 'diagnostics') {
        return 'gestion'
    } else if (name === 'operateurs' || name === 'absences' || name === 'rh') {
        return 'rh'
    }

    return null
})

const currentModuleLinks = computed(() => {
    const module = currentModule.value
    if (!module) return []

    const links = moduleLinks[module]
    // Si c'est un computed ref, on accède à .value
    return links?.value ? links.value : (links || [])
})

const isActiveLink = (href) => {
    return route.path === href || route.path.startsWith(href + '/')
}

const handleCreateJob = () => {
    bus.trigger('open-job-dialog', {})
}

</script>