<template>
    <Dialog v-model:open="show">
        <DialogContent class="sm:max-w-2xl">
            <DialogHeader>
                <DialogTitle class="flex items-center">
                    <Ticket :size="20" class="mr-2" />
                    {{ isEdit ? 'Modifier le coupon' : 'Nouveau coupon' }}
                </DialogTitle>
                <DialogDescription>
                    {{ isEdit ? 'Modifiez les informations du coupon de crédit.' : 'Créez un nouveau coupon de crédit.' }}
                </DialogDescription>
            </DialogHeader>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="name">Nom du coupon</Label>
                        <Input 
                            id="name"
                            v-model="form.name" 
                            placeholder="Coupon 50 crédits" 
                            :class="errors.name ? 'border-red-500' : ''"
                            @blur="validateField('name')"
                        />
                        <p v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="available_credit">Crédit disponible</Label>
                        <Input 
                            id="available_credit"
                            v-model="form.available_credit" 
                            type="number"
                            step="0.01"
                            placeholder="50.00" 
                            :class="errors.available_credit ? 'border-red-500' : ''"
                            @blur="validateField('available_credit')"
                        />
                        <p v-if="errors.available_credit" class="text-sm text-red-500">{{ errors.available_credit }}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="code">Code promotionnel</Label>
                        <Input 
                            id="code"
                            v-model="form.code" 
                            placeholder="Généré automatiquement si vide"
                            class="font-mono"
                        />
                        <p class="text-sm text-gray-500">Laissez vide pour génération automatique</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="expiration_date">Date d'expiration (optionnelle)</Label>
                        <Popover>
                            <PopoverTrigger asChild>
                                <Button
                                    variant="outline"
                                    class="w-full justify-start text-left font-normal"
                                >
                                    <Calendar class="mr-2 h-4 w-4" />
                                    {{ formattedExpirationDate || "Aucune expiration" }}
                                </Button>
                            </PopoverTrigger>
                            <PopoverContent class="w-auto p-0">
                                <CalendarRoot 
                                    v-model="expirationDate" 
                                    initial-focus 
                                    locale="fr-FR"
                                />
                            </PopoverContent>
                        </Popover>
                        <p class="text-sm text-gray-500">Laissez vide pour aucune expiration</p>
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="description">Description (optionnelle)</Label>
                    <Textarea 
                        id="description"
                        v-model="form.description" 
                        placeholder="Description du coupon promotionnel..."
                        rows="3"
                    />
                </div>

                <div class="flex items-center space-x-2">
                    <Switch 
                        v-model="form.is_active"
                        id="is_active"
                    />
                    <Label for="is_active">Coupon actif</Label>
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
import { Ticket, Calendar } from 'lucide-vue-next'
import { useFetcher } from "@/common/composables/fetcher"
import { toast } from 'vue-sonner'
import { getLocalTimeZone } from '@internationalized/date'
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
import {
    Popover,
    PopoverContent,
    PopoverTrigger,
} from '@/common/components/ui/popover'
import {
    Calendar as CalendarRoot,
} from '@/common/components/ui/calendar'

const props = defineProps({
    show: {
        type: Boolean,
        default: false
    },
    coupon: {
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
    available_credit: '',
    code: '',
    expiration_date: null,
    description: '',
    is_active: true
})

const errors = ref({
    name: '',
    available_credit: ''
})

const expirationDate = ref(null)

const show = computed({
    get: () => props.show,
    set: (value) => emit('update:show', value)
})

const isEdit = computed(() => !!props.coupon?.id)

const isFormValid = computed(() => {
    return form.value.name.trim() !== '' && 
           form.value.available_credit !== '' && 
           !errors.value.name && 
           !errors.value.available_credit
})

const formattedExpirationDate = computed(() => {
    if (!expirationDate.value) return ''
    if (expirationDate.value.toDate) {
        return expirationDate.value.toDate(getLocalTimeZone()).toLocaleDateString('fr-FR')
    }
    const date = new Date(expirationDate.value)
    return date.toLocaleDateString('fr-FR')
})

const validateField = (field) => {
    errors.value[field] = ''
    
    switch (field) {
        case 'name':
            if (!form.value.name.trim()) {
                errors.value.name = 'Le nom du coupon est requis'
            }
            break
        case 'available_credit':
            if (form.value.available_credit === '' || form.value.available_credit === null) {
                errors.value.available_credit = 'Le crédit disponible est requis'
            } else if (isNaN(form.value.available_credit) || form.value.available_credit <= 0) {
                errors.value.available_credit = 'Le crédit doit être un nombre positif'
            }
            break
    }
}

const validateForm = () => {
    validateField('name')
    validateField('available_credit')
    return isFormValid.value
}

const resetForm = () => {
    form.value = {
        name: '',
        available_credit: '',
        code: '',
        expiration_date: null,
        description: '',
        is_active: true
    }
    errors.value = {
        name: '',
        available_credit: ''
    }
    expirationDate.value = null
}

const close = () => {
    show.value = false
    resetForm()
}

const handleSubmit = async () => {
    if (!validateForm()) return

    saving.value = true
    try {
        // Préparer les données à envoyer
        const submitData = { ...form.value }
        
        // Convertir la date d'expiration si elle existe
        if (expirationDate.value) {
            if (expirationDate.value.toDate) {
                submitData.expiration_date = expirationDate.value.toDate(getLocalTimeZone()).toISOString().split('T')[0]
            } else {
                submitData.expiration_date = new Date(expirationDate.value).toISOString().split('T')[0]
            }
        } else {
            submitData.expiration_date = null
        }

        if (isEdit.value) {
            await fetcher.patch(`/admin/service_credit_coupons/${props.coupon.id}`, submitData)
            toast.success('Coupon modifié avec succès')
        } else {
            await fetcher.post('/admin/service_credit_coupons', submitData)
            toast.success('Coupon créé avec succès')
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
        await fetcher.delete(`/admin/service_credit_coupons/${props.coupon.id}`)
        toast.success('Coupon supprimé avec succès')
        emit('deleted')
        close()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

watch(() => props.coupon, (newCoupon) => {
    if (newCoupon) {
        form.value = { ...newCoupon }
        // Convertir la date d'expiration pour le calendar
        if (newCoupon.expiration_date) {
            expirationDate.value = new Date(newCoupon.expiration_date)
        } else {
            expirationDate.value = null
        }
    } else {
        resetForm()
    }
    
    errors.value = {
        name: '',
        available_credit: ''
    }
}, { immediate: true })
</script>
