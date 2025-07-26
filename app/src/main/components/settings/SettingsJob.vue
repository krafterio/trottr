<template>
    <div class="max-w-2xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Paramètres des interventions</h2>
            <p class="text-neutral-600">Configurez les préférences par défaut pour vos interventions.</p>
        </div>

        <div class="space-y-6">
            <div class="space-y-4">
                <div class="space-y-2">
                    <Label for="default-duration">Durée par défaut d'une intervention</Label>
                    <Select>
                        <SelectTrigger class="max-w-sm">
                            <SelectValue placeholder="Sélectionner une durée" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="30">30 minutes</SelectItem>
                            <SelectItem value="60">1 heure</SelectItem>
                            <SelectItem value="90">1h30</SelectItem>
                            <SelectItem value="120">2 heures</SelectItem>
                            <SelectItem value="180">3 heures</SelectItem>
                            <SelectItem value="240">4 heures</SelectItem>
                        </SelectContent>
                    </Select>
                    <p class="text-sm text-neutral-500">
                        Durée appliquée automatiquement lors de la création d'une nouvelle intervention.
                    </p>
                </div>

                <div class="space-y-2">
                    <Label for="default-status">Statut par défaut</Label>
                    <Select>
                        <SelectTrigger class="max-w-sm">
                            <SelectValue placeholder="Sélectionner un statut" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="draft">Brouillon</SelectItem>
                            <SelectItem value="planned">Planifiée</SelectItem>
                            <SelectItem value="assigned">Assignée</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div class="space-y-2">
                    <Label for="default-priority">Priorité par défaut</Label>
                    <Select>
                        <SelectTrigger class="max-w-sm">
                            <SelectValue placeholder="Sélectionner une priorité" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="low">Faible</SelectItem>
                            <SelectItem value="normal">Normale</SelectItem>
                            <SelectItem value="high">Élevée</SelectItem>
                            <SelectItem value="urgent">Urgente</SelectItem>
                        </SelectContent>
                    </Select>
                </div>
            </div>

            <Separator />

            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Notifications d'intervention</h3>

                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Rappels automatiques</Label>
                            <p class="text-sm text-neutral-500">
                                Envoyer des rappels automatiques avant les interventions
                            </p>
                        </div>
                        <Switch v-model:checked="reminders" />
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Notifications de retard</Label>
                            <p class="text-sm text-neutral-500">
                                Alerter quand une intervention est en retard
                            </p>
                        </div>
                        <Switch v-model:checked="lateNotifications" />
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Synchronisation calendrier</Label>
                            <p class="text-sm text-neutral-500">
                                Synchroniser les interventions avec votre calendrier externe
                            </p>
                        </div>
                        <Switch v-model:checked="calendarSync" />
                    </div>
                </div>
            </div>

            <Separator />

            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Rapports d'intervention</h3>

                <div class="space-y-3">
                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Génération automatique</Label>
                            <p class="text-sm text-neutral-500">
                                Générer automatiquement le rapport à la fin de l'intervention
                            </p>
                        </div>
                        <Switch v-model:checked="autoReports" />
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Photos obligatoires</Label>
                            <p class="text-sm text-neutral-500">
                                Exiger des photos avant/après pour chaque intervention
                            </p>
                        </div>
                        <Switch v-model:checked="requiredPhotos" />
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="space-y-0.5">
                            <Label>Signature client obligatoire</Label>
                            <p class="text-sm text-neutral-500">
                                Exiger la signature du client pour valider l'intervention
                            </p>
                        </div>
                        <Switch v-model:checked="requiredSignature" />
                    </div>
                </div>
            </div>

            <Separator />

            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Templates de description</h3>
                <p class="text-sm text-neutral-500">
                    Définissez des templates pour accélérer la création d'interventions
                </p>

                <div class="space-y-3">
                    <div class="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                            <p class="text-sm font-medium">Dépannage plomberie</p>
                            <p class="text-xs text-neutral-500">Intervention de dépannage urgent en plomberie</p>
                        </div>
                        <Button variant="ghost" size="sm">
                            <Edit class="h-4 w-4" />
                        </Button>
                    </div>

                    <div class="flex items-center justify-between p-3 border rounded-lg">
                        <div>
                            <p class="text-sm font-medium">Installation équipement</p>
                            <p class="text-xs text-neutral-500">Installation et mise en service d'équipements</p>
                        </div>
                        <Button variant="ghost" size="sm">
                            <Edit class="h-4 w-4" />
                        </Button>
                    </div>

                    <Button variant="outline" size="sm">
                        <Plus class="h-4 w-4 mr-2" />
                        Ajouter un template
                    </Button>
                </div>
            </div>

            <Separator />

            <div class="flex justify-end">
                <Button @click="saveSettings">
                    Enregistrer les modifications
                </Button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Label } from '@/common/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import { Switch } from '@/common/components/ui/switch'
import { Edit, Plus } from 'lucide-vue-next'
import { ref } from 'vue'

const reminders = ref(true)
const lateNotifications = ref(true)
const calendarSync = ref(false)
const autoReports = ref(true)
const requiredPhotos = ref(false)
const requiredSignature = ref(true)

const saveSettings = () => {
    console.log('Paramètres sauvegardés')
}
</script>