<template>
    <div class="w-16 bg-white border-r flex flex-col items-center py-3">
        <div class="space-y-2 flex-1">
            <div v-for="module in modules" :key="module.title" class="relative group">
                <a :href="module.url" :class="[
                    'w-10 h-10 flex items-center justify-center rounded-lg transition-colors',
                    isActiveRoute(module)
                        ? 'bg-primary text-white hover:bg-primary/90'
                        : module.disabled
                            ? 'text-gray-300 cursor-not-allowed'
                            : 'text-gray-600 hover:bg-gray-100'
                ]" :aria-disabled="module.disabled">
                    <component :is="module.icon" class="h-5 w-5" />
                </a>

                <div
                    class="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 text-white text-xs rounded shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                    {{ module.title }}
                    <div
                        class="absolute right-full top-1/2 -translate-y-1/2 border-4 border-transparent border-r-gray-900">
                    </div>
                </div>
            </div>
        </div>

        <div class="relative group">
            <router-link to="/settings" :class="[
                'w-10 h-10 flex items-center justify-center rounded-lg transition-colors',
                route.name?.startsWith('settings')
                    ? 'bg-primary text-white hover:bg-primary/90'
                    : 'text-gray-600 hover:bg-gray-100'
            ]">
                <Settings class="h-5 w-5" />
            </router-link>

            <div
                class="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 text-white text-xs rounded shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                Paramètres
                <div class="absolute right-full top-1/2 -translate-y-1/2 border-4 border-transparent border-r-gray-900">
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import {
    BarChart3,
    Blocks,
    CalendarDays,
    FileText,
    Map,
    Settings,
    Users,
    UsersIcon
} from 'lucide-vue-next'
import { useRoute } from 'vue-router'

const route = useRoute()

const modules = [
    {
        title: 'Interventions',
        url: '/',
        icon: Map,
        module: 'interventions'
    },
    {
        title: 'CRM',
        url: '/companies',
        icon: UsersIcon,
        module: 'crm'
    },
    {
        title: 'Planning',
        url: '/planning',
        icon: CalendarDays,
        module: 'planning'
    },
    {
        title: 'Tableau de bord',
        url: '/dashboard',
        icon: BarChart3,
        module: 'dashboard'
    },
    {
        title: 'Gestion',
        url: '/tasks',
        icon: Blocks,
        module: 'gestion'
    },
    {
        title: 'Opérateurs',
        url: '/operateurs',
        icon: Users,
        module: 'employes'
    },
    {
        title: 'Vente (bientôt disponible)',
        url: '/devis',
        icon: FileText,
        disabled: true,
        module: 'vente'
    },
    {
        title: 'Documents (bientôt disponible)',
        url: '/documents',
        icon: FileText,
        disabled: true,
        module: 'documents'
    },
]

const getCurrentModule = () => {
    const name = route.name

    if (['jobs', 'job', 'job-planner'].includes(name)) {
        return 'interventions'
    }
    if (['companies', 'company', 'contacts', 'contact', 'sites', 'site', 'subsites', 'subsite'].includes(name)) {
        return 'crm'
    }
    if (name === 'planning') {
        return 'planning'
    }
    if (name === 'dashboard') {
        return 'dashboard'
    }
    if (['stock', 'operations', 'produits', 'gestion'].includes(name)) {
        return 'gestion'
    }
    if (['techniciens', 'absences', 'rh'].includes(name)) {
        return 'employes'
    }
    if (['devis', 'contrats'].includes(name)) {
        return 'vente'
    }
    if (name === 'documents') {
        return 'documents'
    }

    return null
}

const isActiveRoute = (module) => {
    return getCurrentModule() === module.module
}
</script>