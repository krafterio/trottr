<template>
    <Dialog v-model:open="show">
        <DialogContent class="sm:max-w-md">
            <DialogHeader>
                <DialogTitle class="flex items-center">
                    <Globe :size="20" class="mr-2" />
                    {{ country ? 'Modifier le pays' : 'Ajouter un pays' }}
                </DialogTitle>
                <DialogDescription>
                    {{ country ? 'Modifiez les informations du pays.' : 'Ajoutez un nouveau pays à la liste.' }}
                </DialogDescription>
            </DialogHeader>

            <form @submit.prevent="saveCountry" class="space-y-4">
                <div class="space-y-2">
                    <Label for="name">Nom du pays</Label>
                    <Input 
                        id="name"
                        v-model="formData.name" 
                        placeholder="France" 
                        :class="errors.name ? 'border-red-500' : ''"
                        @blur="validateField('name')"
                    />
                    <p v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</p>
                </div>

                <div class="space-y-2">
                    <Label for="iso_code">Code ISO</Label>
                    <Input 
                        id="iso_code"
                        v-model="formData.iso_code" 
                        placeholder="FR" 
                        :class="errors.iso_code ? 'border-red-500' : ''"
                        @blur="validateField('iso_code')"
                    />
                    <p class="text-sm text-gray-500">Code ISO à 2 ou 3 caractères (ex: FR, USA)</p>
                    <p v-if="errors.iso_code" class="text-sm text-red-500">{{ errors.iso_code }}</p>
                </div>

                <DialogFooter class="gap-2">
                    <Button type="button" variant="outline" @click="closeModal">
                        Annuler
                    </Button>
                    <Button 
                        v-if="country" 
                        type="button" 
                        variant="destructive" 
                        :disabled="deleting" 
                        @click="deleteCountry"
                    >
                        <span v-if="deleting" class="flex items-center">
                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Suppression...
                        </span>
                        <span v-else>Supprimer</span>
                    </Button>
                    <Button 
                        type="submit" 
                        :disabled="!isFormValid || saving"
                    >
                        <span v-if="saving" class="flex items-center">
                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            {{ country ? 'Modification...' : 'Création...' }}
                        </span>
                        <span v-else>{{ country ? 'Modifier' : 'Créer' }}</span>
                    </Button>
                </DialogFooter>
            </form>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { Globe } from 'lucide-vue-next'
import { useFetcher } from '@/common/composables/fetcher.js'
import { toast } from 'vue-sonner'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/common/components/ui/dialog'
import { Button } from '@/common/components/ui/button'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'

const props = defineProps({
    show: {
        type: Boolean,
        default: false
    },
    country: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['update:show', 'saved', 'deleted'])

const fetcher = useFetcher()
const saving = ref(false)
const deleting = ref(false)

const formData = ref({
    name: '',
    iso_code: ''
})

const errors = ref({
    name: '',
    iso_code: ''
})

const show = computed({
    get: () => props.show,
    set: (value) => emit('update:show', value)
})

const isFormValid = computed(() => {
    return formData.value.name.trim() !== '' && 
           formData.value.iso_code.trim() !== '' && 
           !errors.value.name && 
           !errors.value.iso_code
})

const validateField = (field) => {
    errors.value[field] = ''
    
    switch (field) {
        case 'name':
            if (!formData.value.name.trim()) {
                errors.value.name = 'Le nom du pays est requis'
            }
            break
        case 'iso_code':
            if (!formData.value.iso_code.trim()) {
                errors.value.iso_code = 'Le code ISO est requis'
            } else if (formData.value.iso_code.length < 2 || formData.value.iso_code.length > 3) {
                errors.value.iso_code = 'Le code ISO doit contenir 2 ou 3 caractères'
            }
            break
    }
}

const validateForm = () => {
    validateField('name')
    validateField('iso_code')
    return isFormValid.value
}

watch(() => props.country, (newCountry) => {
    if (newCountry) {
        formData.value = {
            name: newCountry.name,
            iso_code: newCountry.iso_code
        }
    } else {
        formData.value = {
            name: '',
            iso_code: ''
        }
    }
    
    errors.value = {
        name: '',
        iso_code: ''
    }
}, { immediate: true })

const closeModal = () => {
    show.value = false
}

const saveCountry = async () => {
    if (!validateForm()) return

    saving.value = true
    try {
        if (props.country) {
            await fetcher.patch(`/countries/${props.country.id}`, formData.value)
            toast.success('Pays modifié avec succès')
        } else {
            await fetcher.post('/countries', formData.value)
            toast.success('Pays créé avec succès')
        }
        emit('saved')
        closeModal()
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error('Erreur lors de la sauvegarde')
    } finally {
        saving.value = false
    }
}

const deleteCountry = async () => {
    deleting.value = true
    try {
        await fetcher.delete(`/countries/${props.country.id}`)
        toast.success('Pays supprimé avec succès')
        emit('deleted')
        closeModal()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}
</script>