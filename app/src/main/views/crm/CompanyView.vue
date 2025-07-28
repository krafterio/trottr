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
                            <h1 class="text-xl text-neutral-900 font-semibold">{{ company.name || 'Chargement...' }}
                            </h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge variant="outline" v-if="company.company_type">
                                <Building class="h-4 w-4" />
                                {{ getCompanyTypeLabel(company.company_type) }}
                            </Badge>
                            <Badge variant="outline" v-if="company.siret">
                                <FileText class="h-4 w-4" />
                                SIRET: {{ company.siret }}
                            </Badge>
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline" v-if="company.email" @click="contactCompany">
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

        <div class="flex-1 flex overflow-hidden lg:flex-row flex-col">
            <div class="w-full lg:w-1/4 xl:w-[500px] bg-white border-r overflow-y-auto">
                <div class="p-6">
                    <h2 class="text-lg font-semibold text-neutral-900 mb-4">Informations générales</h2>

                    <form @submit.prevent="saveCompany" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Raison sociale</label>
                            <Input v-model="companyForm.name" class="mt-1" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Type de société</label>
                            <Select v-model="companyForm.company_type">
                                <SelectTrigger class="mt-1 w-full">
                                    <SelectValue placeholder="Sélectionner un type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem v-for="option in companyTypeOptions" :key="option.value"
                                        :value="option.value">
                                        {{ option.label }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Référence interne</label>
                            <Input v-model="companyForm.reference" class="mt-1" placeholder="CLI-001" />
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

                        <h3 class="text-md font-medium text-neutral-700">Adresse de facturation</h3>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Rue</label>
                            <Input v-model="companyForm.invoice_street" class="mt-1" placeholder="123 Rue de la Paix" />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Code postal</label>
                                <Input v-model="companyForm.invoice_zip" class="mt-1" placeholder="75001" />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Ville</label>
                                <Input v-model="companyForm.invoice_city" class="mt-1" placeholder="Paris" />
                            </div>
                        </div>

                        <Separator />

                        <div>
                            <label class="text-sm font-medium text-neutral-700">SIRET</label>
                            <Input v-model="companyForm.siret" class="mt-1" placeholder="12345678901234" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">TVA</label>
                            <Input v-model="companyForm.vat" class="mt-1" placeholder="FR12345678901" />
                        </div>

                        <div class="pt-4">
                            <Button type="submit" :disabled="loading">
                                {{ loading ? 'Sauvegarde...' : 'Sauvegarder' }}
                            </Button>
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
                                    <p class="text-neutral-600" v-if="company.company_type">
                                        {{ getCompanyTypeLabel(company.company_type) }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 ps-11">
                            <div class="flex items-start space-x-3">
                                <MapPin class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">-</p>
                                    <p class="text-xs text-neutral-500">Interventions totales</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <FileText class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">-</p>
                                    <p class="text-xs text-neutral-500">Contrats actifs</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <MapPinIcon class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">-</p>
                                    <p class="text-xs text-neutral-500">Sites rattachés</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <FolderOpen class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">-</p>
                                    <p class="text-xs text-neutral-500">Documents</p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-4 pt-4 border-t border-dashed ps-11">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="flex items-center space-x-2" v-if="company.phone">
                                        <Phone class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ company.phone }}</span>
                                    </div>
                                    <div class="flex items-center space-x-2" v-if="company.email">
                                        <Mail class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ company.email }}</span>
                                    </div>
                                    <div class="flex items-center space-x-2" v-if="company.invoice_city">
                                        <MapPin class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ company.invoice_city }}</span>
                                    </div>
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
                    <Tabs default-value="sites" class="border-b p-2 py-3">
                        <TabsList>
                            <TabsTrigger value="sites">Sites</TabsTrigger>
                            <TabsTrigger value="contacts">Contacts</TabsTrigger>
                            <TabsTrigger value="equipements">Équipements</TabsTrigger>
                            <TabsTrigger value="contrats">Contrats</TabsTrigger>
                            <TabsTrigger value="interventions">Interventions</TabsTrigger>
                            <TabsTrigger value="documents">Documents</TabsTrigger>
                        </TabsList>

                        <TabsContent value="sites">
                            <div class="p-6">
                                <div class="text-center py-8">
                                    <Building class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                    <h3 class="text-lg font-medium text-neutral-900 mb-2">Sites d'intervention</h3>
                                    <p class="text-neutral-600 mb-4">Cette section permettra de gérer les sites
                                        rattachés à cette entreprise.</p>
                                    <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des sites</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="contacts">
                            <div class="p-6">
                                <div class="text-center py-8">
                                    <Users class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                    <h3 class="text-lg font-medium text-neutral-900 mb-2">Contacts</h3>
                                    <p class="text-neutral-600 mb-4">Cette section permettra de gérer les contacts de
                                        l'entreprise.</p>
                                    <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des contacts</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="equipements">
                            <div class="p-6">
                                <div class="text-center py-8">
                                    <Settings class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                    <h3 class="text-lg font-medium text-neutral-900 mb-2">Équipements</h3>
                                    <p class="text-neutral-600 mb-4">Cette section permettra de gérer les équipements de
                                        l'entreprise.</p>
                                    <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des équipements</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="contrats">
                            <div class="p-6">
                                <div class="text-center py-8">
                                    <FileText class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                    <h3 class="text-lg font-medium text-neutral-900 mb-2">Contrats</h3>
                                    <p class="text-neutral-600 mb-4">Cette section permettra de gérer les contrats de
                                        l'entreprise.</p>
                                    <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des contrats</p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="interventions">
                            <div class="p-6">
                                <div class="text-center py-8">
                                    <Wrench class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                    <h3 class="text-lg font-medium text-neutral-900 mb-2">Interventions</h3>
                                    <p class="text-neutral-600 mb-4">Cette section permettra de consulter les
                                        interventions liées à cette entreprise.</p>
                                    <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des interventions
                                    </p>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="documents">
                            <div class="p-6">
                                <div class="text-center py-8">
                                    <FolderOpen class="h-12 w-12 text-neutral-400 mx-auto mb-4" />
                                    <h3 class="text-lg font-medium text-neutral-900 mb-2">Documents</h3>
                                    <p class="text-neutral-600 mb-4">Cette section permettra de gérer les documents de
                                        l'entreprise.</p>
                                    <p class="text-sm text-neutral-500">TODO: Implémenter la gestion des documents</p>
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
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { useFetcher } from '@/common/composables/fetcher'
import { useCompany } from '@/common/composables/useCompany'
import {
    ArrowLeft,
    Building,
    ChevronDown,
    FileText,
    FolderOpen,
    Mail,
    MapPin,
    MapPinIcon,
    MessageSquare,
    Phone,
    Plus,
    Settings,
    Users,
    Wrench
} from 'lucide-vue-next'
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const fetcher = useFetcher()
const { getCompanyTypeLabel, getCompanyTypeOptions } = useCompany()

const companyId = route.params.id
const company = ref({})
const loading = ref(false)
const error = ref(null)

const companyTypeOptions = getCompanyTypeOptions()

const companyForm = reactive({
    name: '',
    company_type: '',
    reference: '',
    phone: '',
    email: '',
    invoice_street: '',
    invoice_zip: '',
    invoice_city: '',
    siret: '',
    vat: ''
})

const fetchCompany = async () => {
    if (!companyId) return

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get(`/companies/${companyId}`)
        company.value = response.data

        Object.assign(companyForm, {
            name: company.value.name || '',
            company_type: company.value.company_type || '',
            reference: company.value.reference || '',
            phone: company.value.phone || '',
            email: company.value.email || '',
            invoice_street: company.value.invoice_street || '',
            invoice_zip: company.value.invoice_zip || '',
            invoice_city: company.value.invoice_city || '',
            siret: company.value.siret || '',
            vat: company.value.vat || ''
        })
    } catch (err) {
        console.error('Erreur lors du chargement de l\'entreprise:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const saveCompany = async () => {
    if (!companyId) return

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.put(`/companies/${companyId}`, companyForm)
        company.value = response.data

        console.log('Entreprise sauvegardée avec succès')
    } catch (err) {
        console.error('Erreur lors de la sauvegarde:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const contactCompany = () => {
    if (company.value.email) {
        window.location.href = `mailto:${company.value.email}`
    }
}

onMounted(() => {
    fetchCompany()
})
</script>