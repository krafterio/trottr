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
                            <SelectItem value="90">1 heure 30 minutes</SelectItem>
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
                                <TableHead class="w-24">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="jobStatuses" :animation="200" handle=".drag-handle" tag="tbody"
                            @end="onStatusReorder">
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
                        <div class="flex items-center space-x-3">
                            <SimpleColorPicker v-model="dialogStatus.color" />
                        </div>
                    </div>
                </div>
                <div class="flex justify-end space-x-2 mt-6">
                    <Button variant="outline" @click="showDialog = false">Annuler</Button>
                    <Button @click="saveStatus" :disabled="loading">{{ editingStatus ? 'Modifier' : 'Créer' }}</Button>
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
                        <div class="flex items-center space-x-3">
                            <SimpleColorPicker v-model="dialogCategory.color" />
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
import SimpleColorPicker from '@/common/components/form/color-picker/SimpleColorPicker.vue'
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
import { useFetcher } from '@/common/composables/fetcher'
import { Edit, GripVertical, Info, Plus, Trash } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { toast } from 'vue-sonner'

const fetcher = useFetcher()
const loading = ref(false)

const jobStatuses = ref([])

const showDialog = ref(false)
const editingStatus = ref(null)
const dialogStatus = ref({
    name: '',
    color: '#1dbcad',
    sequence: 1
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
    color: '#1dbcad'
})

let nextCategoryId = 6

const loadJobStatuses = async () => {
    try {
        const response = await fetcher.get('/job-status')
        jobStatuses.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des statuts:', error)
        toast.error('Impossible de charger les statuts')
    }
}

const openCreateDialog = () => {
    editingStatus.value = null
    const maxSequence = Math.max(...jobStatuses.value.map(s => s.sequence), 0)
    dialogStatus.value = {
        name: '',
        color: '#1dbcad',
        sequence: maxSequence + 1
    }
    showDialog.value = true
}

const editStatus = (status) => {
    editingStatus.value = status
    dialogStatus.value = {
        name: status.name,
        color: status.color,
        sequence: status.sequence
    }
    showDialog.value = true
}

const saveStatus = async () => {
    if (!dialogStatus.value.name.trim()) {
        toast.error('Le nom du statut est requis')
        return
    }

    loading.value = true
    try {
        if (editingStatus.value) {
            const { sequence, ...updateData } = dialogStatus.value
            await fetcher.patch(`/job-status/${editingStatus.value.id}`, updateData)
        } else {
            await fetcher.post('/job-status', dialogStatus.value)
        }

        await loadJobStatuses()
        showDialog.value = false
        toast.success(`Statut ${editingStatus.value ? 'modifié' : 'créé'} avec succès`)
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error(error.message || 'Erreur lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}

const removeStatus = async (statusId) => {
    try {
        await fetcher.delete(`/job-status/${statusId}`)
        await loadJobStatuses()
        toast.success('Statut supprimé avec succès')
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error(error.message || 'Erreur lors de la suppression')
    }
}

const openCreateCategoryDialog = () => {
    editingCategory.value = null
    dialogCategory.value = {
        name: '',
        color: '#1dbcad'
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

const onStatusReorder = async () => {
    try {
        const reorderedStatuses = jobStatuses.value.map((status, index) => ({
            id: status.id,
            sequence: index + 1
        }))

        await fetcher.put('/job-status/reorder', { statuses: reorderedStatuses })
        toast.success('Statuts réorganisés avec succès')
    } catch (error) {
        console.error('Erreur lors de la réorganisation des statuts:', error)
        toast.error(error.message || 'Erreur lors de la réorganisation des statuts')
        await loadJobStatuses()
    }
}

onMounted(() => {
    loadJobStatuses()
})
</script>