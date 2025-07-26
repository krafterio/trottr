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
                        <button @click="currentTab = 'general'" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            currentTab === 'general'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Settings2 class="h-4 w-4" />
                            Général
                        </button>
                        <button @click="currentTab = 'jobs'" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            currentTab === 'jobs'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Map class="h-4 w-4" />
                            Interventions
                        </button>
                        <button @click="currentTab = 'users'" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            currentTab === 'users'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Users class="h-4 w-4" />
                            Utilisateurs
                        </button>
                        <button @click="currentTab = 'billing'" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            currentTab === 'billing'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <CreditCard class="h-4 w-4" />
                            Facturation
                        </button>
                        <button @click="currentTab = 'display'" :class="[
                            'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-2',
                            currentTab === 'display'
                                ? 'bg-primary text-neutral-100'
                                : 'text-neutral-600 hover:text-neutral-900 hover:bg-neutral-50'
                        ]">
                            <Monitor class="h-4 w-4" />
                            Affichage
                        </button>
                    </div>

                </nav>
            </div>

            <div class="flex-1 bg-white">
                <div class="p-6">
                    <SettingsGeneral v-if="currentTab === 'general'" />
                    <SettingsJob v-if="currentTab === 'jobs'" />
                    <SettingsUsers v-if="currentTab === 'users'" />
                    <SettingsBilling v-if="currentTab === 'billing'" />
                    <SettingsDisplay v-if="currentTab === 'display'" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import SettingsBilling from '@/main/components/settings/SettingsBilling.vue'
import SettingsDisplay from '@/main/components/settings/SettingsDisplay.vue'
import SettingsGeneral from '@/main/components/settings/SettingsGeneral.vue'
import SettingsJob from '@/main/components/settings/SettingsJob.vue'
import SettingsUsers from '@/main/components/settings/SettingsUsers.vue'
import { CreditCard, Map, Monitor, Settings2, Users } from 'lucide-vue-next'
import { ref } from 'vue'

const currentTab = ref('general')
</script>