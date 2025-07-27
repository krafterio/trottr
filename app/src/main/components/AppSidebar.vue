<template>
    <div class="w-16 bg-white border-r flex flex-col items-center py-3">
        <div class="space-y-2 flex-1">
            <div v-for="module in modules" :key="module.title" class="relative group">
                <a :href="module.url" :class="[
                    'w-10 h-10 flex items-center justify-center rounded-lg transition-colors',
                    isActiveRoute(module.url)
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
            <a href="/settings" :class="[
                'w-10 h-10 flex items-center justify-center rounded-lg transition-colors',
                isActiveRoute('/settings')
                    ? 'bg-primary text-white hover:bg-primary/90'
                    : 'text-gray-600 hover:bg-gray-100'
            ]">
                <Settings class="h-5 w-5" />
            </a>

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
    },
    {
        title: 'CRM',
        url: '/companies',
        icon: UsersIcon,
    },
    {
        title: 'Planning',
        url: '/planning',
        icon: CalendarDays,
    },
    {
        title: 'Tableau de bord',
        url: '/dashboard',
        icon: BarChart3,
    },
    {
        title: 'Gestion',
        url: '/operations',
        icon: Blocks,
    },
    {
        title: 'Employés',
        url: '/techniciens',
        icon: Users,
    },
    {
        title: 'Vente (bientôt disponible)',
        url: '/devis',
        icon: FileText,
        disabled: true,
    },
    {
        title: 'Documents (bientôt disponible)',
        url: '/documents',
        icon: FileText,
        disabled: true,
    },
]

const isActiveRoute = (url) => {
    const name = route.name

    if (url === '/') {
        return name === 'jobs' || name === 'job' || name === 'job-planner'
    }
    if (url === '/companies') {
        return name === 'companies' || name === 'company' || name === 'contacts' || name === 'contact' || name === 'sites' || name === 'site' || name === 'subsites' || name === 'subsite'
    }
    if (url === '/devis') {
        return name === 'devis' || name === 'contrats'
    }
    if (url === '/planning') {
        return name === 'planning'
    }
    if (url === '/dashboard') {
        return name === 'dashboard'
    }
    if (url === '/documents') {
        return name === 'documents'
    }
    if (url === '/operations') {
        return name === 'stock' || name === 'operations' || name === 'produits' || name === 'gestion'
    }
    if (url === '/techniciens') {
        return name === 'techniciens' || name === 'absences' || name === 'rh'
    }
    return false
}
</script>