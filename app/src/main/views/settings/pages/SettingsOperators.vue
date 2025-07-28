<template>
    <div class="max-w-5xl">
        <div class="mb-6">
            <h2 class="text-lg font-semibold text-neutral-900">Paramètres des opérateurs</h2>
            <p class="text-neutral-600">Configurez les spécialités disponibles pour vos opérateurs.</p>
        </div>

        <div class="space-y-6">
            <div class="space-y-4">
                <h3 class="text-base font-medium text-neutral-900">Spécialités d'opérateur</h3>
                <p class="text-sm text-neutral-500">
                    Configurez les spécialités disponibles pour vos opérateurs. Glissez-déposez pour réorganiser
                    l'ordre.
                </p>

                <div class="border rounded-lg">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead class="w-12"></TableHead>
                                <TableHead>Spécialité</TableHead>
                                <TableHead class="w-24">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <VueDraggable v-model="jobSpecialities" :animation="200" handle=".drag-handle" tag="tbody"
                            @end="onSpecialityReorder">
                            <TableRow v-for="speciality in jobSpecialities" :key="speciality.id">
                                <TableCell>
                                    <div class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                        <GripVertical class="h-4 w-4" />
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-3">
                                        <div class="w-4 h-4 rounded-full border-2 border-neutral-200"
                                            :style="{ backgroundColor: speciality.color }"></div>
                                        <span class="text-sm text-neutral-900">{{ speciality.name }}</span>
                                    </div>
                                </TableCell>
                                <TableCell>
                                    <div class="flex items-center space-x-1">
                                        <Button variant="ghost" size="sm" @click="editSpeciality(speciality)">
                                            <Edit class="h-4 w-4" />
                                        </Button>
                                        <Button variant="ghost" size="sm" @click="removeSpeciality(speciality.id)"
                                            :disabled="speciality.isUsed">
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
                            Ajouter une spécialité
                        </Button>
                    </div>
                </div>

                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-4 w-4 text-blue-600" />
                        <span class="text-sm font-medium text-blue-800">Information</span>
                    </div>
                    <p class="text-sm text-blue-700">
                        L'ordre des spécialités détermine leur affichage dans les formulaires. Les spécialités utilisées
                        par des opérateurs existants ne peuvent pas être supprimées.
                    </p>
                </div>
            </div>
        </div>

        <Dialog :open="showDialog" @update:open="showDialog = $event">
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>{{ editingSpeciality ? 'Modifier la spécialité' : 'Nouvelle spécialité' }}
                    </DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="space-y-2">
                        <Label for="speciality-name">Nom de la spécialité</Label>
                        <Input id="speciality-name" v-model="dialogSpeciality.name" placeholder="Ex: Électricité" />
                    </div>
                    <div class="space-y-2">
                        <Label for="speciality-color">Couleur</Label>
                        <div class="flex items-center space-x-3">
                            <SimpleColorPicker v-model="dialogSpeciality.color" />
                        </div>
                    </div>
                </div>
                <div class="flex justify-end space-x-2 mt-6">
                    <Button variant="outline" @click="showDialog = false">Annuler</Button>
                    <Button @click="saveSpeciality" :disabled="loading">{{ editingSpeciality ? 'Modifier' : 'Créer'
                        }}</Button>
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

const jobSpecialities = ref([])

const showDialog = ref(false)
const editingSpeciality = ref(null)
const dialogSpeciality = ref({
    name: '',
    color: '#1dbcad',
    sequence: 1
})

const loadJobSpecialities = async () => {
    try {
        const response = await fetcher.get('/job-speciality')
        jobSpecialities.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des spécialités:', error)
        toast.error('Impossible de charger les spécialités')
    }
}

const openCreateDialog = () => {
    editingSpeciality.value = null
    const maxSequence = Math.max(...jobSpecialities.value.map(s => s.sequence), 0)
    dialogSpeciality.value = {
        name: '',
        color: '#1dbcad',
        sequence: maxSequence + 1
    }
    showDialog.value = true
}

const editSpeciality = (speciality) => {
    editingSpeciality.value = speciality
    dialogSpeciality.value = {
        name: speciality.name,
        color: speciality.color,
        sequence: speciality.sequence
    }
    showDialog.value = true
}

const saveSpeciality = async () => {
    if (!dialogSpeciality.value.name.trim()) {
        toast.error('Le nom de la spécialité est requis')
        return
    }

    loading.value = true
    try {
        if (editingSpeciality.value) {
            const { sequence, ...updateData } = dialogSpeciality.value
            await fetcher.patch(`/job-speciality/${editingSpeciality.value.id}`, updateData)
        } else {
            await fetcher.post('/job-speciality', dialogSpeciality.value)
        }

        await loadJobSpecialities()
        showDialog.value = false
        toast.success(`Spécialité ${editingSpeciality.value ? 'modifiée' : 'créée'} avec succès`)
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error(error.message || 'Erreur lors de la sauvegarde')
    } finally {
        loading.value = false
    }
}

const removeSpeciality = async (specialityId) => {
    try {
        await fetcher.delete(`/job-speciality/${specialityId}`)
        await loadJobSpecialities()
        toast.success('Spécialité supprimée avec succès')
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error(error.message || 'Erreur lors de la suppression')
    }
}

const onSpecialityReorder = async () => {
    try {
        const reorderedSpecialities = jobSpecialities.value.map((speciality, index) => ({
            id: speciality.id,
            sequence: index + 1
        }))

        await fetcher.put('/job-speciality/reorder', { specialities: reorderedSpecialities })
        toast.success('Spécialités réorganisées avec succès')
    } catch (error) {
        console.error('Erreur lors de la réorganisation des spécialités:', error)
        toast.error(error.message || 'Erreur lors de la réorganisation des spécialités')
        await loadJobSpecialities()
    }
}

onMounted(() => {
    loadJobSpecialities()
})
</script>