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
                            <h1 class="text-xl text-neutral-900 font-semibold">{{ site.label }}</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge variant="outline">
                                <Building class="h-4 w-4" />
                                {{ site.buildingType }}
                            </Badge>
                            <Badge variant="outline" v-if="site.attachedTo">
                                <User class="h-4 w-4" />
                                {{ site.attachedTo }}
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

                    <form @submit.prevent="saveSite" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Libellé</label>
                            <Input v-model="siteForm.label" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Type de bâtiment</label>
                            <Select v-model="siteForm.buildingType">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner le type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="residence-collective">Résidence collective</SelectItem>
                                    <SelectItem value="maison-individuelle">Maison individuelle</SelectItem>
                                    <SelectItem value="batiment-tertiaire">Bâtiment tertiaire</SelectItem>
                                    <SelectItem value="local-commercial">Local commercial</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Rattaché à</label>
                            <Combobox v-model="siteForm.attachedTo" class="mt-1">
                                <ComboboxAnchor as-child>
                                    <ComboboxTrigger as-child>
                                        <Button variant="outline" class="justify-between w-full">
                                            <span>{{ getDisplayValue(siteForm.attachedTo) }}</span>
                                            <ChevronsUpDown class="ml-2 h-4 w-4 shrink-0 opacity-50" />
                                        </Button>
                                    </ComboboxTrigger>
                                </ComboboxAnchor>

                                <ComboboxList class="w-88">
                                    <div class="relative w-full max-w-sm items-center">
                                        <ComboboxInput class="focus-visible:ring-0 border-0  rounded-none h-10 pl-2"
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
                            <label class="text-sm font-medium text-neutral-700">Rue</label>
                            <Input v-model="siteForm.street" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Code postal</label>
                            <Input v-model="siteForm.zipCode" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Ville</label>
                            <Input v-model="siteForm.city" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Pays</label>
                            <Select v-model="siteForm.country">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner le pays" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="france">France</SelectItem>
                                    <SelectItem value="belgique">Belgique</SelectItem>
                                    <SelectItem value="suisse">Suisse</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Informations d'accès</label>
                            <Textarea v-model="siteForm.accessInfo" class="mt-1"
                                placeholder="Codes, instructions particulières..." />
                        </div>
                    </form>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto">
                <div class="bg-white m-6 mb-4 rounded-lg border">
                    <div class="p-6">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex items-start space-x-2">
                                <MapPin class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                <div class="flex flex-col">
                                    <h1 class="text-2xl font-semibold">{{ site.label }}</h1>
                                    <p class="text-neutral-600">{{ site.buildingType }}</p>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 ps-11">
                            <div class="flex items-start space-x-3">
                                <Building class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalLots }}</p>
                                    <p class="text-xs text-neutral-500">Lots</p>
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
                                        <MapPin class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ site.fullAddress }}</span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <User class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ site.attachedTo }}</span>
                                    </div>

                                    <Badge v-if="site.contract"
                                        class="flex items-center space-x-1 bg-green-50 text-green-800">
                                        <FileText class="h-4 w-4 text-green-500" />
                                        <span class="text-sm">{{ site.contract }}</span>
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
                    <Tabs default-value="lots" class="border-b p-4 py-3">
                        <TabsList>
                            <TabsTrigger value="lots">Lots</TabsTrigger>
                            <TabsTrigger value="equipements">Équipements</TabsTrigger>
                        </TabsList>

                        <TabsContent value="lots">
                            <div class="p-2">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Lots</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter un lot
                                    </Button>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50 border-b">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Numéro
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Type
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Description
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Surface (m²)
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Propriétaire
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="lot in siteLots" :key="lot.id" class="hover:bg-neutral-50">
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{ lot.number }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <Badge variant="outline">{{ lot.type }}</Badge>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ lot.description }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ lot.surface || '-' }}</div>
                                                </td>
                                                <td class="px-4 py-4 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ lot.owner || '-' }}</div>
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
                                            <tr v-for="equipment in siteEquipments" :key="equipment.id"
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
import { Combobox, ComboboxAnchor, ComboboxEmpty, ComboboxGroup, ComboboxInput, ComboboxItem, ComboboxItemIndicator, ComboboxList, ComboboxTrigger } from '@/common/components/ui/combobox'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { Textarea } from '@/common/components/ui/textarea'
import {
    ArrowLeft,
    Building,
    Check,
    ChevronDown,
    ChevronsUpDown,
    FileText,
    MapPin,
    MessageSquare,
    MoreVertical,
    Plus,
    Search,
    User,
    Wrench
} from 'lucide-vue-next'
import { reactive } from 'vue'

const site = {
    id: 1,
    label: 'Résidence Les Jardins',
    buildingType: 'Résidence collective',
    attachedTo: 'SARL Immobilier Plus',
    street: '15 rue des Lilas',
    zipCode: '75015',
    city: 'Paris',
    country: 'France',
    fullAddress: '15 rue des Lilas, 75015 Paris',
    lotCount: 45,
    accessInfo: 'Code portail: 1234A, Interphone gardien: *123',
    contract: 'CTR-2024-001'
}

const siteForm = reactive({
    label: site.label,
    buildingType: site.buildingType,
    attachedTo: site.attachedTo,
    street: site.street,
    zipCode: site.zipCode,
    city: site.city,
    country: site.country,
    lotCount: site.lotCount,
    accessInfo: site.accessInfo
})

const kpis = {
    totalLots: 45,
    totalEquipments: 12,
    totalInterventions: 28,
    totalDocuments: 15
}

const siteLots = [
    {
        id: 1,
        number: 'A101',
        type: 'Appartement',
        description: '3 pièces, 2ème étage',
        surface: 65,
        owner: 'M. Martin Pierre'
    },
    {
        id: 2,
        number: 'A102',
        type: 'Appartement',
        description: '2 pièces, 2ème étage',
        surface: 45,
        owner: 'Mme Dubois Claire'
    },
    {
        id: 3,
        number: 'B201',
        type: 'Appartement',
        description: '4 pièces, 1er étage',
        surface: 85,
        owner: null
    }
]

const siteEquipments = [
    {
        id: 1,
        name: 'Ascenseur principal',
        type: 'Ascenseur',
        brand: 'OTIS',
        model: 'Gen2 Comfort',
        location: 'Hall d\'entrée',
        status: 'Fonctionnel'
    },
    {
        id: 2,
        name: 'Chaudière collective',
        type: 'Chauffage',
        brand: 'Viessmann',
        model: 'Vitocrossal 300',
        location: 'Sous-sol technique',
        status: 'Maintenance requise'
    },
    {
        id: 3,
        name: 'Portail automatique',
        type: 'Sécurité',
        brand: 'CAME',
        model: 'BX78',
        location: 'Entrée parking',
        status: 'En panne'
    }
]

const companies = [
    { id: 1, name: 'SARL Immobilier Plus' },
    { id: 2, name: 'SCI Bellecour' },
    { id: 3, name: 'Syndic Moderne' },
    { id: 4, name: 'Office Management SA' },
    { id: 5, name: 'Gestimmo Nantes' }
]

const contacts = [
    { id: 1, firstName: 'Pierre', lastName: 'Dupont' },
    { id: 2, firstName: 'Claire', lastName: 'Martin' },
    { id: 3, firstName: 'Jean', lastName: 'Rochefort' },
    { id: 4, firstName: 'Marie', lastName: 'Dubois' }
]

const getDisplayValue = (value) => {
    if (!value) return 'Sélectionner société ou contact'
    if (typeof value === 'string') return value
    if (value.name) return value.name
    if (value.firstName && value.lastName) return `${value.firstName} ${value.lastName}`
    return 'Sélectionner société ou contact'
}

const saveSite = () => {
    console.log('Saving site:', siteForm)
}
</script>