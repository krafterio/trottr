<template>
    <Dialog :open="isOpen" @update:open="handleClose">
        <DialogContent class="md:!max-w-4xl lg:!max-w-5xl">
            <DialogHeader>
                <DialogTitle>{{ isEdit ? 'Modifier l\'intervention' : 'Nouvelle intervention' }}</DialogTitle>
            </DialogHeader>

            <div class="grid grid-cols-5 gap-4 py-3">
                <div class="w-20">
                    <div class="w-20 h-20 mb-4 bg-secondary rounded-full flex items-center justify-center">
                        <Wrench class="w-10 h-10 text-primary" :stroke-width="1.2" />
                    </div>
                </div>
                <div class="flex-1 col-span-4">
                    <form @submit.prevent="handleSubmit" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Nom de l'intervention *</label>
                            <Input v-model="form.name" class="mt-1" placeholder="Ex: Réparation panne électrique"
                                required />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Description</label>
                            <Textarea v-model="form.description" class="mt-1"
                                placeholder="Détails de l'intervention..." />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Référence client</label>
                                <Input v-model="form.customer_reference" class="mt-1" placeholder="Ex: REF-001" />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Priorité *</label>
                                <PrioritySelect v-model="form.priority" class="mt-1" />
                            </div>
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Catégorie</label>
                                <CategorySelect v-model="form.category" class="mt-1"
                                    placeholder="Sélectionner une catégorie" />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Statut</label>
                                <StatusSelect v-model="form.status" class="mt-1" placeholder="Sélectionner un statut" />
                            </div>
                        </div>

                        <Separator />

                        <h3 class="font-medium text-neutral-700 mb-2">Client</h3>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Entreprise</label>
                                <CompanySelect v-model="form.customer_company" class="mt-1"
                                    placeholder="Sélectionner une entreprise"
                                    @update:model-value="handleCompanyChange" />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Contact</label>
                                <ContactSelect v-model="form.customer_contact" class="mt-1"
                                    placeholder="Sélectionner un contact"
                                    :company="form.customer_company?.id || form.customer_company || null"
                                    @update:model-value="handleContactChange" />
                            </div>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Site</label>
                            <SiteSelect v-model="form.site" class="mt-1" placeholder="Sélectionner un site"
                                :disabled="!canSelectSite"
                                :company-id="form.customer_company?.id || form.customer_company"
                                :contact-id="form.customer_contact?.id || form.customer_contact" />
                        </div>

                        <Separator v-if="isEdit" />

                        <div v-if="isEdit">
                            <h3 class="font-medium text-neutral-700 mb-2">Planification</h3>

                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="text-sm font-medium text-neutral-700">Début prévu</label>
                                    <Input v-model="form.scheduled_start" type="datetime-local" class="mt-1" />
                                </div>

                                <div>
                                    <label class="text-sm font-medium text-neutral-700">Fin prévue</label>
                                    <Input v-model="form.scheduled_end" type="datetime-local" class="mt-1" />
                                </div>
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Opérateur assigné</label>
                                <UserSelect v-model="form.operator" class="mt-1"
                                    placeholder="Sélectionner un opérateur" />
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
import CategorySelect from '@/common/components/form/category-select/CategorySelect.vue'
import CompanySelect from '@/common/components/form/company-select/CompanySelect.vue'
import ContactSelect from '@/common/components/form/contact-select/ContactSelect.vue'
import PrioritySelect from '@/common/components/form/priority-select/PrioritySelect.vue'
import SiteSelect from '@/common/components/form/site-select/SiteSelect.vue'
import StatusSelect from '@/common/components/form/status-select/StatusSelect.vue'
import UserSelect from '@/common/components/form/user-select/UserSelect.vue'
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Separator } from '@/common/components/ui/separator'
import { Textarea } from '@/common/components/ui/textarea'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { Wrench } from 'lucide-vue-next'
import { computed, reactive, ref } from 'vue'
import { toast } from 'vue-sonner'

const fetcher = useFetcher()

const isOpen = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const currentJob = ref(null)

const form = reactive({
    name: '',
    description: '',
    customer_reference: '',
    customer_company: null,
    customer_contact: null,
    priority: 'normal',
    category: null,
    status: null,
    site: null,
    operator: null,
    scheduled_start: '',
    scheduled_end: ''
})

const loadDefaultStatus = async () => {
    try {
        const response = await fetcher.get('/job-status')
        if (response.data && response.data.length > 0) {
            form.status = response.data[0].id
        }
    } catch (error) {
        console.error('Erreur lors du chargement des statuts:', error)
    }
}



const canSelectSite = computed(() => {
    return form.customer_company || form.customer_contact
})

const resetForm = () => {
    Object.assign(form, {
        name: '',
        description: '',
        customer_reference: '',
        customer_company: null,
        customer_contact: null,
        priority: 'normal',
        category: null,
        status: null,
        site: null,
        operator: null,
        scheduled_start: '',
        scheduled_end: ''
    })
}

const handleCompanyChange = (companyId) => {
    // Réinitialiser le contact et le site quand l'entreprise change
    form.customer_contact = null
    form.site = null
}

const handleContactChange = (contactId) => {
    // Réinitialiser le site quand le contact change
    form.site = null
}



const handleEdit = (data) => {
    isEdit.value = true
    currentJob.value = data
    isOpen.value = true

    Object.assign(form, {
        name: data.name || '',
        description: data.description || '',
        customer_reference: data.customer_reference || '',
        customer_company: data.customer_company?.id || null,
        customer_contact: data.customer_contact?.id || null,
        priority: data.priority || 'normal',
        category: data.category?.id || null,
        status: data.status?.id || null,
        site: data.site?.id || null,
        operator: data.operator?.id || null,
        scheduled_start: data.scheduled_start ? new Date(data.scheduled_start).toISOString().slice(0, 16) : '',
        scheduled_end: data.scheduled_end ? new Date(data.scheduled_end).toISOString().slice(0, 16) : ''
    })
}

const handleClose = () => {
    isOpen.value = false
    resetForm()
    isEdit.value = false
    currentJob.value = null
}

const handleSubmit = async (saveAndView = false) => {
    if (!form.name) {
        toast.error('Le nom de l\'intervention est obligatoire')
        return
    }

    loading.value = true

    try {
        const jobData = {
            name: form.name,
            description: form.description,
            customer_reference: form.customer_reference,
            customer_company: form.customer_company,
            customer_contact: form.customer_contact,
            priority: form.priority,
            category: form.category,
            status: form.status,
            site: form.site,
            operator: form.operator,
            scheduled_start: form.scheduled_start ? new Date(form.scheduled_start).toISOString() : null,
            scheduled_end: form.scheduled_end ? new Date(form.scheduled_end).toISOString() : null
        }

        if (isEdit.value) {
            await fetcher.put(`/jobs/${currentJob.value.id}`, jobData)
            toast.success('Intervention modifiée')
        } else {
            const response = await fetcher.post('/jobs', jobData)
            toast.success('Intervention créée')
            bus.trigger('job-created-stay')
            if (saveAndView) {
                handleClose()
                // Rediriger vers la vue détaillée
                window.location.href = `/job/${response.data.id}`
            }
        }

        bus.trigger('job-saved')
        if (!saveAndView) {
            handleClose()
        }
    } catch (error) {
        console.error('Erreur:', error)
        toast.error(isEdit.value ? 'Erreur lors de la modification' : 'Erreur lors de la création')
    } finally {
        loading.value = false
    }
}

const handleSaveAndClose = () => {
    handleSubmit(false)
}

const handleSaveAndView = () => {
    handleSubmit(true)
}

useBus(bus, 'open-job-dialog', (data) => {
    isOpen.value = true

    if (data && data.id) {
        isEdit.value = true
        currentJob.value = data

        Object.assign(form, {
            name: data.name || '',
            description: data.description || '',
            customer_reference: data.customer_reference || '',
            customer_company: data.customer_company?.id || null,
            customer_contact: data.customer_contact?.id || null,
            priority: data.priority || 'normal',
            category: data.category?.id || null,
            status: data.status?.id || null,
            site: data.site?.id || null,
            operator: data.operator?.id || null,
            scheduled_start: data.scheduled_start ? new Date(data.scheduled_start).toISOString().slice(0, 16) : '',
            scheduled_end: data.scheduled_end ? new Date(data.scheduled_end).toISOString().slice(0, 16) : ''
        })
    } else {
        isEdit.value = false
        currentJob.value = null
        resetForm()
        loadDefaultStatus()
    }
})
</script>