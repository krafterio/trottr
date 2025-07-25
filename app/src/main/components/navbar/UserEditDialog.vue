<template>
    <Dialog :open="isOpen" @update:open="$emit('update:open', $event)">
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
                    <div class="col-span-3 space-y-3">
                        <div class="flex items-center gap-3">
                            <Avatar class="h-16 w-16 rounded-lg">
                                <AvatarImage :src="previewUrl || avatarUrl" :alt="editForm.name" />
                                <AvatarFallback class="rounded-lg text-lg">
                                    {{ editForm.name?.charAt(0).toUpperCase() || 'U' }}
                                </AvatarFallback>
                            </Avatar>
                            <div class="flex flex-col gap-2">
                                <Button type="button" variant="outline" size="sm" @click="triggerFileInput"
                                    :disabled="updateLoading" class="flex items-center gap-2">
                                    <Upload class="h-4 w-4" />
                                    Choisir une image
                                </Button>
                                <Button v-if="selectedFile" type="button" variant="ghost" size="sm"
                                    @click="removeSelectedFile" :disabled="updateLoading"
                                    class="flex items-center gap-2 text-red-600 hover:text-red-700">
                                    <X class="h-4 w-4" />
                                    Supprimer
                                </Button>
                            </div>
                        </div>
                        <input ref="fileInput" type="file" accept="image/*" @change="handleFileSelect" class="hidden" />
                    </div>
                </div>
            </div>
            <DialogFooter>
                <Button variant="outline" @click="$emit('update:open', false)" :disabled="updateLoading">
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
import {
    Avatar,
    AvatarFallback,
    AvatarImage,
} from '@/common/components/ui/avatar'
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
import { useFetcher } from '@/common/composables/fetcher'
import { useAuthStore } from '@/common/stores/auth'
import { Upload, X } from 'lucide-vue-next'
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

const emit = defineEmits(['update:open', 'user-updated'])

const authStore = useAuthStore()
const fetcher = useFetcher()

const editForm = ref({
    name: '',
    email: ''
})

const updateLoading = ref(false)
const selectedFile = ref(null)
const previewUrl = ref('')
const fileInput = ref(null)

const isCurrentUser = computed(() => props.user?.id === authStore.user?.id)

watch(() => props.user, (newUser) => {
    if (newUser) {
        editForm.value = {
            name: newUser.name || '',
            email: newUser.email || ''
        }
    }
}, { immediate: true })

watch(() => props.isOpen, (isOpen) => {
    if (isOpen && props.user) {
        editForm.value = {
            name: props.user.name || '',
            email: props.user.email || ''
        }
        selectedFile.value = null
        previewUrl.value = ''
        if (fileInput.value) {
            fileInput.value.value = ''
        }
    }
})

const handleFileSelect = (event) => {
    const file = event.target.files[0]
    if (file) {
        selectedFile.value = file
        const reader = new FileReader()
        reader.onload = (e) => {
            previewUrl.value = e.target.result
        }
        reader.readAsDataURL(file)
    }
}

const removeSelectedFile = () => {
    selectedFile.value = null
    previewUrl.value = ''
    if (fileInput.value) {
        fileInput.value.value = ''
    }
}

const updateProfile = async () => {
    try {
        updateLoading.value = true
        let avatarUploaded = false

        if (selectedFile.value) {
            const formData = new FormData()
            formData.append('file', selectedFile.value)

            await fetcher.post(`/account/avatar`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })

            selectedFile.value = null
            previewUrl.value = ''
            if (fileInput.value) {
                fileInput.value.value = ''
            }
            avatarUploaded = true
        }

        const hasProfileChanges = editForm.value.name !== props.user.name ||
            editForm.value.email !== props.user.email

        if (hasProfileChanges) {
            const profileData = {
                name: editForm.value.name,
                email: editForm.value.email
            }

            await fetcher.patch('/account', profileData)
            await authStore.fetchUser()

            emit('user-updated')
        }

        if (avatarUploaded || hasProfileChanges) {
            const message = avatarUploaded && hasProfileChanges ?
                'Avatar et profil mis à jour avec succès !' :
                avatarUploaded ? 'Avatar mis à jour avec succès !' :
                    'Profil mis à jour avec succès !'

            toast.success(message)
        }

        emit('update:open', false)

    } catch (error) {
        console.error('Erreur lors de la mise à jour:', error)
        toast.error('Erreur lors de la mise à jour du profil')
    } finally {
        updateLoading.value = false
    }
}
</script>