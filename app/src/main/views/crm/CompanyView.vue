<template>
    <div class="h-full flex flex-col bg-neutral-100">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-start space-x-2">
                    <Button variant="outline" @click="$router.go(-1)" class="h-9 w-9">
                        <ArrowLeft :size="20" />
                    </Button>
                    <template v-if="isDirty"">
                        <Button @click="saveCompany" variant="outline" :disabled="loading" class="w-9">
                        <Save class="h-4 w-4" />
                        </Button>
                        <Button variant="outline" @click="handleCancel" :disabled="loading" class="w-9">
                            <RotateCcw class="h-4 w-4" />
                        </Button>
                    </template>
                </div>
                <div class="flex items-center space-x-3">
                    <DropdownMenu>
                        <DropdownMenuTrigger as-child>
                            <Button variant="outline" class="h-9 w-9">
                                <MoreHorizontal :size="20" />
                            </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                            <DropdownMenuItem @click="handleDelete">
                                <Trash class="h-4 w-4 text-destructive" />
                                Supprimer
                            </DropdownMenuItem>
                        </DropdownMenuContent>
                    </DropdownMenu>
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
                            <Input v-model="companyForm.name" class="mt-1" @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Type de société</label>
                            <Select v-model="companyForm.company_type" @update:model-value="checkDirty">
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
                            <Input v-model="companyForm.reference" class="mt-1" placeholder="CLI-001"
                                @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Téléphone</label>
                            <Input v-model="companyForm.phone" class="mt-1" placeholder="01 42 33 44 55"
                                @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Email</label>
                            <Input v-model="companyForm.email" type="email" class="mt-1"
                                placeholder="contact@entreprise.fr" @input="checkDirty" />
                        </div>

                        <Separator />

                        <h3 class="text-md font-medium text-neutral-700">Adresse de facturation</h3>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Rue</label>
                            <Input v-model="companyForm.invoice_street" class="mt-1" placeholder="123 Rue de la Paix"
                                @input="checkDirty" />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Code postal</label>
                                <Input v-model="companyForm.invoice_zip" class="mt-1" placeholder="75001"
                                    @input="checkDirty" />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Ville</label>
                                <Input v-model="companyForm.invoice_city" class="mt-1" placeholder="Paris"
                                    @input="checkDirty" />
                            </div>
                        </div>

                        <Separator />

                        <div>
                            <label class="text-sm font-medium text-neutral-700">SIRET</label>
                            <Input v-model="companyForm.siret" class="mt-1" placeholder="12345678901234"
                                @input="checkDirty" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">TVA</label>
                            <Input v-model="companyForm.vat" class="mt-1" placeholder="FR12345678901"
                                @input="checkDirty" />
                        </div>
                    </form>
                </div>
            </div>

            <div class="flex-1 overflow-y-auto p-6">
                <div class="bg-white mb-4 rounded-lg border">
                    <div class="p-6">
                        <div class="flex items-start justify-between">
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
                    </div>
                </div>

                <div class="grid grid-cols-4 gap-4 mb-4">
                    <div class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Sites</div>
                    </div>
                    <div class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Contacts</div>
                    </div>
                    <div class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Interventions</div>
                    </div>
                    <div class="bg-white p-4 rounded-lg border">
                        <div class="text-2xl font-semibold text-neutral-900">-</div>
                        <div class="text-sm text-neutral-600">Lots</div>
                    </div>
                </div>


                <Tabs default-value="sites" class="mt-3">
                    <TabsList class="w-full mb-3 bg-neutral-200">
                        <TabsTrigger value="sites">Sites</TabsTrigger>
                        <TabsTrigger value="contacts">Contacts</TabsTrigger>
                        <TabsTrigger value="equipements">Équipements</TabsTrigger>
                        <TabsTrigger value="contrats">Contrats</TabsTrigger>
                        <TabsTrigger value="interventions">Interventions</TabsTrigger>
                        <TabsTrigger value="documents">Documents</TabsTrigger>
                    </TabsList>

                    <TabsContent value="sites" class="bg-white rounded-lg border">
                        <CompanySites :company-id="company.id" />
                    </TabsContent>

                    <TabsContent value="contacts" class="bg-white rounded-lg border">
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

                    <TabsContent value="equipements" class="bg-white rounded-lg border">
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

                    <TabsContent value="contrats" class="bg-white rounded-lg border">
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

                    <TabsContent value="interventions" class="bg-white rounded-lg border">
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

                    <TabsContent value="documents" class="bg-white rounded-lg border">
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
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import Input from '@/common/components/ui/input/Input.vue'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useCompany } from '@/common/composables/useCompany'
import CompanySites from '@/main/components/companies/CompanySites.vue'
import {
    ArrowLeft,
    Building,
    ChevronDown,
    FileText,
    FolderOpen,
    MoreHorizontal,
    Plus,
    RotateCcw,
    Save,
    Settings,
    Trash,
    Users,
    Wrench
} from 'lucide-vue-next'
import { onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const route = useRoute()
const router = useRouter()
const fetcher = useFetcher()
const { getCompanyTypeLabel, getCompanyTypeOptions } = useCompany()

const companyId = route.params.id
const company = ref({})
const loading = ref(false)
const error = ref(null)
const isDirty = ref(false)
const originalForm = ref({})

// Écoute la confirmation de suppression
useBus(bus, 'confirm-delete-company:confirmed', () => {
    deleteCompany()
})

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

const checkDirty = () => {
    isDirty.value = JSON.stringify(companyForm) !== JSON.stringify(originalForm.value)
}

const resetForm = (data) => {
    Object.assign(companyForm, {
        name: data.name || '',
        company_type: data.company_type || '',
        reference: data.reference || '',
        phone: data.phone || '',
        email: data.email || '',
        invoice_street: data.invoice_street || '',
        invoice_zip: data.invoice_zip || '',
        invoice_city: data.invoice_city || '',
        siret: data.siret || '',
        vat: data.vat || ''
    })
    originalForm.value = JSON.parse(JSON.stringify(companyForm))
    isDirty.value = false
}

const handleCancel = () => {
    resetForm(company.value)
}

const handleDelete = () => {
    if (!companyId || !company.value.name) return

    bus.trigger('confirm-delete', {
        title: 'Supprimer l\'entreprise',
        message: 'Êtes-vous sûr de vouloir supprimer cette entreprise ?',
        itemName: company.value.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-company:confirmed'
    })
}

const deleteCompany = async () => {
    try {
        await fetcher.delete(`/companies/${companyId}`)
        toast.success('Entreprise supprimée avec succès')
        bus.trigger('confirm-delete-dialog:close')
        router.push('/companies')
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        toast.error('Erreur lors de la suppression')
        bus.trigger('confirm-delete-dialog:close')
    }
}

const fetchCompany = async () => {
    if (!companyId) return

    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get(`/companies/${companyId}`)
        company.value = response.data
        resetForm(company.value)
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
        resetForm(company.value)
        toast.success('Entreprise sauvegardée avec succès')
    } catch (err) {
        console.error('Erreur lors de la sauvegarde:', err)
        error.value = err
        toast.error('Erreur lors de la sauvegarde')
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