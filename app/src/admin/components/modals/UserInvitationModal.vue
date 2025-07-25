<template>
    <Dialog v-model:open="show">
        <DialogContent class="sm:max-w-2xl">
            <DialogHeader>
                <DialogTitle class="flex items-center">
                    <User :size="20" class="mr-2" />
                    {{ isEdit ? 'Modifier l\'invitation' : 'Nouvelle invitation' }}
                </DialogTitle>
                <DialogDescription>
                    {{ isEdit ? 'Modifiez les informations de l\'invitation.' : 'Créez une nouvelle invitation utilisateur.' }}
                </DialogDescription>
            </DialogHeader>

            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="name">Nom complet</Label>
                        <Input 
                            id="name"
                            v-model="form.name" 
                            placeholder="Nom complet" 
                            :class="errors.name ? 'border-red-500' : ''"
                            @blur="validateField('name')"
                        />
                        <p v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="email">Email</Label>
                        <Input 
                            id="email"
                            v-model="form.email" 
                            type="email"
                            placeholder="email@exemple.com" 
                            :class="errors.email ? 'border-red-500' : ''"
                            @blur="validateField('email')"
                        />
                        <p v-if="errors.email" class="text-sm text-red-500">{{ errors.email }}</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="space-y-2">
                        <Label for="company">Société (optionnel)</Label>
                        <Input 
                            id="company"
                            v-model="form.company" 
                            placeholder="Nom de la société" 
                        />
                        <p class="text-sm text-gray-500">Société de l'utilisateur</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="staff_range">Effectif (optionnel)</Label>
                        <Select v-model="form.staff_range">
                            <SelectTrigger>
                                <SelectValue placeholder="Sélectionnez l'effectif" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="1-10">1-10 employés</SelectItem>
                                <SelectItem value="10-50">10-50 employés</SelectItem>
                                <SelectItem value="50-200">50-200 employés</SelectItem>
                                <SelectItem value="200-500">200-500 employés</SelectItem>
                                <SelectItem value="500-1K">500-1K employés</SelectItem>
                                <SelectItem value="1K-5K">1K-5K employés</SelectItem>
                                <SelectItem value="5K-10K">5K-10K employés</SelectItem>
                                <SelectItem value="> 10K">> 10K employés</SelectItem>
                            </SelectContent>
                        </Select>
                        <p class="text-sm text-gray-500">Taille de l'entreprise</p>
                    </div>
                </div>

                <div v-if="form.invitation_code" class="space-y-2">
                    <Label for="invitation_code">Code d'invitation</Label>
                    <Input 
                        id="invitation_code"
                        v-model="form.invitation_code" 
                        readonly
                        class="bg-gray-50"
                    />
                    <p class="text-sm text-gray-500">Code généré automatiquement</p>
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
import { User } from 'lucide-vue-next'
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
import { Label } from '@/common/components/ui/label'
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
    invitation: {
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
    email: '',
    company: '',
    staff_range: '',
    invitation_code: ''
})

const errors = ref({
    name: '',
    email: ''
})

const isEdit = computed(() => !!props.invitation)

const show = computed({
    get: () => props.show,
    set: (value) => emit('update:show', value)
})

const isFormValid = computed(() => {
    return form.value.name && 
           form.value.email && 
           !errors.value.name && 
           !errors.value.email
})

const validateField = (field) => {
    errors.value[field] = ''
    
    if (field === 'name') {
        if (!form.value.name.trim()) {
            errors.value.name = 'Le nom est requis'
        }
    }
    
    if (field === 'email') {
        if (!form.value.email.trim()) {
            errors.value.email = 'L\'email est requis'
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
            errors.value.email = 'L\'email doit être valide'
        }
    }
}

const resetForm = () => {
    form.value = {
        name: '',
        email: '',
        company: '',
        staff_range: '',
        invitation_code: ''
    }
    errors.value = {
        name: '',
        email: ''
    }
}

const loadInvitation = () => {
    if (props.invitation) {
        form.value = {
            name: props.invitation.name || '',
            email: props.invitation.email || '',
            company: props.invitation.company || '',
            staff_range: props.invitation.staff_range || '',
            invitation_code: props.invitation.invitation_code || ''
        }
    } else {
        resetForm()
    }
}

const handleSubmit = async () => {
    // Validate all fields
    validateField('name')
    validateField('email')
    
    if (!isFormValid.value) return

    try {
        saving.value = true

        const payload = {
            name: form.value.name,
            email: form.value.email,
            company: form.value.company || null,
            staff_range: form.value.staff_range || null
        }

        if (isEdit.value) {
            await fetcher.patch(`/admin/user_invitations/${props.invitation.id}`, payload)
            toast.success('Invitation modifiée avec succès')
        } else {
            await fetcher.post('/admin/user_invitations', payload)
            toast.success('Invitation créée avec succès')
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
    if (!props.invitation) return

    try {
        deleting.value = true
        await fetcher.delete(`/admin/user_invitations/${props.invitation.id}`)
        toast.success('Invitation supprimée avec succès')
        emit('deleted')
        close()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

const close = () => {
    show.value = false
}

watch(() => props.show, (newShow) => {
    if (newShow) {
        loadInvitation()
    }
})

watch(() => props.invitation, () => {
    if (props.show) {
        loadInvitation()
    }
})
</script> 
