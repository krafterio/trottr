<template>
    <Dialog :open="isOpen" @update:open="handleClose">
        <DialogContent class="md:!max-w-4xl lg:!max-w-5xl">
            <DialogHeader>
                <DialogTitle>{{ isEdit ? 'Modifier le site' : 'Nouveau site' }}</DialogTitle>
            </DialogHeader>

            <div class="grid grid-cols-5 gap-4 py-3">
                <div class="w-30">
                    <div class="w-16 h-16 mx-auto mb-4 bg-neutral-100 rounded-full flex items-center justify-center">
                        <MapPin class="w-8 h-8 text-neutral-400" :stroke-width="1.2" />
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
                                <CompanySelect v-model="form.company_id" class="mt-1"
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
                            <CountrySelect v-model="form.country_id" class="mt-1" placeholder="Sélectionner un pays"
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
import { Button } from '@/common/components/ui/button'
import { CompanySelect } from '@/common/components/ui/company-select'
import { CountrySelect } from '@/common/components/ui/country-select'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { bus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useSite } from '@/common/composables/useSite'
import { MapPin } from 'lucide-vue-next'
import { reactive, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
    isOpen: Boolean,
    site: Object
})

const emit = defineEmits(['close', 'saved'])

const fetcher = useFetcher()
const { getSiteBuildingTypeOptions } = useSite()

const loading = ref(false)
const isEdit = ref(false)
const buildingTypeOptions = getSiteBuildingTypeOptions()

const defaultForm = {
    name: '',
    building_type: 'autre',
    street: '',
    street_2: '',
    zip: '',
    city: '',
    country_id: null,
    company_id: null
}

const form = reactive({ ...defaultForm })

watch(() => props.site, (newSite) => {
    if (newSite) {
        isEdit.value = true
        Object.assign(form, {
            name: newSite.name || '',
            building_type: newSite.building_type || 'autre',
            street: newSite.street || '',
            street_2: newSite.street_2 || '',
            zip: newSite.zip || '',
            city: newSite.city || '',
            country_id: newSite.country_id || null,
            company_id: newSite.company_id || null
        })
    } else {
        isEdit.value = false
        Object.assign(form, defaultForm)
    }
}, { immediate: true })

const handleClose = () => {
    emit('close')
}

const handleSubmit = async () => {
    if (loading.value) return

    loading.value = true

    try {
        let response
        if (isEdit.value) {
            response = await fetcher.put(`/api/sites/${props.site.id}`, form)
        } else {
            response = await fetcher.post('/api/sites/', form)
        }

        if (response.success) {
            toast.success(isEdit.value ? 'Site modifié avec succès' : 'Site créé avec succès')
            bus.emit('sites:refresh')
            emit('saved', response.data)
            handleClose()
        } else {
            toast.error(response.message || 'Une erreur est survenue')
        }
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error('Une erreur est survenue lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}
</script>