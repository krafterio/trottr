<template>
    <div class="max-w-5xl space-y-6">
        <div>
            <h2 class="text-lg font-semibold">Utilisateurs</h2>
            <p class="text-muted-foreground">Gérez les utilisateurs de votre organisation.</p>
        </div>

        <div class="flex items-center justify-between">
            <div>
                <h3 class="text-base font-medium">Membres de l'équipe</h3>
                <p class="text-sm text-muted-foreground">{{ users.length }} utilisateur(s) actif(s)</p>
            </div>
            <Button @click="showInviteDialog = true">
                <Plus class="h-4 w-4 mr-2" />
                Inviter un utilisateur
            </Button>
        </div>

        <div class="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Utilisateur</TableHead>
                        <TableHead>Rôle</TableHead>
                        <TableHead>Statut</TableHead>
                        <TableHead class="w-20">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow v-if="loading">
                        <TableCell colspan="4" class="text-center py-8">
                            <div class="flex items-center justify-center space-x-2">
                                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                <span>Chargement...</span>
                            </div>
                        </TableCell>
                    </TableRow>
                    <TableRow v-else-if="error">
                        <TableCell colspan="4" class="text-center py-8">
                            <div class="text-destructive">
                                Erreur lors du chargement des utilisateurs: {{ error.message }}
                            </div>
                        </TableCell>
                    </TableRow>
                    <TableRow v-else-if="users.length === 0">
                        <TableCell colspan="4" class="text-center py-8 text-muted-foreground">
                            Aucun utilisateur trouvé
                        </TableCell>
                    </TableRow>
                    <TableRow v-else v-for="user in users" :key="user.id">
                        <TableCell>
                            <div class="flex items-center space-x-3">
                                <Avatar class="w-8 h-8 rounded-md">
                                    <AvatarImage v-if="user.avatar" :src="`/storage/download/${user.avatar}`"
                                        v-fetcher-src.lazy :alt="user.name || user.email" />
                                    <AvatarFallback class="bg-primary/10 text-primary text-xs font-medium rounded-md">
                                        {{ user.initials || getInitials(user.name, user.email) }}
                                    </AvatarFallback>
                                </Avatar>
                                <div>
                                    <div class="font-medium">{{ user.name || user.email }}</div>
                                    <div class="text-sm text-muted-foreground">{{ user.email }}</div>
                                </div>
                            </div>
                        </TableCell>
                        <TableCell>
                            <Badge :variant="getRoleBadgeVariant(user.role)">
                                {{ getRoleLabel(user.role) }}
                            </Badge>
                        </TableCell>
                        <TableCell>
                            <Badge variant="secondary">
                                Actif
                            </Badge>
                        </TableCell>
                        <TableCell>
                            <div class="flex items-center space-x-1">
                                <Button variant="ghost" size="sm" @click="openEditDialog(user)">
                                    <Edit class="h-4 w-4" />
                                </Button>
                                <Button v-if="user.role !== 'Owner'" variant="ghost" size="sm"
                                    @click="removeUser(user)">
                                    <Trash class="h-4 w-4" />
                                </Button>
                            </div>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>

        <!-- Section Invitations en cours -->
        <div class="space-y-4">
            <div class="flex items-center justify-between">
                <div>
                    <h3 class="text-base font-medium">Invitations en cours</h3>
                    <p class="text-sm text-muted-foreground">{{ invitations.length }} invitation(s) en attente</p>
                </div>
            </div>

            <div class="rounded-md border">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Email</TableHead>
                            <TableHead>Envoyée le</TableHead>
                            <TableHead>Expire le</TableHead>
                            <TableHead class="w-20">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        <TableRow v-if="loadingInvitations">
                            <TableCell colspan="4" class="text-center py-8">
                                <div class="flex items-center justify-center space-x-2">
                                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                    <span>Chargement des invitations...</span>
                                </div>
                            </TableCell>
                        </TableRow>
                        <TableRow v-else-if="invitations.length === 0">
                            <TableCell colspan="4" class="text-center py-8 text-muted-foreground">
                                Aucune invitation en cours
                            </TableCell>
                        </TableRow>
                        <TableRow v-else v-for="invitation in invitations" :key="invitation.id">
                            <TableCell>
                                <div class="flex items-center space-x-3">
                                    <div
                                        class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center text-yellow-600 text-xs font-medium">
                                        <Mail class="h-4 w-4" />
                                    </div>
                                    <div>
                                        <div class="font-medium">{{ invitation.email }}</div>
                                        <div class="text-sm text-muted-foreground">Invitation envoyée</div>
                                    </div>
                                </div>
                            </TableCell>
                            <TableCell>
                                <div class="text-sm">{{ formatDate(invitation.created_at) }}</div>
                            </TableCell>
                            <TableCell>
                                <div class="text-sm">{{ formatDate(invitation.expires_at) }}</div>
                            </TableCell>
                            <TableCell>
                                <Button variant="ghost" size="sm" @click="cancelInvitation(invitation)"
                                    class="text-destructive hover:text-destructive">
                                    <X class="h-4 w-4" />
                                </Button>
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </div>
        </div>

        <!-- Dialog d'invitation -->
        <Dialog v-model:open="showInviteDialog">
            <DialogContent class="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle>Inviter un utilisateur</DialogTitle>
                    <DialogDescription>
                        Saisissez l'adresse email de la personne que vous souhaitez inviter dans votre workspace.
                    </DialogDescription>
                </DialogHeader>
                <form @submit.prevent="sendInvitation" class="space-y-4">
                    <div class="space-y-2">
                        <Label for="invite-email">Email</Label>
                        <Input id="invite-email" v-model="inviteForm.email" type="email"
                            placeholder="exemple@domaine.com" :disabled="inviteLoading" required />
                    </div>
                    <DialogFooter>
                        <Button type="button" variant="outline" @click="showInviteDialog = false"
                            :disabled="inviteLoading">
                            Annuler
                        </Button>
                        <Button type="submit" :disabled="inviteLoading || !inviteForm.email">
                            <span v-if="inviteLoading">Envoi...</span>
                            <span v-else>Envoyer l'invitation</span>
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>

        <!-- Dialog d'édition utilisateur -->
        <UserEditDialog :is-open="showEditDialog" :user="selectedUser" />

        <!-- Dialog de confirmation de suppression -->
        <ConfirmDeleteDialog :show="showDeleteDialog" :title="deleteDialogData.title"
            :message="deleteDialogData.message" :item-name="deleteDialogData.itemName" :loading="deleteLoading" />
    </div>
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import { Badge } from '@/common/components/ui/badge'
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
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/common/components/ui/table'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import ConfirmDeleteDialog from '@/main/components/dialogs/ConfirmDeleteDialog.vue'
import UserEditDialog from '@/main/components/dialogs/UserEditDialog.vue'
import { useWorkspaceStore } from '@/main/stores/workspace'
import { Edit, Mail, Plus, Trash, X } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { toast } from 'vue-sonner'

const users = ref([])
const invitations = ref([])
const loading = ref(false)
const loadingInvitations = ref(false)
const error = ref(null)
const fetcher = useFetcher()
const workspaceStore = useWorkspaceStore()

const showInviteDialog = ref(false)
const showEditDialog = ref(false)
const showDeleteDialog = ref(false)
const selectedUser = ref(null)
const inviteLoading = ref(false)
const editLoading = ref(false)
const deleteLoading = ref(false)

const deleteDialogData = ref({
    title: '',
    message: '',
    itemName: '',
    action: null,
    data: null
})

const inviteForm = ref({
    email: ''
})

const editForm = ref({
    id: null,
    name: '',
    email: '',
    role: ''
})

useBus(bus, 'confirm-delete-dialog:update-show', (event) => {
    showDeleteDialog.value = event.detail
})

useBus(bus, 'confirm-delete-dialog:confirm', () => {
    confirmDelete()
})

useBus(bus, 'confirm-delete-dialog:cancel', () => {
    cancelDelete()
})

useBus(bus, 'user-edit-dialog:update-open', (event) => {
    showEditDialog.value = event.detail
})

useBus(bus, 'user-edit-dialog:user-updated', () => {
    fetchUsers()
})

const fetchUsers = async () => {
    loading.value = true
    error.value = null

    try {
        const response = await fetcher.get('/workspace/members')
        users.value = response.data.items || []
    } catch (err) {
        console.error('Erreur lors du chargement des utilisateurs:', err)
        error.value = err
    } finally {
        loading.value = false
    }
}

const fetchInvitations = async () => {
    loadingInvitations.value = true

    try {
        const response = await fetcher.get('/workspace/invitations')
        invitations.value = response.data || []
    } catch (err) {
        console.error('Erreur lors du chargement des invitations:', err)
    } finally {
        loadingInvitations.value = false
    }
}

const sendInvitation = async () => {
    if (!inviteForm.value.email) return

    inviteLoading.value = true

    try {
        const response = await fetcher.post('/workspace/invite', {
            email: inviteForm.value.email
        })

        toast.success('Invitation envoyée avec succès !')
        showInviteDialog.value = false
        inviteForm.value.email = ''
        await fetchInvitations()

    } catch (err) {
        console.error('Erreur lors de l\'envoi de l\'invitation:', err)
        const errorMessage = err.response?.data?.detail || 'Erreur lors de l\'envoi de l\'invitation'
        toast.error(errorMessage)
    } finally {
        inviteLoading.value = false
    }
}

const openEditDialog = (user) => {
    selectedUser.value = user
    showEditDialog.value = true
}

const updateUser = async () => {
    if (!editForm.value.id) return

    const currentUser = users.value.find(u => u.id === editForm.value.id)
    if (!currentUser || currentUser.role === editForm.value.role) {
        showEditDialog.value = false
        return
    }

    editLoading.value = true

    try {
        if (currentUser.role === 'Owner' && editForm.value.role === 'Member') {
            await fetcher.patch(`/workspace/member/${editForm.value.id}`)
            toast.success('Propriétaire rétrogradé en membre avec succès !')
        } else if (currentUser.role === 'Member' && editForm.value.role === 'Owner') {
            await fetcher.patch(`/workspace/owner/${editForm.value.id}`)
            toast.success('Membre promu propriétaire avec succès !')
        }

        showEditDialog.value = false
        await fetchUsers()

    } catch (err) {
        console.error('Erreur lors de la mise à jour de l\'utilisateur:', err)
        const errorMessage = err.response?.data?.detail || 'Erreur lors de la mise à jour de l\'utilisateur'
        toast.error(errorMessage)
    } finally {
        editLoading.value = false
    }
}

const removeUser = (user) => {
    if (user.role === 'Owner') return

    deleteDialogData.value = {
        title: 'Supprimer l\'utilisateur',
        message: 'Êtes-vous sûr de vouloir supprimer cet utilisateur du workspace ?',
        itemName: user.name || user.email,
        action: 'removeUser',
        data: user
    }
    showDeleteDialog.value = true
}

const getInitials = (name, email) => {
    if (name) {
        return name.split(' ').map(word => word[0]).join('').toUpperCase().slice(0, 2)
    }
    if (email) {
        return email.slice(0, 2).toUpperCase()
    }
    return 'U'
}

const getRoleLabel = (role) => {
    switch (role) {
        case 'Owner': return 'Propriétaire'
        case 'Member': return 'Membre'
        default: return role
    }
}

const getRoleBadgeVariant = (role) => {
    switch (role) {
        case 'Owner': return 'default'
        case 'Member': return 'secondary'
        default: return 'outline'
    }
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    })
}

const cancelInvitation = (invitation) => {
    deleteDialogData.value = {
        title: 'Annuler l\'invitation',
        message: 'Êtes-vous sûr de vouloir annuler cette invitation ?',
        itemName: invitation.email,
        action: 'cancelInvitation',
        data: invitation
    }
    showDeleteDialog.value = true
}

const confirmDelete = async () => {
    const { action, data } = deleteDialogData.value
    deleteLoading.value = true

    try {
        if (action === 'removeUser') {
            await fetcher.delete(`/workspace/member/${data.id}`)
            toast.success('Utilisateur supprimé avec succès !')
            await fetchUsers()
        } else if (action === 'cancelInvitation') {
            await fetcher.delete(`/workspace/invitation/${data.id}`)
            toast.success('Invitation annulée avec succès !')
            await fetchInvitations()
        }

        showDeleteDialog.value = false

    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        const errorMessage = err.response?.data?.detail || 'Erreur lors de la suppression'
        toast.error(errorMessage)
    } finally {
        deleteLoading.value = false
    }
}

const cancelDelete = () => {
    showDeleteDialog.value = false
}

onMounted(async () => {
    await workspaceStore.fetchWorkspace()
    await fetchUsers()
    await fetchInvitations()
})
</script>