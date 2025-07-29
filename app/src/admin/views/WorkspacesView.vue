<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6">
                <h1 class="text-3xl font-bold mb-2">Espaces de travail</h1>
                <p class="text-gray-600">Gestion des espaces de travail</p>
            </div>

            <Card class="shadow-none py-5">
                <CardContent class="px-5 py-0">
                    <div class="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Nom</TableHead>
                                    <TableHead>ID Unique</TableHead>
                                    <TableHead>Devise</TableHead>
                                    <TableHead>Plan</TableHead>
                                    <TableHead>Fin d'essai</TableHead>
                                    <TableHead class="w-20"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-if="loading">
                                    <TableCell colspan="8" class="text-center py-8">
                                        <div class="flex items-center justify-center space-x-2">
                                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                            <span>Chargement...</span>
                                        </div>
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else-if="workspaces.length === 0">
                                    <TableCell colspan="8" class="text-center py-8 text-gray-500">
                                        Aucun espace de travail trouvé
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else v-for="workspace in workspaces" :key="workspace.id" class="hover:bg-gray-50">
                                    <TableCell>
                                        <div class="flex items-center space-x-3">
                                            <Avatar class="h-8 w-8">
                                                <AvatarImage 
                                                    v-if="workspace.image_url" 
                                                    v-fetcher-src.lazy
                                                    :src="`/admin/storage/download/${workspace.id}/${workspace.image_url}`" 
                                                    :alt="workspace.name" 
                                                />
                                                <AvatarFallback class="bg-blue-100 text-blue-800">
                                                    {{ workspace.name.charAt(0).toUpperCase() }}
                                                </AvatarFallback>
                                            </Avatar>
                                            <span
                                                class="font-medium text-blue-600 hover:text-blue-800 hover:underline"
                                            >
                                                {{ workspace.name || 'N/A' }}
                                            </span>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <span class="font-mono text-sm">{{ workspace.unique_id }}</span>
                                    </TableCell>
                                    <TableCell>
                                        {{ workspace.currency }}
                                    </TableCell>
                                    <TableCell>
                                        <Badge :variant="getPlanVariant(workspace.plan)" class="capitalize">
                                            {{ workspace.plan || 'Aucun' }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <span v-if="workspace.trial_end">{{ formatDate(workspace.trial_end) }}</span>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger as-child>
                                                <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                    <MoreHorizontal class="h-4 w-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem 
                                                    @click="confirmDelete(workspace)" 
                                                    class="text-red-600 focus:text-red-600"
                                                >
                                                    <Trash2 class="mr-2 h-4 w-4" />
                                                    Supprimer
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>

                    <div class="flex items-center justify-between mt-4">
                        <div class="text-sm text-gray-500">
                            Affichage de {{ ((page - 1) * itemsPerPage) + 1 }} à {{ Math.min(page * itemsPerPage, totalWorkspaces) }} sur {{ totalWorkspaces }} résultats
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
                                Page {{ page }} sur {{ Math.ceil(totalWorkspaces / itemsPerPage) }}
                            </span>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                @click="nextPage" 
                                :disabled="page >= Math.ceil(totalWorkspaces / itemsPerPage)"
                            >
                                Suivant
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <AlertDialog v-model:open="deleteDialog">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Confirmation de suppression</AlertDialogTitle>
                    <AlertDialogDescription>
                        Êtes-vous sûr de vouloir supprimer l'espace de travail "{{ selectedWorkspace?.name }}" ? 
                        Cette action est irréversible.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Annuler</AlertDialogCancel>
                    <AlertDialogAction 
                        @click="deleteWorkspace" 
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
import { useRouter } from 'vue-router'
import { useFetcher } from "@/common/composables/fetcher.js"
import { Trash2, MoreHorizontal, Pencil } from 'lucide-vue-next'
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
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
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
const router = useRouter()

const workspaces = ref([])
const loading = ref(false)
const totalWorkspaces = ref(0)
const page = ref(1)
const itemsPerPage = ref(10)
const selectedWorkspace = ref(null)
const deleteDialog = ref(false)
const deleting = ref(false)

const loadItems = async () => {
    loading.value = true
    
    try {
        const params = new URLSearchParams()
        params.append('page', page.value)
        params.append('size', itemsPerPage.value)

        const response = await fetcher.get(`/admin/workspaces?${params.toString()}`)
        const data = response.data
        workspaces.value = data.items
        totalWorkspaces.value = data.total
    } catch (error) {
        console.error('Erreur lors de la récupération des workspaces:', error)
        toast.error('Erreur lors du chargement des espaces de travail')
    } finally {
        loading.value = false
    }
}

const formatNumber = (number) => {
    return new Intl.NumberFormat().format(number)
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    }).format(date)
}

const getPlanVariant = (plan) => {
    switch (plan) {
        case 'pro':
            return 'secondary'
        case 'business':
            return 'default'
        case 'enterprise':
            return 'default'
        default:
            return 'outline'
    }
}

const confirmDelete = (workspace) => {
    selectedWorkspace.value = workspace
    deleteDialog.value = true
}

const deleteWorkspace = async () => {
    if (!selectedWorkspace.value) {
        return
    }

    deleting.value = true

    try {
        await fetcher.delete(`/admin/workspaces/${selectedWorkspace.value.id}`)
        toast.success(`Workspace "${selectedWorkspace.value.name}" supprimé avec succès`)
        deleteDialog.value = false
        loadItems()
    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

const previousPage = () => {
    if (page.value > 1) {
        page.value--
        loadItems()
    }
}

const nextPage = () => {
    if (page.value < Math.ceil(totalWorkspaces.value / itemsPerPage.value)) {
        page.value++
        loadItems()
    }
}

onMounted(() => {
    loadItems()
})
</script>
