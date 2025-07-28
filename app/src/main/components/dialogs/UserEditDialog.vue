<template>
    <Dialog :open="isOpen" @update:open="bus.trigger('user-edit-dialog:update-open', $event)">
        <DialogContent class="sm:max-w-[625px]">
            <DialogHeader>
                <DialogTitle>Modifier l'utilisateur</DialogTitle>
                <DialogDescription>
                    Modifiez les informations de cet utilisateur. Seuls les propriétaires peuvent modifier les autres
                    utilisateurs.
                </DialogDescription>
            </DialogHeader>
            <div class="grid gap-4 py-4">
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="name" class="text-right">
                        Nom
                    </Label>
                    <Input id="name" v-model="editForm.name" class="col-span-3" :disabled="updateLoading" />
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="email" class="text-right">
                        Email
                    </Label>
                    <Input id="email" v-model="editForm.email" type="email" class="col-span-3" disabled readonly />
                    <div class="col-span-4 text-xs text-muted-foreground">
                        L'email ne peut pas être modifié pour les autres utilisateurs
                    </div>
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="avatar" class="text-right">
                        Avatar
                    </Label>
                    <div class="col-span-3">
                        <ImagePicker v-model="avatarPath" avatar :alt="editForm.name || 'Avatar utilisateur'"
                            help-text="Formats acceptés : JPG, PNG, GIF, WebP. Taille max : 5MB"
                            @upload="handleAvatarUpload" @remove="handleAvatarRemove" />
                    </div>
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="role" class="text-right">
                        Rôle
                    </Label>
                    <div class="col-span-3">
                        <Select v-model="editForm.role" :disabled="updateLoading">
                            <SelectTrigger>
                                <SelectValue placeholder="Sélectionner un rôle" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="Member">Membre</SelectItem>
                                <SelectItem value="Owner">Propriétaire</SelectItem>
                                <SelectItem value="Operator">Technicien</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </div>
                <div class="grid grid-cols-4 items-center gap-4" v-if="editForm.role === 'Operator'">
                    <Label for="specialities" class="text-right">
                        Spécialités
                    </Label>
                    <div class="col-span-3">
                        <JobSpecialityMultiSelect :modelValue="editForm.specialities"
                            @update:modelValue="(value) => editForm.specialities = value"
                            :specialities="availableSpecialities" :disabled="updateLoading" />
                    </div>
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="zone" class="text-right">
                        Zone
                    </Label>
                    <Input id="zone" v-model="editForm.zone" class="col-span-3" :disabled="updateLoading"
                        placeholder="Zone d'intervention" />
                </div>
                <div class="grid grid-cols-4 items-center gap-4">
                    <Label for="phone" class="text-right">
                        Téléphone
                    </Label>
                    <Input id="phone" v-model="editForm.phone" class="col-span-3" :disabled="updateLoading"
                        placeholder="Numéro de téléphone" />
                </div>
            </div>
            <DialogFooter>
                <Button variant="outline" @click="bus.trigger('user-edit-dialog:update-open', false)"
                    :disabled="updateLoading">
                    Annuler
                </Button>
                <Button type="submit" @click="updateUser" :disabled="updateLoading">
                    <span v-if="updateLoading">Sauvegarde...</span>
                    <span v-else>Sauvegarder</span>
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import ImagePicker from '@/common/components/form/ImagePicker.vue'
import JobSpecialityMultiSelect from '@/common/components/form/JobSpecialityMultiSelect.vue'
import { Button } from '@/common/components/ui/button'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/common/components/ui/select'
import { bus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useAuthStore } from '@/common/stores/auth'
import { computed, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    user: {
        type: Object,
        default: null
    }
})

const authStore = useAuthStore()
const fetcher = useFetcher()

const isCurrentUser = computed(() => props.user?.id === authStore.user?.id)

const editForm = ref({
    name: '',
    email: '',
    role: '',
    zone: '',
    phone: '',
    specialities: []
})

const avatarPath = ref(null)
const availableSpecialities = ref([])

const updateLoading = ref(false)

const loadSpecialities = async () => {
    try {
        const response = await fetcher.get('/job-speciality')
        availableSpecialities.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des spécialités:', error)
    }
}

const loadUserDetails = async (userId) => {
    try {
        const response = await fetcher.get(`/workspace/members/${userId}`)
        return response.data
    } catch (error) {
        console.error('Erreur lors du chargement des détails utilisateur:', error)
        return null
    }
}

watch(() => props.user, (newUser) => {
    if (newUser) {
        editForm.value = {
            name: newUser.name || '',
            email: newUser.email || '',
            role: newUser.role || 'Member',
            zone: newUser.zone || '',
            phone: newUser.phone || '',
            specialities: newUser.job_specialities || []
        }
        avatarPath.value = newUser.avatar || null
    }
}, { immediate: true })

watch(() => props.isOpen, async (isOpen) => {
    if (isOpen && props.user) {
        // Load user details with specialities
        const userDetails = await loadUserDetails(props.user.id)

        editForm.value = {
            name: props.user.name || '',
            email: props.user.email || '',
            role: props.user.role || 'Member',
            zone: userDetails?.zone || '',
            phone: userDetails?.phone || '',
            specialities: userDetails?.job_specialities || []
        }
        avatarPath.value = props.user.avatar || null
        loadSpecialities()
    }
})

const handleAvatarUpload = async (file) => {
    try {
        updateLoading.value = true
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetcher.post(`/storage/upload/users/${props.user.id}/avatar`, formData)
        avatarPath.value = response.data

        // Si c'est l'utilisateur connecté, rafraîchir authStore
        if (isCurrentUser.value) {
            await authStore.fetchUser()
            bus.trigger('account-dialog:user-updated', { user: props.user })
        }

        bus.trigger('user-edit-dialog:user-updated', { user: props.user })
        toast.success('Avatar mis à jour avec succès !')
    } catch (error) {
        console.error('Erreur lors du téléchargement de l\'avatar:', error)
        toast.error('Erreur lors du téléchargement de l\'avatar')
    } finally {
        updateLoading.value = false
    }
}

const handleAvatarRemove = async () => {
    try {
        updateLoading.value = true

        await fetcher.delete(`/storage/file/users/${props.user.id}/avatar`)
        avatarPath.value = null

        // Si c'est l'utilisateur connecté, rafraîchir authStore
        if (isCurrentUser.value) {
            await authStore.fetchUser()
            bus.trigger('account-dialog:user-updated', { user: props.user })
        }

        bus.trigger('user-edit-dialog:user-updated', { user: props.user })
        toast.success('Avatar supprimé avec succès !')
    } catch (error) {
        console.error('Erreur lors de la suppression de l\'avatar:', error)
        toast.error('Erreur lors de la suppression de l\'avatar')
    } finally {
        updateLoading.value = false
    }
}

const updateUser = async () => {
    try {
        updateLoading.value = true

        const hasChanges = editForm.value.name !== props.user.name ||
            editForm.value.role !== props.user.role ||
            editForm.value.zone !== props.user.zone ||
            editForm.value.phone !== props.user.phone ||
            JSON.stringify(editForm.value.specialities.map(s => s.id).sort()) !== JSON.stringify((props.user.job_specialities || []).map(s => s.id).sort())

        if (hasChanges) {
            const updateData = {}

            if (editForm.value.name !== props.user.name) {
                updateData.name = editForm.value.name
            }

            if (editForm.value.role !== props.user.role) {
                updateData.role = editForm.value.role
            }

            if (editForm.value.zone !== props.user.zone) {
                updateData.zone = editForm.value.zone
            }

            if (editForm.value.phone !== props.user.phone) {
                updateData.phone = editForm.value.phone
            }

            if (JSON.stringify(editForm.value.specialities.map(s => s.id).sort()) !== JSON.stringify((props.user.job_specialities || []).map(s => s.id).sort())) {
                updateData.job_speciality_ids = editForm.value.specialities.map(s => s.id)
            }

            await fetcher.patch(`/workspace/member/${props.user.id}/profile`, updateData)

            // Si c'est l'utilisateur connecté, rafraîchir authStore
            if (isCurrentUser.value) {
                await authStore.fetchUser()
                bus.trigger('account-dialog:user-updated', { user: props.user })
            }

            bus.trigger('user-edit-dialog:user-updated', { user: props.user })
            toast.success('Utilisateur mis à jour avec succès !')
        }

        bus.trigger('user-edit-dialog:update-open', false)

    } catch (error) {
        console.error('Erreur lors de la mise à jour:', error)
        toast.error('Erreur lors de la mise à jour de l\'utilisateur')
    } finally {
        updateLoading.value = false
    }
}
</script>