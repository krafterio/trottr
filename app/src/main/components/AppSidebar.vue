<script setup>
import {
    BarChart3,
    Blocks,
    CalendarDays,
    FileText,
    Map,
    Settings,
    UsersIcon
} from 'lucide-vue-next'
import { useRoute } from 'vue-router'

const route = useRoute()

const modules = [
    {
        title: 'Interventions',
        url: '/home',
        icon: Map,
    },
    {
        title: 'CRM',
        url: '/clients',
        icon: UsersIcon,
    },
    {
        title: 'Devis',
        url: '/devis',
        icon: FileText,
    },
    {
        title: 'Planning',
        url: '/planning',
        icon: CalendarDays,
    },
    {
        title: 'Tableau de bord',
        url: '/reports',
        icon: BarChart3,
    },
    {
        title: 'Documents',
        url: '/documents',
        icon: FileText,
    },
    {
        title: 'Gestion',
        url: '/gestion',
        icon: Blocks,
    },
]

const isActiveRoute = (url) => {
    if (url === '/home') {
        return route.path === '/home' || route.path === '/'
    }
    return route.path.startsWith(url)
}
</script>

<template>
    <div class="w-16 bg-white border-r flex flex-col items-center py-4">
        <div class="space-y-2 flex-1">
            <div v-for="module in modules" :key="module.title" class="relative group">
                <a :href="module.url" :class="[
                    'w-10 h-10 flex items-center justify-center rounded-lg transition-colors',
                    isActiveRoute(module.url)
                        ? 'bg-primary text-white hover:bg-primary/90'
                        : 'text-gray-600 hover:bg-gray-100'
                ]">
                    <component :is="module.icon" class="h-5 w-5" />
                </a>

                <!-- Tooltip -->
                <div
                    class="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 text-white text-xs rounded shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                    {{ module.title }}
                    <!-- Flèche -->
                    <div
                        class="absolute right-full top-1/2 -translate-y-1/2 border-4 border-transparent border-r-gray-900">
                    </div>
                </div>
            </div>
        </div>

        <!-- Bouton Paramètres en bas -->
        <div class="relative group">
            <a href="/settings" :class="[
                'w-10 h-10 flex items-center justify-center rounded-lg transition-colors',
                isActiveRoute('/settings')
                    ? 'bg-primary text-white hover:bg-primary/90'
                    : 'text-gray-600 hover:bg-gray-100'
            ]">
                <Settings class="h-5 w-5" />
            </a>

            <!-- Tooltip -->
            <div
                class="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-2 py-1 bg-gray-900 text-white text-xs rounded shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50">
                Paramètres
                <!-- Flèche -->
                <div class="absolute right-full top-1/2 -translate-y-1/2 border-4 border-transparent border-r-gray-900">
                </div>
            </div>
        </div>
    </div>
</template>