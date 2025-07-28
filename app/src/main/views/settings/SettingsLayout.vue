<template>
    <div class="h-full flex flex-col bg-neutral-50">
        <div class="bg-white border-b px-6 py-4">
            <h1 class="text-2xl font-bold text-neutral-900">Paramètres</h1>
            <p class="text-neutral-600">Gérez les paramètres de votre compte et définissez vos préférences.</p>
        </div>

        <div class="flex-1 mw-full flex">
            <div class="w-64 bg-white border-r min-h-full">
                <nav class="px-6 py-4">
                    <div class="space-y-1">
                        <router-link to="/settings/general" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            $route.name === 'settings-general'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Settings2 class="h-4 w-4" />
                            Général
                        </router-link>
                        <router-link to="/settings/jobs" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            $route.name === 'settings-jobs'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Map class="h-4 w-4" />
                            Interventions
                        </router-link>
                        <router-link to="/settings/crm" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            $route.name === 'settings-crm'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Building class="h-4 w-4" />
                            CRM
                        </router-link>
                        <router-link to="/settings/users" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            $route.name === 'settings-users'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Users class="h-4 w-4" />
                            Utilisateurs
                        </router-link>
                        <router-link to="/settings/billing" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            $route.name === 'settings-billing'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <CreditCard class="h-4 w-4" />
                            Facturation
                        </router-link>
                        <router-link to="/settings/display" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            $route.name === 'settings-display'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Monitor class="h-4 w-4" />
                            Affichage
                        </router-link>
                    </div>
                </nav>
            </div>

            <div class="flex-1 bg-white">
                <div class="p-6">
                    <router-view />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Building, CreditCard, Map, Monitor, Settings2, Users } from 'lucide-vue-next';
</script>