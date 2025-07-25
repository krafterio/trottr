<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Packs de crédit</h1>
                    <p class="text-gray-600">Gestion des packs de crédit pour l'enrichissement de données</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <Switch 
                            v-model="showInactivePacks" 
                            @update:model-value="onToggleInactivePacks"
                        />
                        <Label class="text-sm">Afficher inactifs</Label>
                    </div>
                    <Button @click="openPackModal">
                        <Plus :size="16" class="mr-2" />
                        Ajouter un pack
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
                                    <TableHead>Prix</TableHead>
                                    <TableHead>Crédit disponible</TableHead>
                                    <TableHead>Description</TableHead>
                                    <TableHead>Statut</TableHead>
                                    <TableHead class="w-20"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-if="loadingTable">
                                    <TableCell colspan="6" class="text-center py-8">
                                        <div class="flex items-center justify-center space-x-2">
                                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                            <span>Chargement...</span>
                                        </div>
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else-if="packs.length === 0">
                                    <TableCell colspan="6" class="text-center py-8 text-gray-500">
                                        Aucun pack trouvé
                                    </TableCell>
                                </TableRow>
                                <TableRow 
                                    v-else 
                                    v-for="pack in packs" 
                                    :key="pack.id"
                                    :class="[
                                        'cursor-pointer hover:bg-gray-50 transition-colors',
                                        { 'opacity-60': !pack.is_active }
                                    ]"
                                    @click="onRowClick(pack)"
                                >
                                    <TableCell class="font-medium">
                                        <div class="flex items-center space-x-2">
                                            <Coins
                                                :size="16" 
                                                :class="pack.is_active ? 'text-blue-600' : 'text-gray-400'"
                                            />
                                            <span :class="{ 'text-gray-500': !pack.is_active }">
                                                {{ pack.name }}
                                            </span>
                                        </div>
                                    </TableCell>
                                    <TableCell class="font-mono text-sm">
                                        {{ formatPrice(pack.price, pack.currency) }}
                                    </TableCell>
                                    <TableCell class="font-mono text-sm">
                                        {{ formatCredit(pack.available_credit) }}
                                    </TableCell>
                                    <TableCell>
                                        <div v-if="pack.description" class="max-w-xs truncate text-sm">
                                            {{ pack.description }}
                                        </div>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge :variant="pack.is_active ? 'default' : 'secondary'">
                                            {{ pack.is_active ? 'Actif' : 'Inactif' }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger asChild>
                                                <Button 
                                                    variant="ghost" 
                                                    size="sm"
                                                    @click.stop
                                                >
                                                    <EllipsisVertical :size="16" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem 
                                                    v-if="!pack.is_active" 
                                                    @click="activatePack(pack)"
                                                >
                                                    <Eye :size="16" class="mr-2" />
                                                    Activer
                                                </DropdownMenuItem>
                                                <DropdownMenuItem 
                                                    v-else 
                                                    @click="deactivatePack(pack)"
                                                >
                                                    <EyeOff :size="16" class="mr-2" />
                                                    Désactiver
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    @click="deletePack(pack)" 
                                                    class="text-red-600 focus:text-red-600"
                                                >
                                                    <Trash :size="16" class="mr-2" />
                                                    Supprimer
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>

                    <div v-if="packs.length > 0" class="flex items-center justify-between mt-4">
                        <p class="text-sm text-gray-600">
                            {{ packs.length }} pack(s) sur {{ total }}
                        </p>
                        
                        <div class="flex items-center space-x-2">
                            <Button 
                                variant="outline" 
                                size="sm"
                                :disabled="page <= 1"
                                @click="onPageChange(page - 1)"
                            >
                                Précédent
                            </Button>
                            
                            <div class="flex items-center space-x-1">
                                <Button
                                    v-for="pageNum in visiblePages"
                                    :key="pageNum"
                                    :variant="pageNum === page ? 'default' : 'outline'"
                                    size="sm"
                                    class="w-8 h-8"
                                    @click="onPageChange(pageNum)"
                                >
                                    {{ pageNum }}
                                </Button>
                            </div>
                            
                            <Button 
                                variant="outline" 
                                size="sm"
                                :disabled="page >= totalPages"
                                @click="onPageChange(page + 1)"
                            >
                                Suivant
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <CreditPackModal v-model:show="packModal" :pack="selectedPack" @saved="onPackSaved" @deleted="onPackDeleted"/>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

import CreditPackModal from '@/admin/components/modals/CreditPackModal.vue'
import { useFetcher } from "@/common/composables/fetcher"
import { toast } from 'vue-sonner'
import { bus } from '@/common/composables/bus'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/common/components/ui/table'
import {
    Card,
    CardContent,
} from '@/common/components/ui/card'
import { Button } from '@/common/components/ui/button'
import { Badge } from '@/common/components/ui/badge'
import { Label } from '@/common/components/ui/label'
import { Switch } from '@/common/components/ui/switch'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import {
    Coins,
    Eye,
    EyeOff,
    Trash,
    Plus,
    EllipsisVertical,
} from 'lucide-vue-next'

const fetcher = useFetcher()

const loadingTable = ref(false)
const packs = ref([])
const total = ref(0)
const page = ref(1)
const itemsPerPage = ref(50)
const packModal = ref(false)
const selectedPack = ref(null)
const showInactivePacks = ref(false)

const totalPages = computed(() => Math.ceil(total.value / itemsPerPage.value))

const visiblePages = computed(() => {
    const start = Math.max(1, page.value - 2)
    const end = Math.min(totalPages.value, page.value + 2)
    const pages = []
    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    return pages
})

const formatPrice = (price, currency) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency || 'EUR',
    }).format(price)
}

const formatCredit = (credit) => {
    return new Intl.NumberFormat('fr-FR', {
        maximumFractionDigits: 2,
    }).format(credit)
}

const fetchPacks = async () => {
    loadingTable.value = true

    try {
        const params = {
            limit: itemsPerPage.value,
            offset: (page.value - 1) * itemsPerPage.value,
        }

        const headers = {}

        if (!showInactivePacks.value) {
            headers['X-Filter'] = JSON.stringify([['is_active', 'is true']])
        }

        const { data } = await fetcher.get('/admin/service_credit_packs', { params, headers })
        packs.value = data.items
        total.value = data.total
    } catch (error) {
        console.error('Erreur lors du chargement des packs:', error)
        toast.error('Erreur lors du chargement des packs')
    } finally {
        loadingTable.value = false
    }
}

const onPageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages.value) {
        page.value = newPage
        fetchPacks()
    }
}

const onRowClick = (pack) => {
    selectedPack.value = pack
    packModal.value = true
}

const openPackModal = () => {
    selectedPack.value = null
    packModal.value = true
}

const onPackSaved = () => {
    fetchPacks()
    packModal.value = false
}

const onPackDeleted = () => {
    fetchPacks()
    packModal.value = false
}

const onToggleInactivePacks = () => {
    page.value = 1
    fetchPacks()
}

const activatePack = async (pack) => {
    try {
        await fetcher.patch(`/admin/service_credit_packs/${pack.id}`, { is_active: true })
        toast.success('Pack activé avec succès')
        await fetchPacks()
    } catch (error) {
        console.error('Erreur lors de l\'activation:', error)
        toast.error('Erreur lors de l\'activation')
    }
}

const deactivatePack = async (pack) => {
    try {
        await fetcher.patch(`/admin/service_credit_packs/${pack.id}`, { is_active: false })
        toast.success('Pack désactivé avec succès')
        await fetchPacks()
    } catch (error) {
        console.error('Erreur lors de la désactivation:', error)
        toast.error('Erreur lors de la désactivation')
    }
}

const deletePack = (pack) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le pack de crédit',
        message: 'Êtes-vous sûr de vouloir supprimer ce pack de crédit ?',
        itemName: pack.name || '',
        onConfirm: () => confirmDeletePack(pack)
    })
}

const confirmDeletePack = async (pack) => {
    try {
        await fetcher.delete(`/admin/service_credit_packs/${pack.id}`)
        toast.success('Pack supprimé avec succès')
        await fetchPacks()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    }
}

onMounted(() => {
    fetchPacks()
})
</script>
