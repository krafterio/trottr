<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Invitations utilisateur</h1>
                    <p class="text-gray-600">Gestion des demandes d'accès et invitations utilisateur</p>
                </div>
                <div class="flex items-center space-x-3">
                    <Button @click="openInvitationModal">
                        <Plus :size="16" class="mr-2" />
                        Ajouter une invitation
                    </Button>
                </div>
            </div>

            <Card class="shadow-none py-5">
                <CardContent class="px-5 py-0">
                    <div class="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Nom</TableHead>
                                    <TableHead>Email</TableHead>
                                    <TableHead>Société</TableHead>
                                    <TableHead>Effectif</TableHead>
                                    <TableHead>Statut</TableHead>
                                    <TableHead>Créé le</TableHead>
                                    <TableHead class="w-20"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-if="loadingTable">
                                    <TableCell colspan="7" class="text-center py-8">
                                        <div class="flex items-center justify-center space-x-2">
                                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                            <span>Chargement...</span>
                                        </div>
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else-if="invitations.length === 0">
                                    <TableCell colspan="7" class="text-center py-8 text-gray-500">
                                        Aucune invitation trouvée
                                    </TableCell>
                                </TableRow>
                                <TableRow 
                                    v-else 
                                    v-for="invitation in invitations" 
                                    :key="invitation.id" 
                                    class="hover:bg-gray-50 cursor-pointer"
                                    @click="openInvitation(invitation)"
                                >
                                    <TableCell>
                                        <div class="flex items-center space-x-2">
                                            <User :size="16" class="text-primary" />
                                            <span class="font-medium">{{ invitation.name }}</span>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <span class="text-sm">{{ invitation.email }}</span>
                                    </TableCell>
                                    <TableCell>
                                        <span v-if="invitation.company" class="text-sm">{{ invitation.company }}</span>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge v-if="invitation.staff_range" variant="outline" class="font-mono text-xs">
                                            {{ invitation.staff_range }}
                                        </Badge>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge 
                                            v-if="invitation.invitation_code" 
                                            class="bg-green-100 text-green-800"
                                        >
                                            Code envoyé
                                        </Badge>
                                        <Badge 
                                            v-else 
                                            variant="secondary" 
                                            class="bg-orange-100 text-orange-800"
                                        >
                                            En attente
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <span class="text-sm text-gray-500">{{ formatDate(invitation.created_at) }}</span>
                                    </TableCell>
                                    <TableCell>
                                        <div class="flex items-center space-x-1">
                                            <Button 
                                                v-if="!invitation.invitation_code"
                                                variant="ghost" 
                                                size="sm" 
                                                class="h-8 w-8 p-0"
                                                @click.stop="sendInvitationCode(invitation)"
                                                :disabled="sendingCode === invitation.id"
                                            >
                                                <div v-if="sendingCode === invitation.id" class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
                                                <Send v-else :size="16" />
                                            </Button>
                                            
                                            <Button 
                                                v-else
                                                variant="ghost" 
                                                size="sm" 
                                                class="h-8 w-8 p-0"
                                                @click.stop="resendInvitationCode(invitation)"
                                                :disabled="sendingCode === invitation.id"
                                            >
                                                <div v-if="sendingCode === invitation.id" class="animate-spin rounded-full h-4 w-4 border-b-2 border-primary"></div>
                                                <RotateCcw v-else :size="16" />
                                            </Button>

                                            <DropdownMenu>
                                                <DropdownMenuTrigger as-child>
                                                    <Button variant="ghost" size="sm" class="h-8 w-8 p-0" @click.stop>
                                                        <MoreHorizontal :size="16" />
                                                    </Button>
                                                </DropdownMenuTrigger>
                                                <DropdownMenuContent align="end">
                                                    <DropdownMenuItem v-if="!invitation.invitation_code" @click="sendInvitationCode(invitation)">
                                                        <Send class="mr-2 h-4 w-4" />
                                                        Envoyer le code
                                                    </DropdownMenuItem>
                                                    
                                                    <DropdownMenuItem v-if="invitation.invitation_code" @click="resendInvitationCode(invitation)">
                                                        <RotateCcw class="mr-2 h-4 w-4" />
                                                        Renvoyer le code
                                                    </DropdownMenuItem>
                                                    
                                                    <DropdownMenuSeparator />
                                                    
                                                    <DropdownMenuItem 
                                                        @click="confirmDelete(invitation)" 
                                                        class="text-red-600 focus:text-red-600"
                                                    >
                                                        <Trash2 class="mr-2 h-4 w-4" />
                                                        Supprimer
                                                    </DropdownMenuItem>
                                                </DropdownMenuContent>
                                            </DropdownMenu>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>

                    <div class="flex items-center justify-between mt-4">
                        <div class="text-sm text-gray-500">
                            Affichage de {{ ((page - 1) * itemsPerPage) + 1 }} à {{ Math.min(page * itemsPerPage, total) }} sur {{ total }} résultats
                        </div>
                        <div class="flex items-center space-x-2">
                            <Button 
                                variant="outline" 
                                size="sm" 
                                @click="previousPage" 
                                :disabled="page === 1"
                            >
                                Précédent
                            </Button>
                            <span class="text-sm text-gray-500">
                                Page {{ page }} sur {{ Math.ceil(total / itemsPerPage) }}
                            </span>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                @click="nextPage" 
                                :disabled="page >= Math.ceil(total / itemsPerPage)"
                            >
                                Suivant
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <UserInvitationModal 
            v-model:show="invitationModal" 
            :invitation="selectedInvitation" 
            @saved="onInvitationSaved" 
            @deleted="onInvitationDeleted"
        />

        <AlertDialog v-model:open="deleteModal">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Confirmation de suppression</AlertDialogTitle>
                    <AlertDialogDescription>
                        Êtes-vous sûr de vouloir supprimer l'invitation de "{{ invitationToDelete?.name }}" ? 
                        Cette action est irréversible.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Annuler</AlertDialogCancel>
                    <AlertDialogAction 
                        @click="deleteInvitation" 
                        :disabled="deleting"
                        class="bg-red-600 hover:bg-red-700"
                    >
                        <span v-if="deleting" class="flex items-center">
                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Suppression...
                        </span>
                        <span v-else>Supprimer</span>
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
    Plus, 
    User, 
    MoreHorizontal, 
    Trash2, 
    Send, 
    RotateCcw 
} from 'lucide-vue-next'
import UserInvitationModal from '@/admin/components/modals/UserInvitationModal.vue'
import { useFetcher } from "@/common/composables/fetcher"
import { toast } from 'vue-sonner'
import { Card, CardContent } from '@/common/components/ui/card'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/common/components/ui/table'
import { Button } from '@/common/components/ui/button'
import { Badge } from '@/common/components/ui/badge'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/common/components/ui/alert-dialog'

const fetcher = useFetcher()
const loadingTable = ref(false)
const invitations = ref([])
const total = ref(0)
const page = ref(1)
const itemsPerPage = ref(50)
const invitationModal = ref(false)
const selectedInvitation = ref(null)
const deleteModal = ref(false)
const invitationToDelete = ref(null)
const deleting = ref(false)
const sendingCode = ref(null)

const formatDate = (dateString) => {
    if (!dateString) return '-'
    return new Date(dateString).toLocaleDateString('fr-FR')
}

const fetchInvitations = async () => {
    try {
        loadingTable.value = true
        const response = await fetcher.get('/admin/user_invitations', {
            params: {
                page: page.value,
                per_page: itemsPerPage.value
            }
        })
        invitations.value = response.data.items
        total.value = response.data.total
    } catch (error) {
        console.error('Erreur lors du chargement des invitations:', error)
        toast.error('Erreur lors du chargement des invitations')
    } finally {
        loadingTable.value = false
    }
}

const openInvitation = (invitation) => {
    selectedInvitation.value = invitation
    invitationModal.value = true
}

const openInvitationModal = () => {
    selectedInvitation.value = null
    invitationModal.value = true
}

const sendInvitationCode = async (invitation) => {
    try {
        sendingCode.value = invitation.id
        await fetcher.post(`/admin/user_invitations/${invitation.id}/send-code`)
        await fetchInvitations()
        toast.success('Code d\'invitation envoyé avec succès')
    } catch (error) {
        console.error('Erreur lors de l\'envoi du code:', error)
        toast.error('Erreur lors de l\'envoi du code')
    } finally {
        sendingCode.value = null
    }
}

const resendInvitationCode = async (invitation) => {
    try {
        sendingCode.value = invitation.id
        await fetcher.post(`/admin/user_invitations/${invitation.id}/send-code`)
        await fetchInvitations()
        toast.success('Code d\'invitation renvoyé avec succès')
    } catch (error) {
        console.error('Erreur lors du renvoi du code:', error)
        toast.error('Erreur lors du renvoi du code')
    } finally {
        sendingCode.value = null
    }
}

const confirmDelete = (invitation) => {
    invitationToDelete.value = invitation
    deleteModal.value = true
}

const deleteInvitation = async () => {
    if (!invitationToDelete.value) return

    deleting.value = true

    try {
        await fetcher.delete(`/admin/user_invitations/${invitationToDelete.value.id}`)
        toast.success(`Invitation de "${invitationToDelete.value.name}" supprimée avec succès`)
        deleteModal.value = false
        fetchInvitations()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

const onInvitationSaved = () => {
    invitationModal.value = false
    fetchInvitations()
}

const onInvitationDeleted = () => {
    invitationModal.value = false
    fetchInvitations()
}

const previousPage = () => {
    if (page.value > 1) {
        page.value--
        fetchInvitations()
    }
}

const nextPage = () => {
    if (page.value < Math.ceil(total.value / itemsPerPage.value)) {
        page.value++
        fetchInvitations()
    }
}

onMounted(() => {
    fetchInvitations()
})
</script> 

