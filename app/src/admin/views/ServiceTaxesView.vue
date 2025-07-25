<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Taxes des services</h1>
                    <p class="text-gray-600">Gestion des taxes des services par pays et région</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <Switch 
                            v-model:checked="showInactiveTaxes" 
                            @update:checked="onToggleInactiveTaxes"
                        />
                        <Label class="text-sm">Afficher inactives</Label>
                    </div>
                    <Button @click="openTaxModal">
                        <Plus :size="16" class="mr-2" />
                        Ajouter une taxe
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
                                    <TableHead>Pourcentage</TableHead>
                                    <TableHead>Pays</TableHead>
                                    <TableHead>Région</TableHead>
                                    <TableHead>Description</TableHead>
                                    <TableHead>Statut</TableHead>
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
                                <TableRow v-else-if="taxes.length === 0">
                                    <TableCell colspan="7" class="text-center py-8 text-gray-500">
                                        Aucune taxe trouvée
                                    </TableCell>
                                </TableRow>
                                <TableRow 
                                    v-else 
                                    v-for="tax in taxes" 
                                    :key="tax.id" 
                                    class="hover:bg-gray-50"
                                    :class="{ 'opacity-60': !tax.is_active }"
                                >
                                    <TableCell>
                                        <span class="font-medium" :class="{ 'text-gray-500': !tax.is_active }">
                                            {{ tax.name }}
                                        </span>
                                    </TableCell>
                                    <TableCell>
                                        <span class="font-mono">{{ tax.rate }}%</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge v-if="tax.country_code" variant="outline" class="font-mono">
                                            {{ tax.country_code }}
                                        </Badge>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <span v-if="tax.region">{{ tax.region }}</span>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <div v-if="tax.description" class="max-w-[200px] truncate text-sm">
                                            {{ tax.description }}
                                        </div>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge 
                                            :variant="tax.is_active ? 'default' : 'secondary'" 
                                            :class="tax.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                                        >
                                            {{ tax.is_active ? 'Actif' : 'Inactif' }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger as-child>
                                                <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                    <MoreHorizontal class="h-4 w-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem @click="editTax(tax)">
                                                    <Pencil class="mr-2 h-4 w-4" />
                                                    Modifier
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    v-if="!tax.is_active" 
                                                    @click="toggleTaxStatus(tax, true)"
                                                >
                                                    <Eye class="mr-2 h-4 w-4" />
                                                    Activer
                                                </DropdownMenuItem>
                                                <DropdownMenuItem 
                                                    v-else 
                                                    @click="toggleTaxStatus(tax, false)"
                                                >
                                                    <EyeOff class="mr-2 h-4 w-4" />
                                                    Désactiver
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    @click="confirmDelete(tax)" 
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

        <TaxModal v-model:show="taxModal" :tax="selectedTax" @saved="onTaxSaved" @deleted="onTaxDeleted" />

        <AlertDialog v-model:open="deleteModal">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Confirmation de suppression</AlertDialogTitle>
                    <AlertDialogDescription>
                        Êtes-vous sûr de vouloir supprimer la taxe "{{ taxToDelete?.name }}" ? 
                        Cette action est irréversible.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Annuler</AlertDialogCancel>
                    <AlertDialogAction 
                        @click="deleteTax" 
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
import { Plus, Pencil, Trash2, Eye, EyeOff } from 'lucide-vue-next'
import TaxModal from '@/admin/components/modals/TaxModal.vue'
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
import { Switch } from '@/common/components/ui/switch'
import { Label } from '@/common/components/ui/label'
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
import { MoreHorizontal } from 'lucide-vue-next'

const fetcher = useFetcher()

const loadingTable = ref(false)
const taxes = ref([])
const total = ref(0)
const page = ref(1)
const itemsPerPage = ref(50)
const taxModal = ref(false)
const selectedTax = ref(null)
const deleteModal = ref(false)
const taxToDelete = ref(null)
const deleting = ref(false)
const showInactiveTaxes = ref(false)

const fetchTaxes = async () => {
    loadingTable.value = true

    try {
        const params = {
            limit: itemsPerPage.value,
            offset: (page.value - 1) * itemsPerPage.value,
        }

        const headers = {}
        if (!showInactiveTaxes.value) {
            headers['X-Filter'] = JSON.stringify([['is_active', 'is true']])
        }

        const { data } = await fetcher.get('/admin/service_taxes', { params, headers })
        taxes.value = data.items
        total.value = data.total
    } catch (error) {
        console.error('Erreur lors du chargement des taxes:', error)
        toast.error('Erreur lors du chargement des taxes')
    } finally {
        loadingTable.value = false
    }
}

const openTaxModal = () => {
    selectedTax.value = null
    taxModal.value = true
}

const editTax = (tax) => {
    selectedTax.value = tax
    taxModal.value = true
}

const confirmDelete = (tax) => {
    taxToDelete.value = tax
    deleteModal.value = true
}

const deleteTax = async () => {
    if (!taxToDelete.value) return

    deleting.value = true

    try {
        await fetcher.delete(`/admin/service_taxes/${taxToDelete.value.id}`)
        toast.success(`Taxe "${taxToDelete.value.name}" supprimée avec succès`)
        deleteModal.value = false
        fetchTaxes()
    } catch (error) {
        console.error('Erreur:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

const toggleTaxStatus = async (tax, isActive) => {
    try {
        await fetcher.patch(`/admin/service_taxes/${tax.id}`, { is_active: isActive })
        toast.success(`Taxe ${isActive ? 'activée' : 'désactivée'} avec succès`)
        fetchTaxes()
    } catch (error) {
        console.error('Erreur lors du changement de statut:', error)
        toast.error('Erreur lors du changement de statut')
    }
}

const onTaxSaved = () => {
    fetchTaxes()
    taxModal.value = false
}

const onTaxDeleted = () => {
    fetchTaxes()
    taxModal.value = false
}

const onToggleInactiveTaxes = () => {
    page.value = 1
    fetchTaxes()
}

const previousPage = () => {
    if (page.value > 1) {
        page.value--
        fetchTaxes()
    }
}

const nextPage = () => {
    if (page.value < Math.ceil(total.value / itemsPerPage.value)) {
        page.value++
        fetchTaxes()
    }
}

onMounted(() => {
    fetchTaxes()
})
</script> 
