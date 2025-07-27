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
                        <VueDraggable v-model="contactSiteRelations" :animation="200" handle=".drag-handle" tag="tbody">
                            <TableRow v-for="relation in contactSiteRelations" :key="relation.id">
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

        <!-- Modal d'édition -->
        <Dialog v-model:open="isEditModalOpen">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{{ editingRelation?.id ? 'Modifier' : 'Ajouter' }} une relation</DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div>
                        <label class="text-sm font-medium text-neutral-700">Libellé</label>
                        <Input v-model="editingRelation.name" class="mt-1" placeholder="Ex: Responsable site" />
                    </div>
                </div>
                <DialogFooter>
                    <Button variant="outline" @click="cancelEdit">Annuler</Button>
                    <Button @click="saveRelation">{{ editingRelation?.id ? 'Modifier' : 'Ajouter' }}</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Table, TableCell, TableHead, TableHeader, TableRow } from '@/common/components/ui/table'
import {
    Edit,
    GripVertical,
    Info,
    Plus,
    Trash
} from 'lucide-vue-next'
import { ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'

const contactSiteRelations = ref([
    {
        id: 1,
        name: 'Responsable site',
        isUsed: true
    },
    {
        id: 2,
        name: 'Propriétaire',
        isUsed: true
    },
    {
        id: 3,
        name: 'Occupant',
        isUsed: false
    },
    {
        id: 4,
        name: 'Gestionnaire',
        isUsed: true
    },
    {
        id: 5,
        name: 'Gardien / Agent local',
        isUsed: false
    },
    {
        id: 6,
        name: 'Chargé d\'exploitation',
        isUsed: false
    }
])

const isEditModalOpen = ref(false)
const editingRelation = ref({
    id: null,
    name: ''
})

const editRelation = (relation) => {
    editingRelation.value = { ...relation }
    isEditModalOpen.value = true
}

const removeRelation = (id) => {
    contactSiteRelations.value = contactSiteRelations.value.filter(relation => relation.id !== id)
}

const openCreateDialog = () => {
    editingRelation.value = {
        id: null,
        name: ''
    }
    isEditModalOpen.value = true
}

const cancelEdit = () => {
    editingRelation.value = {
        id: null,
        name: ''
    }
    isEditModalOpen.value = false
}

const saveRelation = () => {
    if (editingRelation.value.id) {
        const index = contactSiteRelations.value.findIndex(relation => relation.id === editingRelation.value.id)
        if (index !== -1) {
            contactSiteRelations.value[index] = { ...editingRelation.value }
        }
    } else {
        const newId = Math.max(...contactSiteRelations.value.map(s => s.id)) + 1
        contactSiteRelations.value.push({
            ...editingRelation.value,
            id: newId,
            isUsed: false
        })
    }
    cancelEdit()
}
</script>