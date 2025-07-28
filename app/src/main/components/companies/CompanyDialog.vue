<template>
    <Dialog :open="isOpen" @update:open="handleClose">
        <DialogContent class="md:!max-w-4xl lg:!max-w-5xl">
            <DialogHeader>
                <DialogTitle>{{ isEdit ? 'Modifier l\'entreprise' : 'Nouvelle entreprise' }}</DialogTitle>
            </DialogHeader>

            <div class="grid grid-cols-5 gap-4 py-3">
                <div class="w-30">
                    <div class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                        <Building2 class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
                    </div>
                </div>
                <div class="flex-1 col-span-4">
                    <form @submit.prevent="handleSubmit" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Raison sociale *</label>
                            <Input v-model="form.name" class="mt-1" placeholder="Ex: SARL Martin" required />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Type de société</label>
                                <Select v-model="form.company_type">
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
                                <Input v-model="form.reference" class="mt-1" placeholder="Ex: CLI-001" />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Téléphone</label>
                                <Input v-model="form.phone" class="mt-1" placeholder="01 42 33 44 55" />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Email</label>
                                <Input v-model="form.email" type="email" class="mt-1"
                                    placeholder="contact@entreprise.fr" />
                            </div>
                        </div>

                        <Separator />

                        <h3 class="font-medium text-neutral-700 mb-2">Adresse de facturation</h3>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Rue</label>
                            <Input v-model="form.invoice_street" class="mt-1" placeholder="123 Rue de la Paix" />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Code postal</label>
                                <Input v-model="form.invoice_zip" class="mt-1" placeholder="75001" />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Ville</label>
                                <Input v-model="form.invoice_city" class="mt-1" placeholder="Paris" />
                            </div>
                        </div>

                        <Separator />

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">SIRET</label>
                                <Input v-model="form.siret" class="mt-1" placeholder="12345678901234" />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">TVA</label>
                                <Input v-model="form.vat" class="mt-1" placeholder="FR12345678901" />
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <DialogFooter class="mt-6">
                <Button variant="outline" @click="handleClose" :disabled="loading">
                    Annuler
                </Button>
                <Button @click="handleSaveAndClose" :disabled="loading" variant="outline">
                    {{ loading ? 'Sauvegarde...' : 'Enregistrer et fermer' }}
                </Button>
                <Button @click="handleSaveAndView" :disabled="loading">
                    {{ loading ? 'Sauvegarde...' : 'Enregistrer et voir' }}
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import {
    Dialog,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle
} from '@/common/components/ui/dialog'
import Input from '@/common/components/ui/input/Input.vue'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useCompany } from '@/common/composables/useCompany'
import { Building2 } from 'lucide-vue-next'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()
const { getCompanyTypeOptions } = useCompany()

const isOpen = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const companyId = ref(null)

const companyTypeOptions = getCompanyTypeOptions()

const defaultForm = {
    name: '',
    company_type: 'client_final',
    reference: '',
    phone: '',
    email: '',
    invoice_street: '',
    invoice_zip: '',
    invoice_city: '',
    siret: '',
    vat: ''
}

const form = reactive({ ...defaultForm })

const resetForm = () => {
    Object.assign(form, defaultForm)
    isEdit.value = false
    companyId.value = null
}

const handleClose = () => {
    isOpen.value = false
    resetForm()
}

const handleSubmit = async (action = 'close') => {
    if (!form.name.trim()) {
        toast.error('Le nom de l\'entreprise est obligatoire')
        return
    }

    loading.value = true

    try {
        let response
        if (isEdit.value && companyId.value) {
            response = await fetcher.put(`/companies/${companyId.value}`, form)
            toast.success('Entreprise modifiée avec succès')
        } else {
            response = await fetcher.post('/companies/', form)
            toast.success('Entreprise créée avec succès')
        }

        const company = response.data

        if (action === 'view') {
            router.push(`/company/${company.id}`)
            bus.trigger('company-saved', company)
        } else {
            // Action 'close' - on émet un événement spécifique pour rafraîchir la liste
            bus.trigger('company-created-stay', company)
        }

        handleClose()
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error(isEdit.value ? 'Erreur lors de la modification' : 'Erreur lors de la création')
    } finally {
        loading.value = false
    }
}

const handleSaveAndClose = () => {
    handleSubmit('close')
}

const handleSaveAndView = () => {
    handleSubmit('view')
}

useBus(bus, 'open-company-dialog', (event) => {
    const data = event.detail || {}
    if (data.company) {
        isEdit.value = true
        companyId.value = data.company.id
        Object.assign(form, {
            name: data.company.name || '',
            company_type: data.company.company_type || 'client_final',
            reference: data.company.reference || '',
            phone: data.company.phone || '',
            email: data.company.email || '',
            invoice_street: data.company.invoice_street || '',
            invoice_zip: data.company.invoice_zip || '',
            invoice_city: data.company.invoice_city || '',
            siret: data.company.siret || '',
            vat: data.company.vat || ''
        })
    } else {
        resetForm()
    }
    isOpen.value = true
})
</script>