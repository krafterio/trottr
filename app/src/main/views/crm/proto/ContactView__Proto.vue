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
                            <h1 class="text-xl text-neutral-900 font-semibold">{{ contact.firstName }} {{
                                contact.lastName }}</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge variant="outline">
                                <User class="h-4 w-4" />
                                {{ contact.function }}
                            </Badge>
                            <Badge variant="outline" v-if="contact.company">
                                <Building class="h-4 w-4" />
                                {{ contact.company }}
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

                    <form @submit.prevent="saveContact" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Prénom</label>
                            <Input v-model="contactForm.firstName" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Nom</label>
                            <Input v-model="contactForm.lastName" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Fonction</label>
                            <Input v-model="contactForm.function" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Rôle</label>
                            <Select v-model="contactForm.roles">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner les rôles" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="occupant">Occupant</SelectItem>
                                    <SelectItem value="responsable-site">Responsable site</SelectItem>
                                    <SelectItem value="contact-facturation">Contact facturation</SelectItem>
                                    <SelectItem value="charge-exploitation">Chargé d'exploitation</SelectItem>
                                    <SelectItem value="gardien-agent">Gardien / Agent local</SelectItem>
                                    <SelectItem value="decideur">Décideur</SelectItem>
                                    <SelectItem value="proprietaire">Propriétaire</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Société</label>
                            <Combobox v-model="contactForm.company" class="mt-1">
                                <ComboboxAnchor as-child>
                                    <ComboboxTrigger as-child>
                                        <Button variant="outline" class="justify-between w-full">
                                            <span>{{ getDisplayValue(contactForm.company) }}</span>
                                            <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                                        </Button>
                                    </ComboboxTrigger>
                                </ComboboxAnchor>

                                <ComboboxList class="w-88">
                                    <div class="relative w-full max-w-sm items-center">
                                        <ComboboxInput class="focus-visible:ring-0 border-0 rounded-none h-10 pl-2"
                                            placeholder="Rechercher..." />
                                        <span class="absolute start-0 inset-y-0 flex items-center justify-center px-3">
                                            <Search class="size-4 text-muted-foreground" />
                                        </span>
                                    </div>

                                    <ComboboxEmpty>
                                        Aucun résultat trouvé
                                    </ComboboxEmpty>

                                    <ComboboxGroup>
                                        <ComboboxItem v-for="company in companies" :key="company.id" :value="company">
                                            <Building class="mr-2 h-4 w-4" />
                                            {{ company.name }}
                                            <ComboboxItemIndicator>
                                                <Check class="ml-auto h-4 w-4" />
                                            </ComboboxItemIndicator>
                                        </ComboboxItem>

                                        <ComboboxItem v-for="contact in contacts" :key="contact.id" :value="contact">
                                            <User class="mr-2 h-4 w-4" />
                                            {{ contact.firstName }} {{ contact.lastName }}
                                            <ComboboxItemIndicator>
                                                <Check class="ml-auto h-4 w-4" />
                                            </ComboboxItemIndicator>
                                        </ComboboxItem>
                                    </ComboboxGroup>
                                </ComboboxList>
                            </Combobox>
                        </div>

                        <Separator />

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Email</label>
                            <Input v-model="contactForm.email" type="email" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Téléphone mobile</label>
                            <Input v-model="contactForm.mobilePhone" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Téléphone fixe</label>
                            <Input v-model="contactForm.fixedPhone" class="mt-1" />
                        </div>
                    </form>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto">
                <div class="bg-white m-6 mb-4 rounded-lg border">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex items-start space-x-2">
                                <User class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                <div class="flex flex-col">
                                    <h1 class="text-2xl font-semibold">{{ contact.firstName }} {{ contact.lastName }}
                                    </h1>
                                    <p class="text-neutral-600">{{ contact.function }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 ps-11">
                            <div class="flex items-start space-x-3">
                                <MapPin class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalInterventions }}</p>
                                    <p class="text-xs text-neutral-500">Interventions totales</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <FileText class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.activeContracts }}</p>
                                    <p class="text-xs text-neutral-500">Contrats actifs</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <Building class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalSites }}</p>
                                    <p class="text-xs text-neutral-500">Sites rattachés</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <FolderOpen class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
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
                                        <Phone class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ contact.mobilePhone }}</span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <Mail class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ contact.email }}</span>
                                    </div>

                                    <Badge v-if="contact.company"
                                        class="flex items-center space-x-1 bg-blue-50 text-blue-800">
                                        <Building class="h-4 w-4 text-blue-500" />
                                        <span class="text-sm">{{ contact.company }}</span>
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
                    <Tabs default-value="sites" class="border-b p-4 py-3">
                        <TabsList>
                            <TabsTrigger value="sites">Sites</TabsTrigger>
                            <TabsTrigger value="equipements">Équipements</TabsTrigger>
                            <TabsTrigger value="contrats">Contrats</TabsTrigger>
                            <TabsTrigger value="interventions">Interventions</TabsTrigger>
                            <TabsTrigger value="documents">Documents</TabsTrigger>
                        </TabsList>

                        <TabsContent value="sites">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Sites rattachés</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Rattacher un site
                                    </Button>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50 border-b">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Libellé
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Adresse
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Type relation
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Type bâtiment
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="site in contactSites" :key="site.id" class="hover:bg-neutral-50">
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{ site.label }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ site.address }}</div>
                                                    <div class="text-sm text-neutral-500">{{ site.city }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Badge variant="outline">{{ site.relationType }}</Badge>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ site.buildingType }}</div>
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
                                                    Site
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Lot
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Marque / Modèle
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
                                            <tr v-for="equipment in contactEquipments" :key="equipment.id"
                                                class="hover:bg-neutral-50">
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{ equipment.name
                                                    }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Badge variant="outline">{{ equipment.type }}</Badge>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ equipment.site }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ equipment.lot || '-' }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ equipment.brand }}</div>
                                                    <div class="text-sm text-neutral-500">{{ equipment.model }}</div>
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

                        <TabsContent value="contrats">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Contrats</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Nouveau contrat
                                    </Button>
                                </div>
                                <div class="text-center py-8 text-neutral-500">
                                    <FileText class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
                                    <p>Aucun contrat pour ce contact</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="interventions">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Historique des interventions</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Nouvelle intervention
                                    </Button>
                                </div>
                                <div class="text-center py-8 text-neutral-500">
                                    <MapPin class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
                                    <p>Aucune intervention pour ce contact</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="documents">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Documents</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter document
                                    </Button>
                                </div>
                                <div class="text-center py-8 text-neutral-500">
                                    <FolderOpen class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
                                    <p>Aucun document pour ce contact</p>
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
import { Combobox, ComboboxAnchor, ComboboxEmpty, ComboboxGroup, ComboboxInput, ComboboxItem, ComboboxItemIndicator, ComboboxList, ComboboxTrigger } from '@/common/components/ui/combobox'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import {
    ArrowLeft,
    Building,
    Check,
    ChevronDown,
    ChevronsUpDown,
    FileText,
    FolderOpen,
    Mail,
    MapPin,
    MessageSquare,
    MoreVertical,
    Phone,
    Plus,
    Search,
    User
} from 'lucide-vue-next'
import { reactive } from 'vue'

const contact = {
    id: 1,
    firstName: 'Pierre',
    lastName: 'Dupont',
    function: 'Responsable maintenance',
    company: 'SARL Immobilier Plus',
    email: 'pierre.dupont@immobilier-plus.fr',
    mobilePhone: '06 12 34 56 78',
    fixedPhone: '01 23 45 67 89',
    roles: ['responsable-site', 'decideur'],
    createdAt: '2023-01-15'
}

const contactForm = reactive({
    firstName: contact.firstName,
    lastName: contact.lastName,
    function: contact.function,
    roles: contact.roles,
    company: contact.company,
    email: contact.email,
    mobilePhone: contact.mobilePhone,
    fixedPhone: contact.fixedPhone,
    createdAt: contact.createdAt
})

const kpis = {
    totalInterventions: 12,
    activeContracts: 2,
    totalSites: 3,
    totalDocuments: 8
}

const contactSites = [
    {
        id: 1,
        label: 'Résidence Les Jardins',
        address: '15 rue des Lilas, 75015',
        city: 'Paris',
        relationType: 'Responsable site',
        buildingType: 'Résidence collective'
    },
    {
        id: 2,
        label: 'Villa Dupont',
        address: '8 avenue de la Paix, 69003',
        city: 'Lyon',
        relationType: 'Propriétaire',
        buildingType: 'Maison individuelle'
    }
]

const companies = [
    { id: 1, name: 'SARL Immobilier Plus' },
    { id: 2, name: 'SCI Bellecour' },
    { id: 3, name: 'Syndic Moderne' },
    { id: 4, name: 'Office Management SA' },
    { id: 5, name: 'Gestimmo Nantes' }
]

const getDisplayValue = (value) => {
    if (!value) return 'Optionnel pour particuliers'
    if (typeof value === 'string') return value
    if (value.name) return value.name
    if (value.firstName && value.lastName) return `${value.firstName} ${value.lastName}`
    return 'Optionnel pour particuliers'
}

const saveContact = () => {
    console.log('Saving contact:', contactForm)
}

const contactEquipments = [
    {
        id: 1,
        name: 'Chaudière lot A101',
        type: 'Chauffage',
        site: 'Résidence Les Jardins',
        lot: 'A101',
        brand: 'Chaffoteaux',
        model: 'Niagara C Green',
        status: 'Fonctionnel'
    },
    {
        id: 2,
        name: 'Climatiseur bureau',
        type: 'Climatisation',
        site: 'Villa Dupont',
        lot: null,
        brand: 'Daikin',
        model: 'Sensira FTXC25B',
        status: 'Maintenance requise'
    }
]

const resetForm = () => {
    Object.assign(contactForm, {
        firstName: contact.firstName,
        lastName: contact.lastName,
        function: contact.function,
        roles: contact.roles,
        company: contact.company,
        email: contact.email,
        mobilePhone: contact.mobilePhone,
        fixedPhone: contact.fixedPhone,
        createdAt: contact.createdAt
    })
}
</script>