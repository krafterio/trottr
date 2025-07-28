<template>
    <Dialog :open="isOpen" @update:open="bus.trigger('account-dialog:update-open', $event)">
        <DialogContent class="sm:max-w-[425px]">
            <DialogHeader>
                <DialogTitle>Modifier le profil</DialogTitle>
                <DialogDescription>
                    Modifiez vos informations personnelles. Cliquez sur sauvegarder pour enregistrer les modifications.
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
                    <Input id="email" v-model="editForm.email" type="email" class="col-span-3"
                        :disabled="updateLoading" />
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
            </div>
            <DialogFooter>
                <Button variant="outline" @click="bus.trigger('account-dialog:update-open', false)"
                    :disabled="updateLoading">
                    Annuler
                </Button>
                <Button type="submit" @click="updateProfile" :disabled="updateLoading">
                    <span v-if="updateLoading">Sauvegarde...</span>
                    <span v-else>Sauvegarder</span>
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import ImagePicker from '@/common/components/form/ImagePicker.vue'
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

const editForm = ref({
    name: '',
    email: ''
})

const updateLoading = ref(false)
const avatarPath = ref('')

const isCurrentUser = computed(() => props.user?.id === authStore.user?.id)

watch(() => props.user, (newUser) => {
    if (newUser) {
        editForm.value = {
            name: newUser.name || '',
            email: newUser.email || ''
        }
        avatarPath.value = newUser.avatar || ''
    }
}, { immediate: true })

watch(() => props.isOpen, (isOpen) => {
    if (isOpen && props.user) {
        editForm.value = {
            name: props.user.name || '',
            email: props.user.email || ''
        }
        avatarPath.value = props.user.avatar || ''
    }
})

const handleAvatarUpload = async (file) => {
    try {
        updateLoading.value = true

        const formData = new FormData()
        formData.append('file', file)

        const response = await fetcher.post(`/account/upload-image`, formData)
        avatarPath.value = response.data.avatar

        // Rafraîchir les données utilisateur immédiatement
        if (isCurrentUser.value) {
            await authStore.fetchUser()
        }

        toast.success('Avatar mis à jour avec succès !')

    } catch (error) {
        console.error('Erreur lors de l\'upload:', error)
        toast.error('Erreur lors de la mise à jour de l\'avatar')
    } finally {
        updateLoading.value = false
    }
}

const handleAvatarRemove = async () => {
    try {
        updateLoading.value = true

        await fetcher.delete('/account/image')
        avatarPath.value = ''

        // Rafraîchir les données utilisateur immédiatement
        if (isCurrentUser.value) {
            await authStore.fetchUser()
        }

        toast.success('Avatar supprimé avec succès !')

    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression de l\'avatar')
    } finally {
        updateLoading.value = false
    }
}

const updateProfile = async () => {
    try {
        updateLoading.value = true

        const hasProfileChanges = editForm.value.name !== props.user.name ||
            editForm.value.email !== props.user.email

        if (hasProfileChanges) {
            const profileData = {
                name: editForm.value.name,
                email: editForm.value.email
            }

            if (isCurrentUser.value) {
                // Modifier son propre profil
                await fetcher.patch('/account', profileData)

                // Rafraîchir les données utilisateur
                await authStore.fetchUser()
            } else {
                // Pour les autres utilisateurs, on ne peut modifier que le nom
                // car l'email est unique et géré différemment
                if (editForm.value.name !== props.user.name) {
                    // Il faudrait un endpoint spécifique pour ça
                    // Pour l'instant, on affiche une erreur
                    throw new Error("La modification d'autres utilisateurs n'est pas encore supportée")
                }
            }

            bus.trigger('account-dialog:user-updated', { user: props.user })
            toast.success('Profil mis à jour avec succès !')
        }

        bus.trigger('account-dialog:update-open', false)

    } catch (error) {
        console.error('Erreur lors de la mise à jour:', error)
        if (error.message) {
            toast.error(error.message)
        } else {
            toast.error('Erreur lors de la mise à jour du profil')
        }
    } finally {
        updateLoading.value = false
    }
}
</script>