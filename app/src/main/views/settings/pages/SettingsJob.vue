<template>
    <div class="max-w-5xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Paramètres des interventions</h2>
            <p class="text-neutral-600">Configurez les préférences par défaut pour vos interventions.</p>
        </div>

        <div class="space-y-6">
            <div class="space-y-6">
                <div class="space-y-3">
                    <Label for="default-duration">Durée par défaut d'une intervention</Label>
                    <Select>
                        <SelectTrigger class="w-full">
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

                <div class="space-y-3">
                    <Label for="default-status">Statut par défaut</Label>
                    <Select>
                        <SelectTrigger class="w-full">
                            <SelectValue placeholder="Sélectionner un statut" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="draft">Brouillon</SelectItem>
                            <SelectItem value="planned">Planifiée</SelectItem>
                            <SelectItem value="assigned">Assignée</SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div class="space-y-3">
                    <Label for="default-priority">Priorité par défaut</Label>
                    <Select>
                        <SelectTrigger class="w-full">
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
                <h3 class="text-base font-medium text-neutral-900">Statuts d'intervention</h3>
                <p class="text-sm text-neutral-500">
                    Configurez les statuts disponibles pour vos interventions. Glissez-déposez pour réorganiser l'ordre.
                </p>

                <div class="border rounded-lg">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead class="w-12"></TableHead>
                                <TableHead>Statut</TableHead>
                                <TableHead class="w-24">Utilisé</TableHead>
                                <TableHead class="w-24">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="jobStatuses" :animation="200" handle=".drag-handle" tag="tbody">
                            <TableRow v-for="status in jobStatuses" :key="status.id">
                                <TableCell>
                                    <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                        <GripVertical class="h-4 w-4" />
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-4 h-4 rounded-full border-2 border-neutral-200"
                                            :style="{ backgroundColor: status.color }"></div>
                                        <span class="text-sm text-neutral-900">{{ status.name }}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Badge :class="status.isUsed
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-neutral-100 text-neutral-600'">
                                        {{ status.isUsed ? 'Utilisé' : 'Non utilisé' }}
                                    </Badge>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-1">
                                        <Button variant="ghost" size="sm" @click="editStatus(status)">
                                            <Edit class="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="sm" @click="removeStatus(status.id)"
                                            :disabled="status.isUsed">
                                            <Trash class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        </VueDraggable>
                    </Table>

                    <div class="p-4 border-t bg-neutral-50">
                        <Button variant="outline" size="sm" @click="openCreateDialog">
                            <Plus class="h-4 w-4 mr-2" />
                            Ajouter un statut
                        </Button>
                    </div>
                </div>

                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-4 w-4 text-blue-600" />
                        <span class="text-sm font-medium text-blue-800">Information</span>
                    </div>
                    <p class="text-sm text-blue-700">
                        L'ordre des statuts détermine leur progression logique. Les statuts utilisés dans des
                        interventions existantes ne peuvent pas être supprimés.
                    </p>
                </div>
            </div>

            <Separator />

            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Catégories d'intervention</h3>
                <p class="text-sm text-neutral-500">
                    Configurez les catégories disponibles pour vos interventions. Glissez-déposez pour réorganiser
                    l'ordre.
                </p>

                <div class="border rounded-lg">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead class="w-12"></TableHead>
                                <TableHead>Catégorie</TableHead>
                                <TableHead class="w-24">Utilisé</TableHead>
                                <TableHead class="w-24">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="jobCategories" :animation="200" handle=".drag-handle-cat" tag="tbody">
                            <TableRow v-for="category in jobCategories" :key="category.id">
                                <TableCell>
                                    <div class="drag-handle-cat cursor-move text-neutral-400 hover:text-neutral-600">
                                        <GripVertical class="h-4 w-4" />
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-4 h-4 rounded-full border-2 border-neutral-200"
                                            :style="{ backgroundColor: category.color }"></div>
                                        <span class="text-sm text-neutral-900">{{ category.name }}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <Badge :class="category.isUsed
                                        ? 'bg-green-100 text-green-800'
                                        : 'bg-neutral-100 text-neutral-600'">
                                        {{ category.isUsed ? 'Utilisé' : 'Non utilisé' }}
                                    </Badge>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-1">
                                        <Button variant="ghost" size="sm" @click="editCategory(category)">
                                            <Edit class="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="sm" @click="removeCategory(category.id)"
                                            :disabled="category.isUsed">
                                            <Trash class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </TableCell>
                            </TableRow>
                        </VueDraggable>
                    </Table>

                    <div class="p-4 border-t bg-neutral-50">
                        <Button variant="outline" size="sm" @click="openCreateCategoryDialog">
                            <Plus class="h-4 w-4 mr-2" />
                            Ajouter une catégorie
                        </Button>
                    </div>
                </div>

                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-4 w-4 text-blue-600" />
                        <span class="text-sm font-medium text-blue-800">Information</span>
                    </div>
                    <p class="text-sm text-blue-700">
                        L'ordre des catégories détermine leur affichage dans les formulaires. Les catégories utilisées
                        dans des
                        interventions existantes ne peuvent pas être supprimées.
                    </p>
                </div>
            </div>

            <Separator />

            <div class="flex justify-end">
                <Button @click="saveSettings">
                    Enregistrer les modifications
                </Button>
            </div>
        </div>

        <Dialog :open="showDialog" @update:open="showDialog = $event">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{{ editingStatus ? 'Modifier le statut' : 'Nouveau statut' }}</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="space-y-2">
                        <Label for="status-name">Nom du statut</Label>
                        <Input id="status-name" v-model="dialogStatus.name" placeholder="Ex: En cours" />
                    </div>
                    <div class="space-y-2">
                        <Label for="status-color">Couleur</Label>
                        <div class="flex items-center space-x-2">
                            <div class="w-6 h-6 rounded-full border-2 border-neutral-200"
                                :style="{ backgroundColor: dialogStatus.color }"></div>
                            <Input id="status-color" type="color" v-model="dialogStatus.color"
                                class="w-20 h-8 p-0 border-0 cursor-pointer" />
                        </div>
                    </div>
                </div>
                <div class="flex justify-end space-x-2 mt-6">
                    <Button variant="outline" @click="showDialog = false">Annuler</Button>
                    <Button @click="saveStatus">{{ editingStatus ? 'Modifier' : 'Créer' }}</Button>
                </div>
            </DialogContent>
        </Dialog>

        <Dialog :open="showCategoryDialog" @update:open="showCategoryDialog = $event">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{{ editingCategory ? 'Modifier la catégorie' : 'Nouvelle catégorie' }}</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="space-y-2">
                        <Label for="category-name">Nom de la catégorie</Label>
                        <Input id="category-name" v-model="dialogCategory.name" placeholder="Ex: Dépannage simple" />
                    </div>
                    <div class="space-y-2">
                        <Label for="category-color">Couleur</Label>
                        <div class="flex items-center space-x-2">
                            <div class="w-6 h-6 rounded-full border-2 border-neutral-200"
                                :style="{ backgroundColor: dialogCategory.color }"></div>
                            <Input id="category-color" type="color" v-model="dialogCategory.color"
                                class="w-20 h-8 p-0 border-0 cursor-pointer" />
                        </div>
                    </div>
                </div>
                <div class="flex justify-end space-x-2 mt-6">
                    <Button variant="outline" @click="showCategoryDialog = false">Annuler</Button>
                    <Button @click="saveCategory">{{ editingCategory ? 'Modifier' : 'Créer' }}</Button>
                </div>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import Dialog from '@/common/components/ui/dialog/Dialog.vue'
import DialogContent from '@/common/components/ui/dialog/DialogContent.vue'
import DialogHeader from '@/common/components/ui/dialog/DialogHeader.vue'
import DialogTitle from '@/common/components/ui/dialog/DialogTitle.vue'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import { Separator } from '@/common/components/ui/separator'
import Table from '@/common/components/ui/table/Table.vue'
import TableCell from '@/common/components/ui/table/TableCell.vue'
import TableHead from '@/common/components/ui/table/TableHead.vue'
import TableHeader from '@/common/components/ui/table/TableHeader.vue'
import TableRow from '@/common/components/ui/table/TableRow.vue'
import { Edit, GripVertical, Info, Plus, Trash } from 'lucide-vue-next'
import { ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'

const reminders = ref(true)
const lateNotifications = ref(true)
const calendarSync = ref(false)
const autoReports = ref(true)
const requiredPhotos = ref(false)
const requiredSignature = ref(true)

const jobStatuses = ref([
    {
        id: 1,
        name: 'Brouillon',
        color: '#6b7280',
        isUsed: false
    },
    {
        id: 2,
        name: 'Planifiée',
        color: '#3b82f6',
        isUsed: true
    },
    {
        id: 3,
        name: 'En cours',
        color: '#f59e0b',
        isUsed: true
    },
    {
        id: 4,
        name: 'En pause',
        color: '#8b5cf6',
        isUsed: false
    },
    {
        id: 5,
        name: 'En attente client',
        color: '#ef4444',
        isUsed: true
    },
    {
        id: 6,
        name: 'Terminée',
        color: '#10b981',
        isUsed: true
    },
    {
        id: 7,
        name: 'Annulée',
        color: '#dc2626',
        isUsed: false
    }
])

const showDialog = ref(false)
const editingStatus = ref(null)
const dialogStatus = ref({
    name: '',
    color: '#6b7280'
})

const jobCategories = ref([
    {
        id: 1,
        name: 'Dépannage simple',
        color: '#3b82f6',
        isUsed: true
    },
    {
        id: 2,
        name: 'Dépannage urgent',
        color: '#ef4444',
        isUsed: true
    },
    {
        id: 3,
        name: 'État des lieux',
        color: '#f59e0b',
        isUsed: false
    },
    {
        id: 4,
        name: 'Audit Gaz',
        color: '#8b5cf6',
        isUsed: true
    },
    {
        id: 5,
        name: 'Diagnostic Gaz',
        color: '#10b981',
        isUsed: false
    }
])

const showCategoryDialog = ref(false)
const editingCategory = ref(null)
const dialogCategory = ref({
    name: '',
    color: '#6b7280'
})

let nextStatusId = 8
let nextCategoryId = 6

const openCreateDialog = () => {
    editingStatus.value = null
    dialogStatus.value = {
        name: '',
        color: '#6b7280'
    }
    showDialog.value = true
}

const editStatus = (status) => {
    editingStatus.value = status
    dialogStatus.value = {
        name: status.name,
        color: status.color
    }
    showDialog.value = true
}

const saveStatus = () => {
    if (editingStatus.value) {
        editingStatus.value.name = dialogStatus.value.name
        editingStatus.value.color = dialogStatus.value.color
    } else {
        jobStatuses.value.push({
            id: nextStatusId++,
            name: dialogStatus.value.name,
            color: dialogStatus.value.color,
            isUsed: false
        })
    }
    showDialog.value = false
}

const removeStatus = (statusId) => {
    const index = jobStatuses.value.findIndex(status => status.id === statusId)
    if (index !== -1 && !jobStatuses.value[index].isUsed) {
        jobStatuses.value.splice(index, 1)
    }
}

const openCreateCategoryDialog = () => {
    editingCategory.value = null
    dialogCategory.value = {
        name: '',
        color: '#6b7280'
    }
    showCategoryDialog.value = true
}

const editCategory = (category) => {
    editingCategory.value = category
    dialogCategory.value = {
        name: category.name,
        color: category.color
    }
    showCategoryDialog.value = true
}

const saveCategory = () => {
    if (editingCategory.value) {
        editingCategory.value.name = dialogCategory.value.name
        editingCategory.value.color = dialogCategory.value.color
    } else {
        jobCategories.value.push({
            id: nextCategoryId++,
            name: dialogCategory.value.name,
            color: dialogCategory.value.color,
            isUsed: false
        })
    }
    showCategoryDialog.value = false
}

const removeCategory = (categoryId) => {
    const index = jobCategories.value.findIndex(category => category.id === categoryId)
    if (index !== -1 && !jobCategories.value[index].isUsed) {
        jobCategories.value.splice(index, 1)
    }
}

const saveSettings = () => {
    console.log('Paramètres sauvegardés', {
        statuses: jobStatuses.value,
        categories: jobCategories.value
    })
}
</script>