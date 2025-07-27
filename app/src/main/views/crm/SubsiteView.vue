<template>
    <div class="h-full flex flex-col bg-neutral-100">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <Button variant="outline" @click="$router.go(-1)" class="h-9 w-9">
                        <ArrowLeft :size="20" />
                    </Button>
                    <div class="flex flex-col gap-1">
                        <div class="flex items-center space-x-3">
                            <h1 class="text-xl text-neutral-900 font-semibold">{{ lot.number }}</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge variant="outline">
                                <Building class="h-4 w-4" />
                                {{ lot.type }}
                            </Badge>
                            <Badge variant="outline" v-if="lot.site">
                                <MapPin class="h-4 w-4" />
                                {{ lot.site }}
                            </Badge>
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <MessageSquare class="h-4 w-4" />
                        Contacter
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Ajouter
                        <ChevronDown class="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div class="w-100 bg-white border-r overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-lg font-semibold text-neutral-900 mb-4">Informations générales</h2>

                    <form @submit.prevent="saveLot" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Libellé</label>
                            <Input v-model="lotForm.number" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Type de lot</label>
                            <Select v-model="lotForm.type">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner le type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="appartement">Appartement</SelectItem>
                                    <SelectItem value="local-commercial">Local commercial</SelectItem>
                                    <SelectItem value="parking">Parking</SelectItem>
                                    <SelectItem value="cave">Cave</SelectItem>
                                    <SelectItem value="bureau">Bureau</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Site rattaché</label>
                            <Select v-model="lotForm.site">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner le site" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="residence-jardins">Résidence Les Jardins</SelectItem>
                                    <SelectItem value="centre-bellecour">Centre Commercial Bellecour</SelectItem>
                                    <SelectItem value="immeuble-saint-michel">Immeuble Saint-Michel</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <Separator />

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Description</label>
                            <Input v-model="lotForm.description" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Surface (m²)</label>
                            <Input v-model="lotForm.surface" type="number" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Étage</label>
                            <Input v-model="lotForm.floor" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Informations complémentaires</label>
                            <Textarea v-model="lotForm.additionalInfo" class="mt-1"
                                placeholder="Informations particulières, accès..." />
                        </div>
                    </form>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto">
                <div class="bg-white m-6 mb-4 rounded-lg border">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex items-start space-x-2">
                                <Building class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                <div class="flex flex-col">
                                    <h1 class="text-2xl font-semibold">{{ lot.number }}</h1>
                                    <p class="text-neutral-600">{{ lot.type }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 ps-11">
                            <div class="flex items-start space-x-3">
                                <User class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalContacts }}</p>
                                    <p class="text-xs text-neutral-500">Contacts</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <Wrench class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalEquipments }}</p>
                                    <p class="text-xs text-neutral-500">Équipements</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <MapPin class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalInterventions }}</p>
                                    <p class="text-xs text-neutral-500">Interventions</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <FileText class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalDocuments }}</p>
                                    <p class="text-xs text-neutral-500">Documents</p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-4 pt-4 border-t border-dashed ps-11">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="flex items-center space-x-2">
                                        <Building class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ lot.description }}</span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <MapPin class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ lot.site }}</span>
                                    </div>

                                    <Badge v-if="lot.surface"
                                        class="flex items-center space-x-1 bg-blue-50 text-blue-800">
                                        <span class="text-sm">{{ lot.surface }} m²</span>
                                    </Badge>
                                </div>
                                <div class="flex gap-2">
                                    <Button variant="outline">
                                        <FileText class="h-3 w-3" />
                                        Générer rapport de situation
                                    </Button>
                                    <Button>
                                        <Plus class="h-3 w-3" />
                                        Nouvelle intervention
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white m-6 mt-0 rounded-lg border">
                    <Tabs default-value="contacts" class="border-b p-4 py-3">
                        <TabsList>
                            <TabsTrigger value="contacts">Contacts</TabsTrigger>
                            <TabsTrigger value="equipements">Équipements</TabsTrigger>
                        </TabsList>

                        <TabsContent value="contacts">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Contacts</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter un contact
                                    </Button>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50 border-b">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Contact
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Rôle
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Téléphone
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Email
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="contact in lotContacts" :key="contact.id"
                                                class="hover:bg-neutral-50">
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{
                                                        contact.firstName }} {{ contact.lastName }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Badge variant="outline">{{ contact.role }}</Badge>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contact.phone || '-' }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contact.email || '-' }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Button variant="ghost" size="sm">
                                                        <MoreVertical class="h-4 w-4" />
                                                    </Button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="equipements">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Équipements</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter un équipement
                                    </Button>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50 border-b">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Équipement
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Type
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Marque / Modèle
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Localisation
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    État
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="equipment in lotEquipments" :key="equipment.id"
                                                class="hover:bg-neutral-50">
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{ equipment.name
                                                    }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Badge variant="outline">{{ equipment.type }}</Badge>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ equipment.brand }}</div>
                                                    <div class="text-sm text-neutral-500">{{ equipment.model }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ equipment.location }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Badge :class="equipment.status === 'Fonctionnel' ? 'bg-green-100 text-green-800' :
                                                        equipment.status === 'En panne' ? 'bg-red-100 text-red-800' :
                                                            'bg-yellow-100 text-yellow-800'">
                                                        {{ equipment.status }}
                                                    </Badge>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Button variant="ghost" size="sm">
                                                        <MoreVertical class="h-4 w-4" />
                                                    </Button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { Textarea } from '@/common/components/ui/textarea'
import {
    ArrowLeft,
    Building,
    ChevronDown,
    FileText,
    MapPin,
    MessageSquare,
    MoreVertical,
    Plus,
    User,
    Wrench
} from 'lucide-vue-next'
import { reactive } from 'vue'

const lot = {
    id: 1,
    number: 'A101',
    type: 'Appartement',
    description: '3 pièces, 2ème étage',
    surface: 65,
    site: 'Résidence Les Jardins',
    floor: '2ème étage',
    additionalInfo: 'Accès par escalier principal ou ascenseur'
}

const lotForm = reactive({
    number: lot.number,
    type: lot.type,
    description: lot.description,
    surface: lot.surface,
    site: lot.site,
    floor: lot.floor,
    additionalInfo: lot.additionalInfo
})

const kpis = {
    totalContacts: 2,
    totalEquipments: 3,
    totalInterventions: 8,
    totalDocuments: 4
}

const lotContacts = [
    {
        id: 1,
        firstName: 'Pierre',
        lastName: 'Martin',
        role: 'Propriétaire',
        phone: '06 12 34 56 78',
        email: 'pierre.martin@email.com'
    },
    {
        id: 2,
        firstName: 'Marie',
        lastName: 'Dubois',
        role: 'Occupant',
        phone: '06 98 76 54 32',
        email: 'marie.dubois@email.com'
    }
]

const lotEquipments = [
    {
        id: 1,
        name: 'Chauffe-eau électrique',
        type: 'Chauffage',
        brand: 'Atlantic',
        model: 'Zénéo ACI+',
        location: 'Salle de bain',
        status: 'Fonctionnel'
    },
    {
        id: 2,
        name: 'VMC simple flux',
        type: 'Ventilation',
        brand: 'Aldes',
        model: 'Bahia Compact',
        location: 'Plafond salle de bain',
        status: 'Maintenance requise'
    },
    {
        id: 3,
        name: 'Radiateur électrique',
        type: 'Chauffage',
        brand: 'Noirot',
        model: 'Calidou Smart',
        location: 'Salon',
        status: 'Fonctionnel'
    }
]

const saveLot = () => {
    console.log('Saving lot:', lotForm)
}
</script>