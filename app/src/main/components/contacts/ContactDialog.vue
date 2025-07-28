<template>
    <Dialog :open="isOpen" @update:open="handleClose">
        <DialogContent class="md:!max-w-4xl lg:!max-w-5xl">
            <DialogHeader>
                <DialogTitle>{{ isEdit ? 'Modifier le contact' : 'Nouveau contact' }}</DialogTitle>
            </DialogHeader>

            <div class="grid grid-cols-5 gap-4 py-3">
                <div class="w-20">
                    <div class="w-20 h-20 mb-4 bg-secondary rounded-full flex items-center justify-center">
                        <User class="w-10 h-10 text-primary" :stroke-width="1.2" />
                    </div>
                </div>
                <div class="flex-1 col-span-4">
                    <form @submit.prevent="handleSubmit" class="space-y-4">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Prénom *</label>
                                <Input v-model="form.first_name" class="mt-1" placeholder="Ex: Jean" required />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Nom *</label>
                                <Input v-model="form.last_name" class="mt-1" placeholder="Ex: Dupont" required />
                            </div>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Fonction</label>
                            <Input v-model="form.function" class="mt-1" placeholder="Ex: Directeur général" />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Entreprise</label>
                            <CompanySelect v-model="form.company" class="mt-1" />
                        </div>

                        <Separator />

                        <h3 class="font-medium text-neutral-700 mb-2">Informations de contact</h3>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Email</label>
                            <Input v-model="form.email" type="email" class="mt-1"
                                placeholder="jean.dupont@entreprise.fr" />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Téléphone mobile</label>
                                <Input v-model="form.mobile" class="mt-1" placeholder="06 12 34 56 78" />
                            </div>
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Téléphone fixe</label>
                                <Input v-model="form.phone" class="mt-1" placeholder="01 42 33 44 55" />
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
import CompanySelect from '@/common/components/form/company-select/CompanySelect.vue'
import { Button } from '@/common/components/ui/button'
import {
    Dialog,
    DialogContent,
    DialogFooter,
    DialogHeader,
    DialogTitle
} from '@/common/components/ui/dialog'
import Input from '@/common/components/ui/input/Input.vue'
import { Separator } from '@/common/components/ui/separator'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { User } from 'lucide-vue-next'
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { toast } from 'vue-sonner'

const router = useRouter()
const fetcher = useFetcher()

const isOpen = ref(false)
const loading = ref(false)
const isEdit = ref(false)
const contactId = ref(null)

const defaultForm = {
    first_name: '',
    last_name: '',
    function: '',
    company: null,
    email: '',
    mobile: '',
    phone: ''
}

const form = reactive({ ...defaultForm })

const resetForm = () => {
    Object.assign(form, defaultForm)
    isEdit.value = false
    contactId.value = null
}

const handleClose = () => {
    isOpen.value = false
    resetForm()
}

const handleSubmit = async (action = 'close') => {
    if (!form.first_name.trim() || !form.last_name.trim()) {
        toast.error('Le prénom et le nom sont obligatoires')
        return
    }

    loading.value = true

    try {
        let response
        if (isEdit.value && contactId.value) {
            response = await fetcher.put(`/contacts/${contactId.value}`, form)
            toast.success('Contact modifié avec succès')
        } else {
            response = await fetcher.post('/contacts/', form)
            toast.success('Contact créé avec succès')
        }

        const contact = response.data

        if (action === 'view') {
            router.push(`/contact/${contact.id}`)
            bus.trigger('contact-saved', contact)
        } else {
            bus.trigger('contact-created-stay', contact)
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

useBus(bus, 'open-contact-dialog', (event) => {
    const data = event.detail || {}
    if (data.id) {
        isEdit.value = true
        contactId.value = data.id
        Object.assign(form, {
            first_name: data.first_name || '',
            last_name: data.last_name || '',
            function: data.function || '',
            company: data.company?.id || data.company || null,
            email: data.email || '',
            mobile: data.mobile || '',
            phone: data.phone || ''
        })
    } else {
        resetForm()
        if (data.company_id) {
            form.company = data.company_id
        }
    }
    isOpen.value = true
})
</script>