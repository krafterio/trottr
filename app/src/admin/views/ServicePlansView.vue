<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Plans d'espaces de travail</h1>
                    <p class="text-gray-600">Gestion des plans d'abonnement et des tarifs</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <Switch 
                            v-model="showInactivePlans" 
                            @update:model-value="onToggleInactivePlans"
                        />
                        <Label class="text-sm">Afficher inactifs</Label>
                    </div>
                    <Button @click="openPlanModal">
                        <Plus :size="16" class="mr-2" />
                        Ajouter un plan
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
                                    <TableHead>Type</TableHead>
                                    <TableHead>Période</TableHead>
                                    <TableHead>Prix</TableHead>
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
                                <TableRow v-else-if="plans.length === 0">
                                    <TableCell colspan="7" class="text-center py-8 text-gray-500">
                                        Aucun plan trouvé
                                    </TableCell>
                                </TableRow>
                                <TableRow 
                                    v-else 
                                    v-for="plan in plans" 
                                    :key="plan.id"
                                    :class="[
                                        'cursor-pointer hover:bg-gray-50 transition-colors',
                                        { 'opacity-60': !plan.is_active }
                                    ]"
                                    @click="onRowClick(plan)"
                                    @contextmenu="onRightClick($event, plan)"
                                >
                                    <TableCell class="font-medium">
                                        <div class="flex items-center space-x-2">
                                            <Crown
                                                :size="16" 
                                                :class="plan.is_active ? 'text-blue-600' : 'text-gray-400'"
                                            />
                                            <span :class="{ 'text-gray-500': !plan.is_active }">
                                                {{ plan.name }}
                                            </span>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <Badge :variant="getTypeVariant(plan.type)">
                                            {{ plan.type }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell>
                                        <Badge :variant="getPeriodVariant(plan.period)">
                                            {{ plan.period }}
                                        </Badge>
                                    </TableCell>
                                    <TableCell class="font-mono text-sm">
                                        {{ formatPrice(plan.price, plan.currency) }}
                                    </TableCell>
                                    <TableCell>
                                        <div v-if="plan.description" class="max-w-xs truncate text-sm">
                                            {{ plan.description }}
                                        </div>
                                        <span v-else class="text-gray-400">-</span>
                                    </TableCell>
                                    <TableCell>
                                        <Badge :variant="plan.is_active ? 'default' : 'secondary'">
                                            {{ plan.is_active ? 'Actif' : 'Inactif' }}
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
                                                    v-if="!plan.is_active" 
                                                    @click="activatePlan(plan)"
                                                >
                                                    <Eye :size="16" class="mr-2" />
                                                    Activer
                                                </DropdownMenuItem>
                                                <DropdownMenuItem 
                                                    v-else 
                                                    @click="deactivatePlan(plan)"
                                                >
                                                    <EyeOff :size="16" class="mr-2" />
                                                    Désactiver
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    @click="deletePlan(plan)" 
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

                    <div v-if="plans.length > 0" class="flex items-center justify-between mt-4">
                        <p class="text-sm text-gray-600">
                            {{ plans.length }} plan(s) sur {{ total }}
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

        <PlanModal v-model:show="planModal" :plan="selectedPlan" @saved="onPlanSaved" @deleted="onPlanDeleted"/>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

import PlanModal from '@/admin/components/modals/PlanModal.vue'
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
    Crown,
    EllipsisVertical,
    Eye,
    EyeOff,
    Plus,
    Trash,
} from 'lucide-vue-next'

const fetcher = useFetcher()

const loadingTable = ref(false)
const plans = ref([])
const total = ref(0)
const page = ref(1)
const itemsPerPage = ref(50)
const planModal = ref(false)
const selectedPlan = ref(null)
const showInactivePlans = ref(false)

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

const getTypeVariant = (type) => {
    const variants = {
        Pro: 'default',
        Team: 'secondary',
        Enterprise: 'outline',
    }
    return variants[type] || 'secondary'
}

const getPeriodVariant = (period) => {
    const variants = {
        Mensuel: 'default',
        Annuel: 'secondary',
    }
    return variants[period] || 'secondary'
}

const formatPrice = (price, currency) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency || 'EUR',
    }).format(price)
}

const fetchPlans = async () => {
    loadingTable.value = true

    try {
        const params = {
            limit: itemsPerPage.value,
            offset: (page.value - 1) * itemsPerPage.value,
        }

        const headers = {}

        if (!showInactivePlans.value) {
            headers['X-Filter'] = JSON.stringify([['is_active', 'is true']])
        }

        const { data } = await fetcher.get('/admin/service_plans', { params, headers })
        plans.value = data.items
        total.value = data.total
    } catch (error) {
        console.error('Erreur lors du chargement des plans:', error)
        toast.error('Erreur lors du chargement des plans')
    } finally {
        loadingTable.value = false
    }
}

const onPageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages.value) {
        page.value = newPage
        fetchPlans()
    }
}

const onRowClick = (plan) => {
    selectedPlan.value = plan
    planModal.value = true
}

const openPlanModal = () => {
    selectedPlan.value = null
    planModal.value = true
}

const onPlanSaved = () => {
    fetchPlans()
    planModal.value = false
}

const onPlanDeleted = () => {
    fetchPlans()
    planModal.value = false
}

const onToggleInactivePlans = () => {
    page.value = 1
    fetchPlans()
}

const activatePlan = async (plan) => {
    try {
        await fetcher.patch(`/admin/service_plans/${plan.id}`, { is_active: true })
        toast.success('Plan activé avec succès')
        await fetchPlans()
    } catch (error) {
        console.error('Erreur lors de l\'activation:', error)
        toast.error('Erreur lors de l\'activation')
    }
}

const deactivatePlan = async (plan) => {
    try {
        await fetcher.patch(`/admin/service_plans/${plan.id}`, { is_active: false })
        toast.success('Plan désactivé avec succès')
        await fetchPlans()
    } catch (error) {
        console.error('Erreur lors de la désactivation:', error)
        toast.error('Erreur lors de la désactivation')
    }
}

const deletePlan = (plan) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le plan',
        message: 'Êtes-vous sûr de vouloir supprimer ce plan ?',
        itemName: plan.name || '',
        onConfirm: () => confirmDeletePlan(plan)
    })
}

const confirmDeletePlan = async (plan) => {
    try {
        await fetcher.delete(`/admin/service_plans/${plan.id}`)
        toast.success('Plan supprimé avec succès')
        await fetchPlans()
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    }
}

onMounted(() => {
    fetchPlans()
})
</script> 
