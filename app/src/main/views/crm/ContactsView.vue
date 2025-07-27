<template>
    <div class="h-full flex flex-col">
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between" :class="showKpis ? 'mb-4' : 'mb-0'">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Contacts</h1>
                    <p class="text-neutral-600">Gestion des contacts</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2 bg-accent rounded-md p-2 h-9">
                        <p class="text-sm text-neutral-600">Afficher KPIs</p>
                        <Switch v-model="showKpis" />
                    </div>
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Nouveau contact
                    </Button>
                </div>
            </div>

            <div v-show="showKpis" class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Users class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Total</p>
                        <p class="text-lg font-semibold text-neutral-900">284</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Building class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Sociétés</p>
                        <p class="text-lg font-semibold text-neutral-900">147</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <UserCheck class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Particuliers</p>
                        <p class="text-lg font-semibold text-neutral-900">137</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Star class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Décideurs</p>
                        <p class="text-lg font-semibold text-neutral-900">89</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div class="w-64 bg-neutral-50 border-r p-4 overflow-y-auto">
                <h3 class="font-semibold text-neutral-900 mb-4">Filtres</h3>

                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Type</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Société</span>
                            <span class="ml-auto text-xs text-neutral-400">147</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Particulier</span>
                            <span class="ml-auto text-xs text-neutral-400">137</span>
                        </label>
                    </div>
                </div>

                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Rôle</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Occupant</span>
                            <span class="ml-auto text-xs text-neutral-400">89</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Responsable site</span>
                            <span class="ml-auto text-xs text-neutral-400">65</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Contact facturation</span>
                            <span class="ml-auto text-xs text-neutral-400">45</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Chargé d'exploitation</span>
                            <span class="ml-auto text-xs text-neutral-400">34</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Gardien / Agent local</span>
                            <span class="ml-auto text-xs text-neutral-400">28</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Décideur</span>
                            <span class="ml-auto text-xs text-neutral-400">89</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Propriétaire</span>
                            <span class="ml-auto text-xs text-neutral-400">52</span>
                        </label>
                    </div>
                </div>

                <Button variant="outline" size="sm" class="w-full">
                    <RotateCcw class="h-4 w-4 mr-2" />
                    Réinitialiser
                </Button>
            </div>

            <div class="flex-1 overflow-y-auto">
                <div class="">
                    <div class="px-6 py-4 border-b">
                        <div class="flex items-center justify-between">
                            <div class="relative">
                                <Search
                                    class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
                                <Input type="text" placeholder="Recherche rapide..." class="h-9 pl-10 pr-4 py-2 w-64" />
                            </div>

                            <div class="flex items-center space-x-3">
                                <span class="text-sm text-muted-foreground">284 contacts</span>

                                <Button variant="outline" size="sm" class="w-8">
                                    <MoreVertical class="h-4 w-4" />
                                </Button>
                                <Button variant="outline">
                                    <Columns class="h-4 w-4" />
                                    Colonnes
                                    <ChevronDown class="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-neutral-50 border-b">
                                <tr>
                                    <th
                                        class="px-3 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider max-w-5">
                                        <Checkbox />
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Nom / Prénom
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Société
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Email
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Téléphone mobile
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Téléphone fixe
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Fonction
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Rôle
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr v-for="contact in contacts" :key="contact.id"
                                    class="hover:bg-neutral-50 cursor-pointer"
                                    @click="$router.push(`/contact/${contact.id}`)">
                                    <td class="px-3 py-2 whitespace-nowrap max-w-5" @click.stop>
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm font-medium text-neutral-900">{{ contact.firstName }} {{
                                            contact.lastName }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ contact.company || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ contact.email }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ contact.mobilePhone || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ contact.fixedPhone || '-' }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ contact.function }}</div>
                                    </td>
                                    <td class="px-6 py-2 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">{{ contact.roles.join(', ') }}</div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <TablePagination :current-page="1" :total-pages="15" :total-items="284" :items-per-page="20"
            position-classes="bottom-0 left-80 right-0" @page-change="handlePageChange"
            @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import Input from '@/common/components/ui/input/Input.vue'
import { Switch } from '@/common/components/ui/switch'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    Building,
    ChevronDown,
    Columns,
    Download,
    MoreVertical,
    Plus,
    RotateCcw,
    Search,
    Star,
    UserCheck,
    Users
} from 'lucide-vue-next'
import { ref } from 'vue'

const showKpis = ref(false)

const contacts = [
    {
        id: 1,
        firstName: 'Jean',
        lastName: 'Martin',
        company: 'SARL Martin',
        email: 'j.martin@sarl-martin.fr',
        mobilePhone: '06 12 34 56 78',
        fixedPhone: '01 42 33 44 55',
        function: 'Directeur général',
        roles: ['Décideur', 'Contact facturation']
    },
    {
        id: 2,
        firstName: 'Sophie',
        lastName: 'Dubois',
        company: 'Hotel Plaza',
        email: 's.dubois@hotelplaza.fr',
        mobilePhone: '06 23 45 67 89',
        fixedPhone: null,
        function: 'Responsable maintenance',
        roles: ['Responsable site']
    },
    {
        id: 3,
        firstName: 'Pierre',
        lastName: 'Leclerc',
        company: 'Café Central',
        email: 'p.leclerc@cafecentral.fr',
        mobilePhone: '06 34 56 78 90',
        fixedPhone: '01 47 88 92 34',
        function: 'Manager',
        roles: ['Décideur', 'Chargé d\'exploitation']
    },
    {
        id: 4,
        firstName: 'Marie',
        lastName: 'Rousseau',
        company: 'Boulangerie Paul',
        email: 'm.rousseau@boulangerie-paul.fr',
        mobilePhone: null,
        fixedPhone: '01 53 67 89 01',
        function: 'Responsable qualité',
        roles: ['Chargé d\'exploitation']
    },
    {
        id: 5,
        firstName: 'Antoine',
        lastName: 'Bernard',
        company: 'Garage Moderne',
        email: 'a.bernard@garage-moderne.fr',
        mobilePhone: '06 45 67 89 01',
        fixedPhone: '01 48 95 73 26',
        function: 'Technicien',
        roles: ['Occupant']
    },
    {
        id: 6,
        firstName: 'François',
        lastName: 'Lambert',
        company: 'Clinique Pasteur',
        email: 'f.lambert@clinique-pasteur.fr',
        mobilePhone: '06 56 78 90 12',
        fixedPhone: '01 44 82 67 39',
        function: 'Directeur technique',
        roles: ['Décideur', 'Responsable site']
    },
    {
        id: 7,
        firstName: 'Sylvie',
        lastName: 'Moreau',
        company: 'Restaurant Le Petit Zinc',
        email: 's.moreau@petitzinc.fr',
        mobilePhone: '06 67 89 01 23',
        fixedPhone: '01 49 73 84 52',
        function: 'Gérante',
        roles: ['Propriétaire', 'Décideur']
    },
    {
        id: 8,
        firstName: 'Thomas',
        lastName: 'Durand',
        company: 'Pharmacie de la Paix',
        email: 't.durand@pharmacie-paix.fr',
        mobilePhone: '06 78 90 12 34',
        fixedPhone: '01 56 91 42 78',
        function: 'Pharmacien',
        roles: ['Contact facturation', 'Décideur']
    },
    {
        id: 9,
        firstName: 'Isabelle',
        lastName: 'Moreau',
        company: null,
        email: 'i.moreau@gmail.com',
        mobilePhone: '06 89 01 23 45',
        fixedPhone: '01 43 87 65 21',
        function: 'Ingénieure',
        roles: ['Occupant']
    },
    {
        id: 10,
        firstName: 'Laurent',
        lastName: 'Petit',
        company: 'Société Générale du Bâtiment',
        email: 'l.petit@sgb.fr',
        mobilePhone: '06 90 12 34 56',
        fixedPhone: '01 48 52 73 94',
        function: 'Chef de projet',
        roles: ['Chargé d\'exploitation', 'Responsable site']
    },
    {
        id: 11,
        firstName: 'Julie',
        lastName: 'Moreau',
        company: null,
        email: 'julie.moreau@free.fr',
        mobilePhone: '06 11 22 33 44',
        fixedPhone: null,
        function: 'Résidente',
        roles: ['Occupant']
    },
    {
        id: 12,
        firstName: 'Paul',
        lastName: 'Gardien',
        company: 'Résidence Les Acacias',
        email: 'p.gardien@acacias.fr',
        mobilePhone: '06 55 66 77 88',
        fixedPhone: '01 23 45 67 89',
        function: 'Gardien',
        roles: ['Gardien / Agent local']
    }
]

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>