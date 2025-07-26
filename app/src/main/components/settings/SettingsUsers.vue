<template>
    <div class="max-w-5xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Utilisateurs</h2>
            <p class="text-neutral-600">Gérez les utilisateurs de votre organisation.</p>
        </div>

        <div class="space-y-6">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-base font-medium text-neutral-900">Membres de l'équipe</h3>
                    <p class="text-sm text-neutral-500">{{ users.length }} utilisateur(s) actif(s)</p>
                </div>
                <Button>
                    <Plus class="h-4 w-4 mr-2" />
                    Inviter un utilisateur
                </Button>
            </div>

            <div class="border rounded-lg">
                <div class="p-4 border-b bg-neutral-50">
                    <div class="grid grid-cols-12 gap-4 text-sm font-medium text-neutral-700">
                        <div class="col-span-4">Utilisateur</div>
                        <div class="col-span-3">Rôle</div>
                        <div class="col-span-3">Statut</div>
                        <div class="col-span-2">Actions</div>
                    </div>
                </div>

                <div class="divide-y">
                    <div v-for="user in users" :key="user.id" class="p-4">
                        <div class="grid grid-cols-12 gap-4 items-center">
                            <div class="col-span-4">
                                <div class="flex items-center space-x-3">
                                    <div
                                        class="w-8 h-8 bg-neutral-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                                        {{ user.initials }}
                                    </div>
                                    <div>
                                        <p class="text-sm font-medium text-neutral-900">{{ user.name }}</p>
                                        <p class="text-xs text-neutral-500">{{ user.email }}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-span-3">
                                <Badge :class="getRoleBadgeClass(user.role)">
                                    {{ user.role }}
                                </Badge>
                            </div>
                            <div class="col-span-3">
                                <Badge :class="getStatusBadgeClass(user.status)">
                                    {{ user.status }}
                                </Badge>
                            </div>
                            <div class="col-span-2">
                                <div class="flex items-center space-x-1">
                                    <Button variant="ghost" size="sm">
                                        <Edit class="h-4 w-4" />
                                    </Button>
                                    <Button variant="ghost" size="sm" v-if="user.role !== 'Propriétaire'">
                                        <Trash class="h-4 w-4" />
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import { Edit, Plus, Trash } from 'lucide-vue-next'
import { ref } from 'vue'

const users = ref([
    {
        id: 1,
        name: 'Marc Dupont',
        email: 'marc.dupont@entreprise.com',
        initials: 'MD',
        role: 'Propriétaire',
        status: 'Actif'
    },
    {
        id: 2,
        name: 'Sophie Martin',
        email: 'sophie.martin@entreprise.com',
        initials: 'SM',
        role: 'Administrateur',
        status: 'Actif'
    },
    {
        id: 3,
        name: 'Pierre Leclerc',
        email: 'pierre.leclerc@entreprise.com',
        initials: 'PL',
        role: 'Technicien',
        status: 'Actif'
    },
    {
        id: 4,
        name: 'Julie Bernard',
        email: 'julie.bernard@entreprise.com',
        initials: 'JB',
        role: 'Lecture seule',
        status: 'Invité'
    }
])

const getRoleBadgeClass = (role) => {
    switch (role) {
        case 'Propriétaire': return 'bg-purple-100 text-purple-800'
        case 'Administrateur': return 'bg-blue-100 text-blue-800'
        case 'Technicien': return 'bg-green-100 text-green-800'
        case 'Lecture seule': return 'bg-neutral-100 text-neutral-800'
        default: return 'bg-neutral-100 text-neutral-800'
    }
}

const getStatusBadgeClass = (status) => {
    switch (status) {
        case 'Actif': return 'bg-green-100 text-green-800'
        case 'Invité': return 'bg-yellow-100 text-yellow-800'
        case 'Inactif': return 'bg-neutral-100 text-neutral-800'
        default: return 'bg-neutral-100 text-neutral-800'
    }
}
</script>