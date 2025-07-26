<template>
    <div class="max-w-5xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Facturation</h2>
            <p class="text-neutral-600">Gérez votre abonnement et vos informations de facturation.</p>
        </div>

        <div class="space-y-6">
            <!-- Plan actuel -->
            <div class="border rounded-lg p-6 bg-accent">
                <div class=" flex items-center justify-between mb-4">
                    <div>
                        <h3 class="text-lg font-semibold text-neutral-900">Plan Professionnel</h3>
                        <p class="text-neutral-600">Jusqu'à 10 utilisateurs</p>
                    </div>
                    <Badge class="bg-primary text-primary-foreground">Actuel</Badge>
                </div>

                <div class="flex items-baseline space-x-2 mb-4">
                    <span class="text-3xl font-bold text-neutral-900">49€</span>
                    <span class="text-neutral-600">/mois</span>
                </div>

                <div class="flex items-center justify-between">
                    <span class="text-sm text-neutral-600">Prochaine facturation le 15 janvier 2025</span>
                    <Button variant="outline" size="sm">
                        Changer de plan
                    </Button>
                </div>
            </div>

            <!-- Utilisation -->
            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Utilisation actuelle</h3>

                <div class="grid grid-cols-2 gap-4">
                    <div class="border rounded-lg p-4">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-neutral-600">Utilisateurs</span>
                            <Users class="h-4 w-4 text-neutral-500" />
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-sm font-semibold text-neutral-900">4</span>
                            <span class="text-sm text-neutral-500">/ 10</span>
                        </div>
                        <div class="w-full bg-neutral-200 rounded-full h-2 mt-2">
                            <div class="bg-primary h-2 rounded-full" style="width: 40%"></div>
                        </div>
                    </div>

                    <div class="border rounded-lg p-4">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-neutral-600">Interventions ce mois</span>
                            <Calendar class="h-4 w-4 text-neutral-500" />
                        </div>
                        <div class="flex items-baseline space-x-2">
                            <span class="text-sm font-semibold text-neutral-900">127</span>
                            <span class="text-sm text-neutral-500">/ illimité</span>
                        </div>
                        <div class="w-full bg-neutral-200 rounded-full h-2 mt-2">
                            <div class="bg-primary h-2 rounded-full" style="width: 25%"></div>
                        </div>
                    </div>
                </div>
            </div>

            <Separator />

            <!-- Méthodes de paiement -->
            <div class="space-y-4">
                <div class="flex items-center justify-between">
                    <h3 class="text-base font-medium text-neutral-900">Méthodes de paiement</h3>
                    <Button variant="outline" size="sm">
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
                            <Button variant="ghost" size="sm">
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
                    <Button variant="outline" size="sm">
                        <Download class="h-4 w-4 mr-2" />
                        Télécharger toutes
                    </Button>
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
                        <div v-for="invoice in invoices" :key="invoice.id" class="p-4">
                            <div class="grid grid-cols-12 gap-4 items-center">
                                <div class="col-span-3">
                                    <p class="text-sm text-neutral-900">{{ invoice.date }}</p>
                                </div>
                                <div class="col-span-3">
                                    <p class="text-sm font-medium text-neutral-900">{{ invoice.amount }}</p>
                                </div>
                                <div class="col-span-3">
                                    <Badge :class="getInvoiceStatusClass(invoice.status)">
                                        {{ invoice.status }}
                                    </Badge>
                                </div>
                                <div class="col-span-3">
                                    <Button variant="ghost" size="sm">
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
                            <p class="text-sm text-neutral-900">SARL Tech Solutions</p>
                        </div>
                        <div>
                            <Label class="text-sm font-medium text-neutral-700">Adresse de facturation</Label>
                            <p class="text-sm text-neutral-900">123 rue de la République<br />75001 Paris, France</p>
                        </div>
                        <div>
                            <Label class="text-sm font-medium text-neutral-700">Email de facturation</Label>
                            <p class="text-sm text-neutral-900">billing@techsolutions.com</p>
                        </div>
                    </div>
                    <div class="mt-4">
                        <Button variant="outline" size="sm">
                            <Edit class="h-4 w-4 mr-2" />
                            Modifier
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import { Label } from '@/common/components/ui/label'
import { Separator } from '@/common/components/ui/separator'
import { Calendar, CreditCard, Download, Edit, Plus, Users } from 'lucide-vue-next'
import { ref } from 'vue'

const invoices = ref([
    {
        id: 1,
        date: '15 Déc 2024',
        amount: '49,00 €',
        status: 'Payée'
    },
    {
        id: 2,
        date: '15 Nov 2024',
        amount: '49,00 €',
        status: 'Payée'
    },
    {
        id: 3,
        date: '15 Oct 2024',
        amount: '49,00 €',
        status: 'Payée'
    },
    {
        id: 4,
        date: '15 Sep 2024',
        amount: '49,00 €',
        status: 'Échouée'
    }
])

const getInvoiceStatusClass = (status) => {
    switch (status) {
        case 'Payée': return 'bg-green-100 text-green-800'
        case 'En attente': return 'bg-yellow-100 text-yellow-800'
        case 'Échouée': return 'bg-red-100 text-red-800'
        default: return 'bg-neutral-100 text-neutral-800'
    }
}
</script>