<template>
    <Dialog v-model:open="show">
        <DialogContent class="sm:max-w-2xl">
            <DialogHeader>
                <DialogTitle class="flex items-center">
                    <Coins :size="20" class="mr-2" />
                    {{ isEdit ? 'Modifier le pack de crédit' : 'Nouveau pack de crédit' }}
                </DialogTitle>
                <DialogDescription>
                    {{ isEdit ? 'Modifiez les informations du pack de crédit.' : 'Créez un nouveau pack de crédit pour l\'enrichissement.' }}
                </DialogDescription>
            </DialogHeader>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="name">Nom du pack</Label>
                        <Input 
                            id="name"
                            v-model="form.name" 
                            placeholder="Pack 100 crédits" 
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
                            placeholder="100.00" 
                            :class="errors.available_credit ? 'border-red-500' : ''"
                            @blur="validateField('available_credit')"
                        />
                        <p v-if="errors.available_credit" class="text-sm text-red-500">{{ errors.available_credit }}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="price">Prix</Label>
                        <div class="flex gap-2">
                            <Input 
                                id="price"
                                v-model="form.price" 
                                type="number"
                                step="0.01"
                                placeholder="9.99" 
                                :class="errors.price ? 'border-red-500' : ''"
                                @blur="validateField('price')"
                                class="flex-1"
                            />
                            <Select v-model="form.currency" class="w-24">
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem v-for="currency in currencies" :key="currency.value" :value="currency.value">
                                        {{ currency.title }}
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <p v-if="errors.price" class="text-sm text-red-500">{{ errors.price }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="stripe_product_id">ID Produit Stripe</Label>
                        <Input 
                            id="stripe_product_id"
                            v-model="form.stripe_product_id" 
                            placeholder="prod_1234567890" 
                            :class="errors.stripe_product_id ? 'border-red-500' : ''"
                            @blur="validateField('stripe_product_id')"
                        />
                        <p class="text-sm text-gray-500">Identifiant du produit dans Stripe</p>
                        <p v-if="errors.stripe_product_id" class="text-sm text-red-500">{{ errors.stripe_product_id }}</p>
                    </div>
                </div>

                <div class="space-y-2">
                    <Label for="stripe_price_id">ID Prix Stripe</Label>
                    <Input 
                        id="stripe_price_id"
                        v-model="form.stripe_price_id" 
                        placeholder="price_1234567890" 
                        :class="errors.stripe_price_id ? 'border-red-500' : ''"
                        @blur="validateField('stripe_price_id')"
                    />
                    <p class="text-sm text-gray-500">Identifiant du prix dans Stripe</p>
                    <p v-if="errors.stripe_price_id" class="text-sm text-red-500">{{ errors.stripe_price_id }}</p>
                </div>

                <div class="space-y-2">
                    <Label for="description">Description (optionnelle)</Label>
                    <Textarea 
                        id="description"
                        v-model="form.description" 
                        placeholder="Description du pack de crédit pour l'enrichissement..."
                        rows="3"
                    />
                </div>

                <div class="flex items-center space-x-2">
                    <Switch 
                        v-model="form.is_active"
                        id="is_active"
                    />
                    <Label for="is_active">Pack actif</Label>
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
                            <span class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                            Suppression...
                        </span>
                        <span v-else>Supprimer</span>
                    </Button>
                    <Button 
                        type="submit" 
                        :disabled="!isFormValid || saving"
                    >
                        <span v-if="saving" class="flex items-center">
                            <span class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
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
import {
    Coins,
} from 'lucide-vue-next'
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
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/common/components/ui/select'

const props = defineProps({
    show: {
        type: Boolean,
        default: false
    },
    pack: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['update:show', 'saved', 'deleted'])

const fetcher = useFetcher()
const saving = ref(false)
const deleting = ref(false)

const currencies = [
    { title: 'EUR', value: 'EUR' },
    { title: 'USD', value: 'USD' },
]

const form = ref({
    name: '',
    price: '',
    currency: 'EUR',
    available_credit: '',
    stripe_product_id: '',
    stripe_price_id: '',
    description: '',
    is_active: true
})

const errors = ref({
    name: '',
    price: '',
    available_credit: '',
    stripe_product_id: '',
    stripe_price_id: ''
})

const show = computed({
    get: () => props.show,
    set: (value) => emit('update:show', value)
})

const isEdit = computed(() => !!props.pack?.id)

const isFormValid = computed(() => {
    return form.value.name.trim() !== '' && 
           form.value.price !== '' && 
           form.value.available_credit !== '' && 
           !errors.value.name && 
           !errors.value.price && 
           !errors.value.available_credit &&
           !errors.value.stripe_product_id &&
           !errors.value.stripe_price_id
})

const validateField = (field) => {
    errors.value[field] = ''
    
    switch (field) {
        case 'name':
            if (!form.value.name.trim()) {
                errors.value.name = 'Le nom du pack est requis'
            }
            break
        case 'price':
            if (form.value.price === '' || form.value.price === null) {
                errors.value.price = 'Le prix est requis'
            } else if (isNaN(form.value.price) || form.value.price <= 0) {
                errors.value.price = 'Le prix doit être un nombre positif'
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
    validateField('price')
    validateField('available_credit')
    return isFormValid.value
}

const resetForm = () => {
    form.value = {
        name: '',
        price: '',
        currency: 'EUR',
        available_credit: '',
        stripe_product_id: '',
        stripe_price_id: '',
        description: '',
        is_active: true
    }
    errors.value = {
        name: '',
        price: '',
        available_credit: '',
        stripe_product_id: '',
        stripe_price_id: ''
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
            await fetcher.patch(`/admin/service_credit_packs/${props.pack.id}`, form.value)
            toast.success('Pack modifié avec succès')
        } else {
            await fetcher.post('/admin/service_credit_packs', form.value)
            toast.success('Pack créé avec succès')
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
        await fetcher.delete(`/admin/service_credit_packs/${props.pack.id}`)
        toast.success('Pack supprimé avec succès')
        emit('deleted')
        close()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

watch(() => props.pack, (newPack) => {
    if (newPack) {
        form.value = { ...newPack }
    } else {
        resetForm()
    }
    
    errors.value = {
        name: '',
        price: '',
        available_credit: '',
        stripe_product_id: '',
        stripe_price_id: ''
    }
}, { immediate: true })
</script>
