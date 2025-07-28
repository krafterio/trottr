<template>
    <div class="max-w-5xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Paramètres CRM</h2>
            <p class="text-neutral-600">Configurez les paramètres de gestion de la relation client.</p>
        </div>

        <div class="space-y-6">
            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Relation contact avec sites</h3>
                <p class="text-sm text-neutral-500">
                    Configurez les types de relations disponibles entre les contacts et les sites. Glissez-déposez pour
                    réorganiser l'ordre.
                </p>

                <div class="border rounded-lg">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead class="w-12"></TableHead>
                                <TableHead>Relation</TableHead>
                                <TableHead class="w-24">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="contactRelationTypes" :animation="200" handle=".drag-handle" tag="tbody"
                            @end="onRelationReorder">
                            <TableRow v-for="relation in contactRelationTypes" :key="relation.id">
                                <TableCell>
                                    <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                        <GripVertical class="h-4 w-4" />
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-3">
                                        <span class="text-sm text-neutral-900">{{ relation.name }}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-1">
                                        <Button variant="ghost" size="sm" @click="editRelation(relation)">
                                            <Edit class="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="sm" @click="removeRelation(relation.id)"
                                            :disabled="relation.isUsed">
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
                            Ajouter une relation
                        </Button>
                    </div>
                </div>

                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-4 w-4 text-blue-600" />
                        <span class="text-sm font-medium text-blue-800">Information</span>
                    </div>
                    <p class="text-sm text-blue-700">
                        L'ordre des relations détermine leur affichage dans les formulaires. Les relations utilisées
                        dans des contacts existants ne peuvent pas être supprimées.
                    </p>
                </div>
            </div>
        </div>

        <Dialog :open="showDialog" @update:open="showDialog = $event">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{{ editingRelation ? 'Modifier la relation' : 'Nouvelle relation' }}</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="space-y-2">
                        <Label for="relation-name">Nom de la relation</Label>
                        <Input id="relation-name" v-model="dialogRelation.name" placeholder="Ex: Responsable site" />
                    </div>
                </div>
                <div class="flex justify-end space-x-2 mt-6">
                    <Button variant="outline" @click="showDialog = false">Annuler</Button>
                    <Button @click="saveRelation" :disabled="loading">{{ editingRelation ? 'Modifier' : 'Créer'
                        }}</Button>
                </div>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import Dialog from '@/common/components/ui/dialog/Dialog.vue'
import DialogContent from '@/common/components/ui/dialog/DialogContent.vue'
import DialogHeader from '@/common/components/ui/dialog/DialogHeader.vue'
import DialogTitle from '@/common/components/ui/dialog/DialogTitle.vue'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import Table from '@/common/components/ui/table/Table.vue'
import TableCell from '@/common/components/ui/table/TableCell.vue'
import TableHead from '@/common/components/ui/table/TableHead.vue'
import TableHeader from '@/common/components/ui/table/TableHeader.vue'
import TableRow from '@/common/components/ui/table/TableRow.vue'
import { useFetcher } from '@/common/composables/fetcher'
import {
    Edit,
    GripVertical,
    Info,
    Plus,
    Trash
} from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { toast } from 'vue-sonner'

const fetcher = useFetcher()
const loading = ref(false)

const contactRelationTypes = ref([])

const showDialog = ref(false)
const editingRelation = ref(null)
const dialogRelation = ref({
    name: '',
    sequence: 1
})

const loadContactRelationTypes = async () => {
    try {
        const response = await fetcher.get('/contact-relation-type')
        contactRelationTypes.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des relations:', error)
        toast.error('Impossible de charger les relations')
    }
}

const openCreateDialog = () => {
    editingRelation.value = null
    const maxSequence = Math.max(...contactRelationTypes.value.map(r => r.sequence), 0)
    dialogRelation.value = {
        name: '',
        sequence: maxSequence + 1
    }
    showDialog.value = true
}

const editRelation = (relation) => {
    editingRelation.value = relation
    dialogRelation.value = {
        name: relation.name,
        sequence: relation.sequence
    }
    showDialog.value = true
}

const saveRelation = async () => {
    if (!dialogRelation.value.name.trim()) {
        toast.error('Le nom de la relation est requis')
        return
    }

    loading.value = true
    try {
        if (editingRelation.value) {
            const { sequence, ...updateData } = dialogRelation.value
            await fetcher.patch(`/contact-relation-type/${editingRelation.value.id}`, updateData)
        } else {
            await fetcher.post('/contact-relation-type', dialogRelation.value)
        }

        await loadContactRelationTypes()
        showDialog.value = false
        toast.success(`Relation ${editingRelation.value ? 'modifiée' : 'créée'} avec succès`)
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error(error.message || 'Erreur lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}

const removeRelation = async (relationId) => {
    try {
        await fetcher.delete(`/contact-relation-type/${relationId}`)
        await loadContactRelationTypes()
        toast.success('Relation supprimée avec succès')
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error(error.message || 'Erreur lors de la suppression')
    }
}

const onRelationReorder = async () => {
    try {
        const reorderedTypes = contactRelationTypes.value.map((relation, index) => ({
            id: relation.id,
            sequence: index + 1
        }))

        await fetcher.put('/contact-relation-type/reorder', { types: reorderedTypes })
        toast.success('Relations réorganisées avec succès')
    } catch (error) {
        console.error('Erreur lors de la réorganisation des relations:', error)
        toast.error(error.message || 'Erreur lors de la réorganisation des relations')
        await loadContactRelationTypes()
    }
}

onMounted(() => {
    loadContactRelationTypes()
})
</script>