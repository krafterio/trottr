<template>
    <Dialog :open="isOpen" @update:open="handleClose">
        <DialogContent class="md:!max-w-4xl lg:!max-w-5xl">
            <DialogHeader>
                <DialogTitle>{{ isEdit ? 'Modifier le site' : 'Nouveau site' }}</DialogTitle>
            </DialogHeader>

            <div class="grid grid-cols-5 gap-4 py-3">
                <div class="w-20">
                    <div class="w-20 h-20 mb-4 bg-secondary rounded-full flex items-center justify-center">
                        <MapPin class="w-10 h-10 text-primary" :stroke-width="1.2" />
                    </div>
                </div>
                <div class="flex-1 col-span-4">
                    <form @submit.prevent="handleSubmit" class="space-y-4">
                        <div>
                            <label class="text-sm font-medium text-neutral-700">Nom du site *</label>
                            <Input v-model="form.name" class="mt-1" placeholder="Ex: Résidence des Jardins" required />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Type de bâtiment</label>
                                <Select v-model="form.building_type">
                                    <SelectTrigger class="mt-1 w-full">
                                        <SelectValue placeholder="Sélectionner un type" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem v-for="option in buildingTypeOptions" :key="option.value"
                                            :value="option.value">
                                            {{ option.label }}
                                        </SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Entreprise</label>
                                <CompanySelect v-model="form.company" class="mt-1"
                                    placeholder="Sélectionner une entreprise" />
                            </div>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Adresse *</label>
                            <Input v-model="form.street" class="mt-1" placeholder="Ex: 123 rue de la Paix" required />
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Complément d'adresse</label>
                            <Input v-model="form.street_2" class="mt-1" placeholder="Ex: Bâtiment A, Étage 2" />
                        </div>

                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="text-sm font-medium text-neutral-700">Code postal *</label>
                                <Input v-model="form.zip" class="mt-1" placeholder="Ex: 75001" required />
                            </div>

                            <div>
                                <label class="text-sm font-medium text-neutral-700">Ville *</label>
                                <Input v-model="form.city" class="mt-1" placeholder="Ex: Paris" required />
                            </div>
                        </div>

                        <div>
                            <label class="text-sm font-medium text-neutral-700">Pays *</label>
                            <CountrySelect v-model="form.country" class="mt-1" placeholder="Sélectionner un pays"
                                required />
                        </div>

                        <DialogFooter>
                            <Button type="button" variant="outline" @click="handleClose">Annuler</Button>
                            <Button type="submit" :disabled="loading">
                                {{ loading ? 'Enregistrement...' : (isEdit ? 'Modifier' : 'Créer') }}
                            </Button>
                        </DialogFooter>
                    </form>
                </div>
            </div>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { CompanySelect } from '@/common/components/form/company-select'
import { CountrySelect } from '@/common/components/form/country-select'
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useSite } from '@/common/composables/useSite'
import { MapPin } from 'lucide-vue-next'
import { reactive, ref } from 'vue'
import { toast } from 'vue-sonner'

const isOpen = ref(false)

const fetcher = useFetcher()
const { getSiteBuildingTypeOptions } = useSite()

const loading = ref(false)
const isEdit = ref(false)
const siteId = ref(null)
const buildingTypeOptions = getSiteBuildingTypeOptions()

const defaultForm = {
    name: '',
    building_type: 'autre',
    street: '',
    street_2: '',
    zip: '',
    city: '',
    country: null,
    company: null
}

const form = reactive({ ...defaultForm })

const resetForm = () => {
    Object.assign(form, defaultForm)
    isEdit.value = false
    siteId.value = null
}

const handleClose = () => {
    isOpen.value = false
    resetForm()
}

const handleSubmit = async () => {
    if (!form.name.trim()) {
        toast.error('Le nom du site est obligatoire')
        return
    }

    loading.value = true

    try {
        const submitData = { ...form }

        if (typeof submitData.country === 'object' && submitData.country?.id) {
            submitData.country = submitData.country.id
        }

        if (typeof submitData.company === 'object' && submitData.company?.id) {
            submitData.company = submitData.company.id
        }

        let response
        if (isEdit.value && siteId.value) {
            response = await fetcher.put(`/sites/${siteId.value}`, submitData)
            toast.success('Site modifié avec succès')
        } else {
            response = await fetcher.post('/sites/', submitData)
            toast.success('Site créé avec succès')
        }

        const site = response.data

        bus.trigger('site-saved', site)
        bus.trigger('site-created-stay', site)
        handleClose()
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error(isEdit.value ? 'Erreur lors de la modification' : 'Erreur lors de la création')
    } finally {
        loading.value = false
    }
}

useBus(bus, 'open-site-dialog', (event) => {
    const data = event.detail || {}
    if (data.id) {
        isEdit.value = true
        siteId.value = data.id
        Object.assign(form, {
            name: data.name || '',
            building_type: data.building_type || 'autre',
            street: data.street || '',
            street_2: data.street_2 || '',
            zip: data.zip || '',
            city: data.city || '',
            country: data.country?.id || data.country || null,
            company: data.company?.id || data.company || null
        })
    } else {
        resetForm()
        if (data.company) {
            form.company = data.company
        }
    }
    isOpen.value = true
})
</script>