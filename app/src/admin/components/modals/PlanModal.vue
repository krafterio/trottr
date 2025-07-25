<template>
    <Dialog v-model:open="show">
        <DialogContent class="sm:max-w-2xl">
            <DialogHeader>
                <DialogTitle class="flex items-center">
                    <Crown :size="20" class="mr-2" />
                    {{ isEdit ? 'Modifier le plan' : 'Nouveau plan' }}
                </DialogTitle>
                <DialogDescription>
                    {{ isEdit ? 'Modifiez les informations du plan d\'abonnement.' : 'Créez un nouveau plan d\'abonnement.' }}
                </DialogDescription>
            </DialogHeader>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="name">Nom du plan</Label>
                        <Input 
                            id="name"
                            v-model="form.name" 
                            placeholder="Plan Pro" 
                            :class="errors.name ? 'border-red-500' : ''"
                            @blur="validateField('name')"
                        />
                        <p v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="type">Type de plan</Label>
                        <Select v-model="form.type" class="w-full">
                            <SelectTrigger :class="errors.type ? 'border-red-500' : ''" class="w-full">
                                <SelectValue placeholder="Sélectionner un type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="type in planTypes" :key="type.value" :value="type.value">
                                    {{ type.title }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                        <p v-if="errors.type" class="text-sm text-red-500">{{ errors.type }}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="period">Période de facturation</Label>
                        <Select v-model="form.period" class="w-full">
                            <SelectTrigger :class="errors.period ? 'border-red-500' : ''" class="w-full">
                                <SelectValue placeholder="Sélectionner une période" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem v-for="period in planPeriods" :key="period.value" :value="period.value">
                                    {{ period.title }}
                                </SelectItem>
                            </SelectContent>
                        </Select>
                        <p v-if="errors.period" class="text-sm text-red-500">{{ errors.period }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="price">Prix</Label>
                        <div class="flex gap-2">
                            <Input 
                                id="price"
                                v-model="form.price" 
                                type="number"
                                step="0.01"
                                placeholder="29.99" 
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
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                </div>

                <div class="space-y-2">
                    <Label for="description">Description (optionnelle)</Label>
                    <Textarea 
                        id="description"
                        v-model="form.description" 
                        placeholder="Description du plan d'abonnement..."
                        rows="3"
                    />
                </div>

                <div class="flex items-center space-x-2">
                    <Switch 
                        v-model="form.is_active"
                        id="is_active"
                    />
                    <Label for="is_active">Plan actif</Label>
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
import { Crown } from 'lucide-vue-next'
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
    plan: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['update:show', 'saved', 'deleted'])

const fetcher = useFetcher()
const saving = ref(false)
const deleting = ref(false)

const planTypes = [
    { title: 'Pro', value: 'Pro' },
    { title: 'Team', value: 'Team' },
    { title: 'Entreprise', value: 'Enterprise' },
]

const planPeriods = [
    { title: 'Mensuel', value: 'Mensuel' },
    { title: 'Annuel', value: 'Annuel' },
]

const currencies = [
    { title: 'EUR', value: 'EUR' },
    { title: 'USD', value: 'USD' },
]

const form = ref({
    name: '',
    type: 'Pro',
    period: 'Mensuel',
    stripe_product_id: '',
    stripe_price_id: '',
    price: '',
    currency: 'EUR',
    description: '',
    is_active: true
})

const errors = ref({
    name: '',
    type: '',
    period: '',
    price: '',
    stripe_product_id: '',
    stripe_price_id: ''
})

const show = computed({
    get: () => props.show,
    set: (value) => emit('update:show', value)
})

const isEdit = computed(() => !!props.plan?.id)

const isFormValid = computed(() => {
    return form.value.name.trim() !== '' && 
           form.value.type !== '' && 
           form.value.period !== '' &&
           form.value.price !== '' && 
           !errors.value.name && 
           !errors.value.type && 
           !errors.value.period &&
           !errors.value.price &&
           !errors.value.stripe_product_id &&
           !errors.value.stripe_price_id
})

const validateField = (field) => {
    errors.value[field] = ''
    
    switch (field) {
        case 'name':
            if (!form.value.name.trim()) {
                errors.value.name = 'Le nom du plan est requis'
            }
            break
        case 'type':
            if (!form.value.type) {
                errors.value.type = 'Le type de plan est requis'
            }
            break
        case 'period':
            if (!form.value.period) {
                errors.value.period = 'La période de facturation est requise'
            }
            break
        case 'price':
            if (form.value.price === '' || form.value.price === null) {
                errors.value.price = 'Le prix est requis'
            } else if (isNaN(form.value.price) || form.value.price < 0) {
                errors.value.price = 'Le prix doit être un nombre positif'
            }
            break
    }
}

const validateForm = () => {
    validateField('name')
    validateField('type')
    validateField('period')
    validateField('price')
    return isFormValid.value
}

const resetForm = () => {
    form.value = {
        name: '',
        type: 'Pro',
        period: 'Mensuel',
        stripe_product_id: '',
        stripe_price_id: '',
        price: '',
        currency: 'EUR',
        description: '',
        is_active: true
    }
    errors.value = {
        name: '',
        type: '',
        period: '',
        price: '',
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
            await fetcher.patch(`/admin/service_plans/${props.plan.id}`, form.value)
            toast.success('Plan modifié avec succès')
        } else {
            await fetcher.post('/admin/service_plans', form.value)
            toast.success('Plan créé avec succès')
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
        await fetcher.delete(`/admin/service_plans/${props.plan.id}`)
        toast.success('Plan supprimé avec succès')
        emit('deleted')
        close()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

watch(() => props.plan, (newPlan) => {
    if (newPlan) {
        form.value = { ...newPlan }
    } else {
        resetForm()
    }
    
    errors.value = {
        name: '',
        type: '',
        period: '',
        price: '',
        stripe_product_id: '',
        stripe_price_id: ''
    }
}, { immediate: true })
</script> 
