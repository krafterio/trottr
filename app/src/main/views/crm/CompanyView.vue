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
                            <h1 class="text-xl text-neutral-900 font-semibold">{{ company.name }}</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge variant="outline">
                                <Building class="h-4 w-4" />
                                {{ company.type }}
                            </Badge>
                            <Badge variant="outline" v-if="company.contractStatus">
                                <FileText class="h-4 w-4" />
                                {{ company.contractStatus }}
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
            <div class="w-80 bg-white border-r overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-lg font-semibold text-neutral-900 mb-4">Informations générales</h2>

                    <form @submit.prevent="saveCompany" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Raison sociale</label>
                            <Input v-model="companyForm.name" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Type de société</label>
                            <Select v-model="companyForm.type">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner un type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="Client final">Client final</SelectItem>
                                    <SelectItem value="Régie / gestionnaire">Régie / gestionnaire</SelectItem>
                                    <SelectItem value="Donneur d'ordre">Donneur d'ordre</SelectItem>
                                    <SelectItem value="Sous-traitant">Sous-traitant</SelectItem>
                                    <SelectItem value="Fournisseur">Fournisseur</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Référence interne</label>
                            <Input v-model="companyForm.internalRef" class="mt-1" placeholder="CLI-001" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Téléphone</label>
                            <Input v-model="companyForm.phone" class="mt-1" placeholder="01 42 33 44 55" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Email</label>
                            <Input v-model="companyForm.email" type="email" class="mt-1"
                                placeholder="contact@entreprise.fr" />
                        </div>

                        <Separator />

                        <div>
                            <label class="text-sm font-medium text-neutral-700">SIRET</label>
                            <Input v-model="companyForm.siret" class="mt-1" placeholder="12345678901234" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">TVA</label>
                            <Input v-model="companyForm.tva" class="mt-1" placeholder="FR12345678901" />
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
                                    <h1 class="text-2xl font-semibold">{{ company.name }}</h1>
                                    <p class="text-neutral-600">{{ company.type }}
                                    </p>
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
                                <MapPinIcon class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ kpis.totalContacts }}</p>
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
                                        <span class="text-sm text-neutral-600">{{ company.phone }}</span>
                                    </div>
                                    <div class="flex items-center space-x-2">
                                        <Mail class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ company.email }}</span>
                                    </div>

                                    <Badge v-if="company.contractStatus"
                                        class="flex items-center space-x-1 bg-green-50 text-green-800">
                                        <CheckCircle class="h-4 w-4 text-green-500" />
                                        <span class="text-sm">{{ company.contractStatus }}</span>
                                    </Badge>
                                </div>
                                <div class="flex gap-2">
                                    <Button size="sm" variant="outline">
                                        <FileText class="h-3 w-3" />
                                        Générer rapport de situation
                                    </Button>
                                    <Button size="sm">
                                        <Plus class="h-3 w-3" />
                                        Nouveau contrat
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
                            <TabsTrigger value="contacts">Contacts</TabsTrigger>
                            <TabsTrigger value="contrats">Contrats</TabsTrigger>
                            <TabsTrigger value="interventions">Interventions</TabsTrigger>
                            <TabsTrigger value="documents">Documents</TabsTrigger>
                        </TabsList>

                        <TabsContent value="sites">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Sites d'intervention</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter un site
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
                                                    Type de site
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Relation
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Adresse
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="site in sites" :key="site.id" class="hover:bg-neutral-50">
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{ site.label }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ site.type }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ site.relation }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ site.address }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <Button variant="ghost" size="sm">
                                                        <Edit class="h-4 w-4" />
                                                    </Button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="contacts">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Contacts rattachés</h2>
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
                                                    Nom / Prénom
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Fonction
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
                                                    Préférences
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="contact in contacts" :key="contact.id"
                                                class="hover:bg-neutral-50">
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{
                                                        contact.firstName }} {{ contact.lastName }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contact.position }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contact.phone }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contact.email }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contact.preferences }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <Button variant="ghost" size="sm">
                                                        <Edit class="h-4 w-4" />
                                                    </Button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="contrats">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Contrats</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Nouveau contrat
                                    </Button>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50 border-b">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Référence
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Type
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Date début
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Date fin
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Statut
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="contract in contracts" :key="contract.id"
                                                class="hover:bg-neutral-50">
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{
                                                        contract.reference }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contract.type }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contract.startDate }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ contract.endDate }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <span :class="[
                                                        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                                        contract.status.bgColor,
                                                        contract.status.textColor
                                                    ]">
                                                        {{ contract.status.label }}
                                                    </span>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <Button variant="ghost" size="sm">
                                                        <Edit class="h-4 w-4" />
                                                    </Button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="interventions">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Historique des interventions</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Nouvelle intervention
                                    </Button>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50 border-b">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Référence
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Type
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Date
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Technicien
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Statut
                                                </th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                                    Actions
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody class="bg-white divide-y divide-neutral-200">
                                            <tr v-for="intervention in interventions" :key="intervention.id"
                                                class="hover:bg-neutral-50 cursor-pointer"
                                                @click="$router.push(`/job/${intervention.ref}`)">
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm font-medium text-neutral-900">{{
                                                        intervention.ref }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ intervention.type }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ intervention.date }}</div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <div class="text-sm text-neutral-900">{{ intervention.technician }}
                                                    </div>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap">
                                                    <span :class="[
                                                        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                                                        intervention.status.bgColor,
                                                        intervention.status.textColor
                                                    ]">
                                                        {{ intervention.status.label }}
                                                    </span>
                                                </td>
                                                <td class="px-4 py-3 whitespace-nowrap" @click.stop>
                                                    <Button variant="ghost" size="sm">
                                                        <Eye class="h-4 w-4" />
                                                    </Button>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="documents">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Documents</h2>
                                    <Button>
                                        <Upload class="h-4 w-4" />
                                        Charger un document
                                    </Button>
                                </div>

                                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                    <div v-for="document in documents" :key="document.id"
                                        class="border rounded-lg p-4 hover:bg-neutral-50 cursor-pointer">
                                        <div class="flex items-start space-x-3">
                                            <div
                                                class="w-10 h-10 bg-neutral-100 rounded-lg flex items-center justify-center">
                                                <FileText class="h-5 w-5 text-neutral-600" />
                                            </div>
                                            <div class="flex-1 min-w-0">
                                                <p class="text-sm font-medium text-neutral-900 truncate">{{
                                                    document.name }}</p>
                                                <p class="text-xs text-neutral-500">{{ document.type }}</p>
                                                <p class="text-xs text-neutral-500">{{ document.uploadDate }}</p>
                                            </div>
                                        </div>
                                    </div>
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
import Input from '@/common/components/ui/input/Input.vue'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import Separator from '@/common/components/ui/separator/Separator.vue'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import {
    ArrowLeft,
    Building,
    CheckCircle,
    ChevronDown,
    Edit,
    Eye,
    FileText,
    FolderOpen,
    Mail,
    MapPin,
    MapPinIcon,
    MessageSquare,
    Phone,
    Plus,
    Upload
} from 'lucide-vue-next'
import { reactive } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const companyId = route.params.id

const company = {
    id: companyId,
    name: 'SARL Martin',
    type: 'Client final',
    siret: '12345678901234',
    tva: 'FR12345678901',
    internalRef: 'CLI-001',
    address: '15 rue de la République, 75001 Paris',
    phone: '01 42 33 44 55',
    email: 'contact@sarl-martin.fr',
    createdAt: '2023-01-15',
    status: {
        label: 'Active',
        bgColor: 'bg-green-100',
        textColor: 'text-green-800'
    },
    contractStatus: 'Contrat actif'
}

const companyForm = reactive({
    name: company.name,
    type: company.type,
    siret: company.siret,
    tva: company.tva,
    internalRef: company.internalRef,
    address: company.address,
    phone: company.phone,
    email: company.email,
    createdAt: company.createdAt
})

const kpis = {
    totalInterventions: 24,
    activeContracts: 2,
    totalContacts: 3,
    totalDocuments: 8
}

const saveCompany = () => {
    console.log('Sauvegarde des données:', companyForm)
}

const resetForm = () => {
    Object.assign(companyForm, {
        name: company.name,
        type: company.type,
        siret: company.siret,
        tva: company.tva,
        internalRef: company.internalRef,
        address: company.address,
        phone: company.phone,
        email: company.email,
        createdAt: company.createdAt
    })
}

const sites = [
    {
        id: 1,
        label: 'Siège social',
        type: 'Bâtiment tertiaire',
        relation: 'Propriétaire',
        address: '15 rue de la République, 75001 Paris'
    },
    {
        id: 2,
        label: 'Entrepôt',
        type: 'Industriel',
        relation: 'Locataire',
        address: '45 avenue des Industries, 94200 Ivry-sur-Seine'
    }
]

const contacts = [
    {
        id: 1,
        firstName: 'Jean',
        lastName: 'Martin',
        position: 'Directeur général',
        phone: '01 42 33 44 55',
        email: 'j.martin@sarl-martin.fr',
        preferences: 'Email + SMS'
    },
    {
        id: 2,
        firstName: 'Sophie',
        lastName: 'Dubois',
        position: 'Responsable maintenance',
        phone: '01 42 33 44 56',
        email: 's.dubois@sarl-martin.fr',
        preferences: 'Téléphone uniquement'
    }
]

const contracts = [
    {
        id: 1,
        reference: 'CTR-2024-001',
        type: 'Maintenance préventive',
        startDate: '01/01/2024',
        endDate: '31/12/2024',
        status: {
            label: 'Actif',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    }
]

const interventions = [
    {
        id: 1,
        ref: 'TR42K8',
        type: 'Maintenance préventive',
        date: '26/07/2025',
        technician: 'Jean Martin',
        status: {
            label: 'Terminée',
            bgColor: 'bg-green-100',
            textColor: 'text-green-800'
        }
    },
    {
        id: 2,
        ref: 'TR43L9',
        type: 'Dépannage',
        date: '15/07/2025',
        technician: 'Sophie Dubois',
        status: {
            label: 'En cours',
            bgColor: 'bg-orange-100',
            textColor: 'text-orange-800'
        }
    }
]

const documents = [
    {
        id: 1,
        name: 'KBIS SARL Martin.pdf',
        type: 'PDF',
        uploadDate: '15/01/2024'
    },
    {
        id: 2,
        name: 'Contrat maintenance 2024.pdf',
        type: 'PDF',
        uploadDate: '01/01/2024'
    },
    {
        id: 3,
        name: 'Cahier des charges.pdf',
        type: 'PDF',
        uploadDate: '10/12/2023'
    }
]
</script>