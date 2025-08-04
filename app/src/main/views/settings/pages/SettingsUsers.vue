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
                    <div class="space-y-2" v-if="workspaceStore.workspace && workspaceStore.workspace.member_count >= workspaceStore.workspace.available_member_count">
                        <div class="rounded-md border border-orange-200 bg-orange-50 p-3">
                            <div class="flex">
                                <div class="flex-shrink-0">
                                    <svg class="h-5 w-5 text-orange-400" viewBox="0 0 20 20" fill="currentColor">
                                        <path fill-rule="evenodd" d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd" />
                                    </svg>
                                </div>
                                <div class="ml-3">
                                    <p class="text-sm text-orange-800">
                                        Limite d'utilisateurs atteinte ({{ workspaceStore.workspace.member_count }}/{{ workspaceStore.workspace.available_member_count }}). 
                                        Vous devez ajouter au moins 1 utilisateur supplémentaire.
                                    </p>
                                </div>
                            </div>
                        </div>
                        <Label for="additional-users">Utilisateurs supplémentaires</Label>
                        <Input 
                            id="additional-users" 
                            v-model.number="inviteForm.additional_users" 
                            type="number"
                            min="1"
                            placeholder="1"
                            :disabled="inviteLoading" 
                            required
                        />
                        <p class="text-sm text-muted-foreground">
                            Votre abonnement sera mis à jour automatiquement.
                        </p>
                    </div>
                    <DialogFooter>
                        <Button type="button" variant="outline" @click="showInviteDialog = false"
                            :disabled="inviteLoading">
                            Annuler
                        </Button>
                        <Button type="submit" :disabled="inviteLoading || !inviteForm.email || (workspaceStore.workspace && workspaceStore.workspace.member_count >= workspaceStore.workspace.available_member_count && (!inviteForm.additional_users || inviteForm.additional_users < 1))">
                            <span v-if="inviteLoading">Envoi...</span>
                            <span v-else-if="workspaceStore.workspace && workspaceStore.workspace.member_count >= workspaceStore.workspace.available_member_count">Mettre à jour et inviter</span>
                            <span v-else>Envoyer l'invitation</span>
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>


        <!-- Dialog d'édition utilisateur -->
        <UserEditDialog :is-open="showEditDialog" :user="selectedUser" />
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
const selectedUser = ref(null)
const inviteLoading = ref(false)
const editLoading = ref(false)

const inviteForm = ref({
    email: '',
    additional_users: 1
})

const editForm = ref({
    id: null,
    name: '',
    email: '',
    role: ''
})

// Écoute la confirmation de suppression d'utilisateur
useBus(bus, 'confirm-delete-user:confirmed', () => {
    deleteUser()
})

// Écoute la confirmation d'annulation d'invitation
useBus(bus, 'confirm-cancel-invitation:confirmed', () => {
    deleteCancelInvitation()
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
        const payload = { email: inviteForm.value.email }
        if (inviteForm.value.additional_users > 0) {
            payload.additional_users = inviteForm.value.additional_users
        }

        const response = await fetcher.post('/workspace/invite', payload)

        toast.success('Invitation envoyée avec succès !')
        showInviteDialog.value = false
        inviteForm.value.email = ''
        inviteForm.value.additional_users = 1
        await fetchInvitations()
        await workspaceStore.fetchWorkspace()

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

const selectedUserForDelete = ref(null)

const removeUser = (user) => {
    if (user.role === 'Owner') return

    selectedUserForDelete.value = user

    bus.trigger('confirm-delete', {
        title: 'Supprimer l\'utilisateur',
        message: 'Êtes-vous sûr de vouloir supprimer cet utilisateur du workspace ?',
        itemName: user.name || user.email,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-user:confirmed'
    })
}

const deleteUser = async () => {
    if (!selectedUserForDelete.value) return

    try {
        await fetcher.delete(`/workspace/member/${selectedUserForDelete.value.id}`)
        toast.success('Utilisateur supprimé avec succès !')
        bus.trigger('confirm-delete-dialog:close')
        await fetchUsers()
        selectedUserForDelete.value = null
    } catch (err) {
        console.error('Erreur lors de la suppression:', err)
        const errorMessage = err.response?.data?.detail || 'Erreur lors de la suppression'
        toast.error(errorMessage)
        bus.trigger('confirm-delete-dialog:close')
    }
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

const selectedInvitationForCancel = ref(null)

const cancelInvitation = (invitation) => {
    selectedInvitationForCancel.value = invitation

    bus.trigger('confirm-delete', {
        title: 'Annuler l\'invitation',
        message: 'Êtes-vous sûr de vouloir annuler cette invitation ?',
        itemName: invitation.email,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-cancel-invitation:confirmed'
    })
}

const deleteCancelInvitation = async () => {
    if (!selectedInvitationForCancel.value) return

    try {
        await fetcher.delete(`/workspace/invitation/${selectedInvitationForCancel.value.id}`)
        toast.success('Invitation annulée avec succès !')
        bus.trigger('confirm-delete-dialog:close')
        await fetchInvitations()
        selectedInvitationForCancel.value = null
    } catch (err) {
        console.error('Erreur lors de l\'annulation de l\'invitation:', err)
        const errorMessage = err.response?.data?.detail || 'Erreur lors de l\'annulation de l\'invitation'
        toast.error(errorMessage)
        bus.trigger('confirm-delete-dialog:close')
    }
}

onMounted(async () => {
    await workspaceStore.fetchWorkspace()
    await fetchUsers()
    await fetchInvitations()
})
</script>