<template>
    <div class="max-w-5xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Facturation</h2>
            <p class="text-neutral-600">Gérez votre abonnement et vos informations de facturation.</p>
        </div>

        <div v-if="loading" class="text-center py-8">
            <p class="text-neutral-600">Chargement...</p>
        </div>

        <div v-else-if="error" class="text-center py-8">
            <p class="text-red-600">Erreur lors du chargement des données de facturation</p>
        </div>

        <div v-else-if="billingInfo" class="space-y-6">
            <!-- Plan actuel -->
            <div class="border rounded-lg p-6 bg-accent">
                <div class=" flex items-center justify-between mb-4">
                    <div>
                        <h3 class="text-lg font-semibold text-neutral-900">
                            {{ billingInfo.plan_name || 'Aucun plan' }}
                        </h3>
                        <p class="text-neutral-600">
                            {{ billingInfo.subscription_available_users_count ? 
                                `Jusqu'à ${billingInfo.subscription_available_users_count} utilisateurs` : 
                                'Aucun plan actif'
                            }}
                        </p>
                    </div>
                    <Badge class="bg-primary text-primary-foreground">
                        {{ getStatusLabel(billingInfo.subscription_status) }}
                    </Badge>
                </div>

                <div class="flex items-baseline space-x-2 mb-4">
                    <span class="text-3xl font-bold text-neutral-900">
                        {{ billingInfo.subscription_price ?
                            formatPrice(billingInfo.subscription_price, billingInfo.plan_currency) :
                            'Gratuit' 
                        }}
                    </span>
                    <span v-if="billingInfo.plan_period" class="text-neutral-600">
                        / {{ formatPeriod(billingInfo.plan_period.toLowerCase()) }}
                    </span>
                </div>

                <div class="flex items-center justify-between">
                    <span class="text-sm text-neutral-600">
                        {{ getNextBillingText() }}
                    </span>
                    <Button
                        variant="outline"
                        size="sm"
                        @click="openStripePortal"
                    >
                        Changer de plan
                    </Button>
                </div>
            </div>

            <!-- Utilisation -->
            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Utilisation actuelle</h3>

                <!-- Alerte dépassement limite utilisateurs -->
                <Alert v-if="workspaceStore.isOverMemberLimit" variant="destructive" class="border-red-200 bg-red-50">
                    <Users class="h-4 w-4" />
                    <AlertDescription class="space-y-3">
                        <div>
                            <strong>Attention :</strong> Vous avez {{ workspaceStore.memberCount }} utilisateurs actifs 
                            mais votre plan n'autorise que {{ workspaceStore.availableMemberCount }} utilisateurs. 
                            Mettez à niveau votre plan ou supprimez des utilisateurs pour éviter toute interruption de service.
                        </div>
                        <div class="flex gap-2 pt-2">
                            <Button variant="outline" size="sm" class="bg-white hover:bg-neutral-50" @click="openStripePortal">
                                Changer de plan
                            </Button>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                class="bg-white hover:bg-neutral-50"
                                @click="navigateToUsers"
                            >
                                Gérer les utilisateurs
                            </Button>
                        </div>
                    </AlertDescription>
                </Alert>

                <div class="grid grid-cols-2 gap-4">
                    <div class="border rounded-lg p-4">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-neutral-600">Utilisateurs</span>
                            <Users class="h-4 w-4 text-neutral-500" />
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-sm font-semibold text-neutral-900" 
                                  :class="{ 'text-red-600': workspaceStore.isOverMemberLimit }">
                                {{ workspaceStore.memberCount }}
                            </span>
                            <span class="text-sm text-neutral-500">
                                / {{ workspaceStore.availableMemberCount || 'illimité' }}
                            </span>
                        </div>
                        <div class="w-full bg-neutral-200 rounded-full h-2 mt-2">
                            <div 
                                class="h-2 rounded-full transition-colors" 
                                :class="workspaceStore.isOverMemberLimit ? 'bg-red-500' : 'bg-primary'"
                                :style="`width: ${getUsersPercentage()}%`"
                            ></div>
                        </div>
                    </div>

                    <div class="border rounded-lg p-4">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-neutral-600">Interventions ce mois</span>
                            <Calendar class="h-4 w-4 text-neutral-500" />
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-sm font-semibold text-neutral-900">{{ billingInfo.current_month_jobs_count }}</span>
                            <span class="text-sm text-neutral-500">/ illimité</span>
                        </div>
                        <div class="w-full bg-neutral-200 rounded-full h-2 mt-2">
                            <div 
                                class="bg-primary h-2 rounded-full" 
                                :style="`width: ${getJobsPercentage()}%`"
                            ></div>
                        </div>
                    </div>
                </div>
            </div>

            <Separator />

            <!-- Méthodes de paiement -->
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-base font-medium text-neutral-900">Méthodes de paiement</h3>
                    <Button 
                        variant="outline" 
                        size="sm"
                        @click="openStripePortal"
                    >
                        <Plus class="h-4 w-4 mr-2" />
                        Ajouter une carte
                    </Button>
                </div>

                <div class="border rounded-lg p-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-3">
                            <div
                                class="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded flex items-center justify-center">
                                <CreditCard class="h-4 w-4 text-white" />
                            </div>
                            <div>
                                <p class="text-sm font-medium text-neutral-900">•••• •••• •••• 4242</p>
                                <p class="text-xs text-neutral-500">Expire 12/26</p>
                            </div>
                        </div>
                        <div class="flex items-center space-x-2">
                            <Badge class="bg-green-100 text-green-800">Par défaut</Badge>
                            <Button 
                                variant="ghost" 
                                size="sm"
                                @click="openStripePortal"
                            >
                                <Edit class="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            <Separator />

            <!-- Historique de facturation -->
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-base font-medium text-neutral-900">Historique de facturation</h3>
                </div>

                <div class="border rounded-lg">
                    <div class="p-4 border-b bg-neutral-50">
                        <div class="grid grid-cols-12 gap-4 text-sm font-medium text-neutral-700">
                            <div class="col-span-3">Date</div>
                            <div class="col-span-3">Montant</div>
                            <div class="col-span-3">Statut</div>
                            <div class="col-span-3">Facture</div>
                        </div>
                    </div>

                    <div class="divide-y">
                        <div v-if="invoices.length === 0" class="p-4 text-center text-neutral-500">
                            Aucune facture disponible
                        </div>
                        <div v-for="invoice in invoices" :key="invoice.id" class="p-4">
                            <div class="grid grid-cols-12 gap-4 items-center">
                                <div class="col-span-3">
                                    <p class="text-sm text-neutral-900">{{ formatInvoiceDate(invoice.created) }}</p>
                                    <p v-if="invoice.number" class="text-xs text-neutral-500">{{ invoice.number }}</p>
                                </div>
                                <div class="col-span-3">
                                    <p class="text-sm font-medium text-neutral-900">
                                        {{ formatInvoiceAmount(invoice.amount_paid, invoice.currency) }}
                                    </p>
                                </div>
                                <div class="col-span-3">
                                    <Badge :class="getInvoiceStatusClass(invoice.status)">
                                        {{ getInvoiceStatusText(invoice.status) }}
                                    </Badge>
                                </div>
                                <div class="col-span-3">
                                    <Button 
                                        variant="ghost" 
                                        size="sm"
                                        @click="downloadInvoice(invoice)"
                                        :disabled="!invoice.invoice_pdf && !invoice.hosted_invoice_url"
                                    >
                                        <Download class="h-4 w-4 mr-2" />
                                        PDF
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <Separator />

            <!-- Informations de facturation -->
            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Informations de facturation</h3>

                <div class="border rounded-lg p-4">
                    <div class="space-y-3">
                        <div>
                            <Label class="text-sm font-medium text-neutral-700">Nom de facturation</Label>
                            <p class="text-sm text-neutral-900">{{ billingInfo.invoice_name || 'Non renseigné' }}</p>
                        </div>
                        <div>
                            <Label class="text-sm font-medium text-neutral-700">Adresse de facturation</Label>
                            <p class="text-sm text-neutral-900" v-html="getInvoiceAddress()"></p>
                        </div>
                        <div>
                            <Label class="text-sm font-medium text-neutral-700">SIREN</Label>
                            <p class="text-sm text-neutral-900">{{ billingInfo.invoice_siren || 'Non renseigné' }}</p>
                        </div>
                        <div>
                            <Label class="text-sm font-medium text-neutral-700">Numéro TVA</Label>
                            <p class="text-sm text-neutral-900">{{ billingInfo.invoice_vat || 'Non renseigné' }}</p>
                        </div>
                    </div>
                    <div class="mt-4">
                        <Button 
                            variant="outline" 
                            size="sm"
                            @click="openBillingDialog"
                        >
                            <Edit class="h-4 w-4 mr-2" />
                            Modifier
                        </Button>
                    </div>
                </div>
            </div>
        </div>
        
        <BillingInfoDialog 
            v-model:open="showBillingDialog"
        />
    </div>
</template>

<script setup>
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import { Label } from '@/common/components/ui/label'
import { Separator } from '@/common/components/ui/separator'
import { Calendar, CreditCard, Download, Edit, Plus, Users } from 'lucide-vue-next'
import { ref, onMounted } from 'vue'
import { useFetcher } from '@/common/composables/fetcher'
import BillingInfoDialog from '@/main/components/dialogs/BillingInfoDialog.vue'
import { useWorkspaceStore } from '@/main/stores/workspace'
import { Alert, AlertDescription } from '@/common/components/ui/alert'
import { useRouter } from 'vue-router'

const fetcher = useFetcher()
const workspaceStore = useWorkspaceStore()
const router = useRouter()

const billingInfo = ref(null)
const loading = ref(false)
const error = ref(null)
const showBillingDialog = ref(false)
const invoices = ref([])

const fetchBillingInfo = async () => {
    try {
        loading.value = true
        error.value = null
        
        const response = await fetcher.get('/workspace/billing')
        billingInfo.value = response.data
    } catch (err) {
        error.value = err
    } finally {
        loading.value = false
    }
}

const fetchInvoices = async () => {
    try {
        const response = await fetcher.get('/workspace/subscription/invoices')
        invoices.value = response.data.invoices || []
    } catch (err) {
        console.error('Erreur lors du chargement des factures:', err)
        invoices.value = []
    }
}

const openStripePortal = async () => {
    try {
        const currentUrl = window.location.origin + window.location.pathname
        
        const response = await fetcher.post('/workspace/subscription/billing-portal', {
            return_url: currentUrl
        })
        
        if (response.data?.url) {
            window.location.href = response.data.url
        }
    } catch (err) {
        console.error('Erreur lors de l\'ouverture du portail Stripe:', err)
    }
}

const formatPrice = (amount, currency = 'EUR') => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency
    }).format(amount)
}

const formatDate = (date) => {
    if (!date) return null
    return new Intl.DateTimeFormat('fr-FR', {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
    }).format(new Date(date))
}

const formatInvoiceDate = (timestamp) => {
    return new Intl.DateTimeFormat('fr-FR', {
        day: 'numeric',
        month: 'short',
        year: 'numeric'
    }).format(new Date(timestamp * 1000))
}

const formatInvoiceAmount = (amount, currency) => {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: currency
    }).format(amount)
}

const getInvoiceStatusText = (status) => {
    switch (status) {
        case 'paid': return 'Payée'
        case 'open': return 'En attente'
        case 'void': return 'Annulée'
        case 'draft': return 'Brouillon'
        case 'uncollectible': return 'Impayée'
        default: return status
    }
}

const downloadInvoice = (invoice) => {
    if (invoice.invoice_pdf) {
        window.open(invoice.invoice_pdf, '_blank')
    } else if (invoice.hosted_invoice_url) {
        window.open(invoice.hosted_invoice_url, '_blank')
    }
}

const formatPeriod = (period) => {
    if (period === 'mensuel') return 'mois'

    return 'an'
}

const openBillingDialog = () => {
    showBillingDialog.value = true
}

const navigateToUsers = () => {
    router.push({ name: 'settings-users' })
}

const getUsagePercentage = (current, max) => {
    if (!max || max === 0) return 0
    return Math.min((current / max) * 100, 100)
}

onMounted(() => {
    fetchBillingInfo()
    workspaceStore.fetchWorkspace()
    fetchInvoices()
})

const getInvoiceStatusClass = (status) => {
    switch (status) {
        case 'paid': return 'bg-green-100 text-green-800'
        case 'open': return 'bg-yellow-100 text-yellow-800'
        case 'void': 
        case 'uncollectible': return 'bg-red-100 text-red-800'
        case 'draft': return 'bg-gray-100 text-gray-800'
        default: return 'bg-neutral-100 text-neutral-800'
    }
}

const getStatusLabel = (status) => {
    switch (status) {
        case 'active': return 'Actif'
        case 'trialing': return 'Essai'
        case 'canceled': return 'Annulé'
        case 'past_due': return 'En retard'
        case 'unpaid': return 'Impayé'
        default: return 'Inconnu'
    }
}

const getNextBillingText = () => {
    if (!billingInfo.value?.subscription_status) return 'Aucun abonnement'
    
    if (billingInfo.value.subscription_trial_end && new Date(billingInfo.value.subscription_trial_end) > new Date()) {
        return `Essai gratuit jusqu'au ${formatDate(billingInfo.value.subscription_trial_end)}`
    }
    
    if (billingInfo.value.subscription_next_billing_date) {
        return `Prochaine facturation le ${formatDate(billingInfo.value.subscription_next_billing_date)}`
    }
    
    if (billingInfo.value.subscription_cancel_at_period_end) {
        return 'Abonnement annulé en fin de période'
    }
    
    return 'Informations de facturation non disponibles'
}

const getUsersPercentage = () => {
    if (!workspaceStore.availableMemberCount) return 0
    return getUsagePercentage(
        workspaceStore.memberCount, 
        workspaceStore.availableMemberCount
    )
}

const getJobsPercentage = () => {
    if (!billingInfo.value?.current_month_jobs_count) return 0
    const maxJobs = 10000
    return getUsagePercentage(
        billingInfo.value.current_month_jobs_count,
        maxJobs
    )
}

const getInvoiceAddress = () => {
    if (!billingInfo.value) return 'Non renseigné'
    
    const parts = []
    if (billingInfo.value.invoice_street) parts.push(billingInfo.value.invoice_street)
    if (billingInfo.value.invoice_street2) parts.push(billingInfo.value.invoice_street2)
    
    const cityLine = []
    if (billingInfo.value.invoice_zip) cityLine.push(billingInfo.value.invoice_zip)
    if (billingInfo.value.invoice_city) cityLine.push(billingInfo.value.invoice_city)
    if (cityLine.length > 0) parts.push(cityLine.join(' '))
    
    if (billingInfo.value.invoice_country?.name) {
        parts.push(billingInfo.value.invoice_country.name)
    }
    
    return parts.length > 0 ? parts.join('<br />') : 'Non renseigné'
}
</script>
