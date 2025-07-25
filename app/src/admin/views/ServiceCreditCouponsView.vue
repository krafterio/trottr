<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Coupons de crédit</h1>
                    <p class="text-gray-600">Gestion des coupons de crédit et codes promotionnels</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <Switch 
                            v-model="showInactiveCoupons" 
                            @update:model-value="onToggleInactiveCoupons"
                        />
                        <Label class="text-sm">Afficher inactifs</Label>
                    </div>
                    <Button @click="openCouponModal">
                        <Plus :size="16" class="mr-2" />
                        Ajouter un coupon
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
                                    <TableHead>Code</TableHead>
                                    <TableHead>Crédit disponible</TableHead>
                                    <TableHead>Date d'expiration</TableHead>
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
                                <TableRow v-else-if="coupons.length === 0">
                                    <TableCell colspan="7" class="text-center py-8 text-gray-500">
                                        Aucun coupon trouvé
                                    </TableCell>
                                </TableRow>
                                <TableRow 
                                    v-else 
                                    v-for="coupon in coupons" 
                                    :key="coupon.id"
                                    :class="[
                                        'cursor-pointer hover:bg-gray-50 transition-colors',
                                        { 'opacity-60': !coupon.is_active }
                                    ]"
                                    @click="onRowClick(coupon)"
                                >
                                    <TableCell class="font-medium">
                                        <div class="flex items-center space-x-2">
                                            <Ticket 
                                                :size="16" 
                                                :class="coupon.is_active ? 'text-blue-600' : 'text-gray-400'"
                                            />
                                            <span :class="{ 'text-gray-500': !coupon.is_active }">
                                                {{ coupon.name }}
                                            </span>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge variant="outline" class="font-mono">
                                            {{ coupon.code }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell class="font-mono text-sm">
                                        {{ formatCredit(coupon.available_credit) }}
                                    </TableCell>
                                    <TableCell class="text-sm">
                                        {{ formatDate(coupon.expiration_date) }}
                                    </TableCell>
                                    <TableCell>
                                        <div v-if="coupon.description" class="max-w-xs truncate text-sm">
                                            {{ coupon.description }}
                                        </div>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge :variant="coupon.is_active ? 'default' : 'secondary'">
                                            {{ coupon.is_active ? 'Actif' : 'Inactif' }}
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
                                                    <MoreHorizontal :size="16" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem 
                                                    v-if="!coupon.is_active" 
                                                    @click="activateCoupon(coupon)"
                                                >
                                                    <Eye :size="16" class="mr-2" />
                                                    Activer
                                                </DropdownMenuItem>
                                                <DropdownMenuItem 
                                                    v-else 
                                                    @click="deactivateCoupon(coupon)"
                                                >
                                                    <EyeOff :size="16" class="mr-2" />
                                                    Désactiver
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    @click="deleteCoupon(coupon)" 
                                                    class="text-red-600 focus:text-red-600"
                                                >
                                                    <Trash2 :size="16" class="mr-2" />
                                                    Supprimer
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>

                    <div v-if="coupons.length > 0" class="flex items-center justify-between mt-4">
                        <p class="text-sm text-gray-600">
                            {{ coupons.length }} coupon(s) sur {{ total }}
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

        <CouponModal v-model:show="couponModal" :coupon="selectedCoupon" @saved="onCouponSaved" @deleted="onCouponDeleted"/>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Plus, Ticket, MoreHorizontal, Trash2, Eye, EyeOff } from 'lucide-vue-next'
import CouponModal from '@/admin/components/modals/CouponModal.vue'
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

const fetcher = useFetcher()

const loadingTable = ref(false)
const coupons = ref([])
const total = ref(0)
const page = ref(1)
const itemsPerPage = ref(50)
const couponModal = ref(false)
const selectedCoupon = ref(null)
const showInactiveCoupons = ref(false)

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

const formatCredit = (credit) => {
    return new Intl.NumberFormat('fr-FR', {
        maximumFractionDigits: 2,
    }).format(credit)
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('fr-FR').format(date)
}

const fetchCoupons = async () => {
    loadingTable.value = true

    try {
        const params = {
            limit: itemsPerPage.value,
            offset: (page.value - 1) * itemsPerPage.value,
        }

        const headers = {}

        if (!showInactiveCoupons.value) {
            headers['X-Filter'] = JSON.stringify([['is_active', 'is true']])
        }

        const { data } = await fetcher.get('/admin/service_credit_coupons', { params, headers })
        coupons.value = data.items
        total.value = data.total
    } catch (error) {
        console.error('Erreur lors du chargement des coupons:', error)
        toast.error('Erreur lors du chargement des coupons')
    } finally {
        loadingTable.value = false
    }
}

const onPageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages.value) {
        page.value = newPage
        fetchCoupons()
    }
}

const onRowClick = (coupon) => {
    selectedCoupon.value = coupon
    couponModal.value = true
}

const openCouponModal = () => {
    selectedCoupon.value = null
    couponModal.value = true
}

const onCouponSaved = () => {
    fetchCoupons()
    couponModal.value = false
}

const onCouponDeleted = () => {
    fetchCoupons()
    couponModal.value = false
}

const onToggleInactiveCoupons = () => {
    page.value = 1
    fetchCoupons()
}

const activateCoupon = async (coupon) => {
    try {
        await fetcher.patch(`/admin/service_credit_coupons/${coupon.id}`, { is_active: true })
        toast.success('Coupon activé avec succès')
        await fetchCoupons()
    } catch (error) {
        console.error('Erreur lors de l\'activation:', error)
        toast.error('Erreur lors de l\'activation')
    }
}

const deactivateCoupon = async (coupon) => {
    try {
        await fetcher.patch(`/admin/service_credit_coupons/${coupon.id}`, { is_active: false })
        toast.success('Coupon désactivé avec succès')
        await fetchCoupons()
    } catch (error) {
        console.error('Erreur lors de la désactivation:', error)
        toast.error('Erreur lors de la désactivation')
    }
}

const deleteCoupon = (coupon) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le coupon',
        message: 'Êtes-vous sûr de vouloir supprimer ce coupon ?',
        itemName: coupon.name || '',
        onConfirm: () => confirmDeleteCoupon(coupon)
    })
}

const confirmDeleteCoupon = async (coupon) => {
    try {
        await fetcher.delete(`/admin/service_credit_coupons/${coupon.id}`)
        toast.success('Coupon supprimé avec succès')
        await fetchCoupons()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    }
}

onMounted(() => {
    fetchCoupons()
})
</script>
