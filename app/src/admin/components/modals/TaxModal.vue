<template>
    <Dialog v-model:open="show">
        <DialogContent class="sm:max-w-2xl">
            <DialogHeader>
                <DialogTitle class="flex items-center">
                    <Percent :size="20" class="mr-2" />
                    {{ isEdit ? 'Modifier la taxe' : 'Nouvelle taxe' }}
                </DialogTitle>
                <DialogDescription>
                    {{ isEdit ? 'Modifiez les informations de la taxe.' : 'Créez une nouvelle taxe de service.' }}
                </DialogDescription>
            </DialogHeader>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="name">Nom de la taxe</Label>
                        <Input 
                            id="name"
                            v-model="form.name" 
                            placeholder="TVA France" 
                            :class="errors.name ? 'border-red-500' : ''"
                            @blur="validateField('name')"
                        />
                        <p v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="rate">Pourcentage (%)</Label>
                        <Input 
                            id="rate"
                            v-model="form.rate" 
                            type="number"
                            step="0.01"
                            placeholder="20.00" 
                            :class="errors.rate ? 'border-red-500' : ''"
                            @blur="validateField('rate')"
                        />
                        <p v-if="errors.rate" class="text-sm text-red-500">{{ errors.rate }}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="stripe_id">ID Stripe</Label>
                        <Input 
                            id="stripe_id"
                            v-model="form.stripe_id" 
                            placeholder="txr_1234567890" 
                            :class="errors.stripe_id ? 'border-red-500' : ''"
                            @blur="validateField('stripe_id')"
                        />
                        <p class="text-sm text-gray-500">Identifiant de la taxe dans Stripe</p>
                        <p v-if="errors.stripe_id" class="text-sm text-red-500">{{ errors.stripe_id }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="country_code">Code pays (optionnel)</Label>
                        <Input 
                            id="country_code"
                            v-model="form.country_code" 
                            placeholder="FR" 
                            maxlength="2"
                            class="uppercase"
                            :class="errors.country_code ? 'border-red-500' : ''"
                            @blur="validateField('country_code')"
                            @input="form.country_code = form.country_code.toUpperCase()"
                        />
                        <p class="text-sm text-gray-500">Code ISO à 2 lettres</p>
                        <p v-if="errors.country_code" class="text-sm text-red-500">{{ errors.country_code }}</p>
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="description">Description (optionnelle)</Label>
                    <Textarea 
                        id="description"
                        v-model="form.description" 
                        placeholder="Description de la taxe..."
                        rows="3"
                    />
                </div>

                <div class="flex items-center space-x-2">
                    <Switch 
                        v-model="form.is_active"
                        id="is_active"
                    />
                    <Label for="is_active">Taxe active</Label>
                </div>

                <DialogFooter class="gap-2">
                    <Button type="button" variant="outline" @click="close">
                        Annuler
                    </Button>
                    <Button 
                        v-if="isEdit" 
                        type="button" 
                        variant="destructive" 
                        :disabled="deleting" 
                        @click="handleDelete"
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
                            {{ isEdit ? 'Modification...' : 'Création...' }}
                        </span>
                        <span v-else>{{ isEdit ? 'Modifier' : 'Créer' }}</span>
                    </Button>
                </DialogFooter>
            </form>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Percent } from 'lucide-vue-next'
import { useFetcher } from "@/common/composables/fetcher"
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
import { Textarea } from '@/common/components/ui/textarea'
import { Label } from '@/common/components/ui/label'
import { Switch } from '@/common/components/ui/switch'

const props = defineProps({
    show: {
        type: Boolean,
        default: false
    },
    tax: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['update:show', 'saved', 'deleted'])

const fetcher = useFetcher()
const saving = ref(false)
const deleting = ref(false)

const form = ref({
    name: '',
    stripe_id: '',
    rate: '',
    country_code: '',
    description: '',
    is_active: true
})

const errors = ref({
    name: '',
    rate: '',
    stripe_id: '',
    country_code: ''
})

const show = computed({
    get: () => props.show,
    set: (value) => emit('update:show', value)
})

const isEdit = computed(() => !!props.tax?.id)

const isFormValid = computed(() => {
    return form.value.name.trim() !== '' && 
           form.value.rate !== '' && 
           !errors.value.name && 
           !errors.value.rate && 
           !errors.value.stripe_id &&
           !errors.value.country_code
})

const validateField = (field) => {
    errors.value[field] = ''
    
    switch (field) {
        case 'name':
            if (!form.value.name.trim()) {
                errors.value.name = 'Le nom de la taxe est requis'
            }
            break
        case 'rate':
            if (form.value.rate === '' || form.value.rate === null) {
                errors.value.rate = 'Le pourcentage est requis'
            } else if (isNaN(form.value.rate) || form.value.rate < 0 || form.value.rate > 100) {
                errors.value.rate = 'Le pourcentage doit être entre 0 et 100'
            }
            break
        case 'country_code':
            if (form.value.country_code && !/^[A-Z]{2}$/.test(form.value.country_code)) {
                errors.value.country_code = 'Le code pays doit être 2 lettres majuscules (ex: FR)'
            }
            break
    }
}

const validateForm = () => {
    validateField('name')
    validateField('rate')
    validateField('country_code')
    return isFormValid.value
}

const resetForm = () => {
    form.value = {
        name: '',
        stripe_id: '',
        rate: '',
        country_code: '',
        description: '',
        is_active: true
    }
    errors.value = {
        name: '',
        rate: '',
        stripe_id: '',
        country_code: ''
    }
}

const close = () => {
    show.value = false
    resetForm()
}

const handleSubmit = async () => {
    if (!validateForm()) return

    saving.value = true
    try {
        if (isEdit.value) {
            await fetcher.patch(`/admin/service_taxes/${props.tax.id}`, form.value)
            toast.success('Taxe modifiée avec succès')
        } else {
            await fetcher.post('/admin/service_taxes', form.value)
            toast.success('Taxe créée avec succès')
        }
        emit('saved')
        close()
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error('Erreur lors de la sauvegarde')
    } finally {
        saving.value = false
    }
}

const handleDelete = async () => {
    deleting.value = true
    try {
        await fetcher.delete(`/admin/service_taxes/${props.tax.id}`)
        toast.success('Taxe supprimée avec succès')
        emit('deleted')
        close()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

watch(() => props.tax, (newTax) => {
    if (newTax) {
        form.value = { ...newTax }
    } else {
        resetForm()
    }
    
    errors.value = {
        name: '',
        rate: '',
        stripe_id: '',
        country_code: ''
    }
}, { immediate: true })
</script> 
