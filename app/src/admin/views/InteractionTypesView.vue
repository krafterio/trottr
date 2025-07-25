<template>
    <div>
        <div class="container mx-auto pt-6 px-5">
            <div class="mb-6 flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold mb-2">Types d'interactions</h1>
                    <p class="text-gray-600">Gérez les types d'interactions disponibles pour tous les workspaces.</p>
                </div>
                <Button @click="openCreateModal">
                    <Plus :size="16" class="mr-2" />
                    Ajouter un type
                </Button>
            </div>

            <Card class="shadow-none py-5">
                <CardContent class="px-5 py-0">
                    <div class="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead class="w-8"></TableHead>
                                    <TableHead>Nom</TableHead>
                                    <TableHead>Icône</TableHead>
                                    <TableHead>Valeur</TableHead>
                                    <TableHead class="w-20"></TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow v-if="loadingTable">
                                    <TableCell colspan="4" class="text-center py-8">
                                        <div class="flex items-center justify-center space-x-2">
                                            <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-900"></div>
                                            <span>Chargement...</span>
                                        </div>
                                    </TableCell>
                                </TableRow>
                                <TableRow v-else-if="interactionTypes.length === 0">
                                    <TableCell colspan="4" class="text-center py-8 text-gray-500">
                                        Aucun type d'interaction trouvé
                                    </TableCell>
                                </TableRow>
                                <TableRow 
                                    v-else 
                                    v-for="(type, index) in interactionTypes" 
                                    :key="type.id" 
                                    class="hover:bg-gray-50 cursor-move"
                                    draggable="true"
                                    @dragstart="onDragStart($event, type, index)"
                                    @dragover="onDragOver($event, index)"
                                    @drop="onDrop($event, index)"
                                    @dragend="onDragEnd"
                                    :class="{ 'bg-blue-50': dragOverIndex === index }"
                                >
                                    <TableCell class="w-8">
                                        <div class="flex items-center">
                                            <GripHorizontal :size="16" class="text-gray-400 drag-handle mr-2" />
                                            <IconViewer :name="type.icone" size="16" class="text-gray-600"/>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <span class="font-medium">{{ type.name }}</span>
                                    </TableCell>
                                    <TableCell>
                                        <span class="font-medium">{{ type.icone }}</span>
                                    </TableCell>
                                    <TableCell>
                                        <code class="bg-gray-100 px-2 py-1 rounded text-sm">{{ type.value }}</code>
                                    </TableCell>
                                    <TableCell>
                                        <DropdownMenu>
                                            <DropdownMenuTrigger as-child>
                                                <Button variant="ghost" size="sm" class="h-8 w-8 p-0">
                                                    <MoreHorizontal weight="bold" class="h-4 w-4" />
                                                </Button>
                                            </DropdownMenuTrigger>
                                            <DropdownMenuContent align="end">
                                                <DropdownMenuItem @click="editType(type)">
                                                    <Pencil class="mr-2 h-4 w-4" />
                                                    Modifier
                                                </DropdownMenuItem>
                                                <DropdownMenuSeparator />
                                                <DropdownMenuItem 
                                                    @click="confirmDelete(type)" 
                                                    class="text-red-600 focus:text-red-600"
                                                >
                                                    <Trash class="mr-2 h-4 w-4" />
                                                    Supprimer
                                                </DropdownMenuItem>
                                            </DropdownMenuContent>
                                        </DropdownMenu>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>

                    <div class="flex items-center justify-center mt-4">
                        <div class="text-sm text-gray-500">
                            {{ interactionTypes.length }} type(s) d'interaction{{ interactionTypes.length > 1 ? 's' : '' }}
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>

        <Dialog v-model:open="showModal">
            <DialogContent class="sm:max-w-md">
                <DialogHeader>
                    <DialogTitle class="flex items-center">
                        <ChartLine :size="20" class="mr-2" />
                        {{ editing ? 'Modifier le type d\'interaction' : 'Nouveau type d\'interaction' }}
                    </DialogTitle>
                    <DialogDescription>
                        {{ editing ? 'Modifiez les informations du type d\'interaction.' : 'Créez un nouveau type d\'interaction.' }}
                    </DialogDescription>
                </DialogHeader>

                <form @submit.prevent="save" class="space-y-4">
                    <div class="space-y-2">
                        <Label for="name">Nom du type</Label>
                        <Input 
                            id="name"
                            v-model="form.name" 
                            placeholder="Appel téléphonique" 
                            :class="errors.name ? 'border-red-500' : ''"
                            @blur="validateField('name')"
                        />
                        <p v-if="errors.name" class="text-sm text-red-500">{{ errors.name }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="icone">Icône</Label>
                        <div class="flex items-center gap-2">
                            <Popover>
                                <PopoverTrigger as-child>
                                    <Button 
                                        variant="outline" 
                                        class="w-16 h-10 p-0"
                                        :class="errors.icone ? 'border-red-500' : ''"
                                    >
                                        <IconViewer v-if="form.icone" :name="form.icone" :size="20" />
                                        <ChartLine v-else :size="20" class="text-muted-foreground" />
                                    </Button>
                                </PopoverTrigger>
                                <PopoverContent class="w-80 p-0" align="start">
                                    <IconPicker @select="selectIcon" />
                                </PopoverContent>
                            </Popover>
                            <Input 
                                id="icone"
                                v-model="form.icone" 
                                placeholder="phone" 
                                :class="errors.icone ? 'border-red-500' : ''"
                                @blur="validateField('icone')"
                                class="flex-1"
                            />
                        </div>
                        <p class="text-sm text-gray-500">Sélectionnez une icône ou saisissez le nom d'une icône Lucide</p>
                        <p v-if="errors.icone" class="text-sm text-red-500">{{ errors.icone }}</p>
                    </div>

                    <div class="space-y-2">
                        <Label for="value">Valeur (identifiant unique)</Label>
                        <Input 
                            id="value"
                            v-model="form.value" 
                            placeholder="phone_call" 
                            :class="errors.value ? 'border-red-500' : ''"
                            @blur="validateField('value')"
                        />
                        <p class="text-sm text-gray-500">Identifiant unique utilisé en interne</p>
                        <p v-if="errors.value" class="text-sm text-red-500">{{ errors.value }}</p>
                    </div>

                    <DialogFooter class="gap-2">
                        <Button type="button" variant="outline" @click="closeModal">
                            Annuler
                        </Button>
                        <Button 
                            v-if="editing" 
                            type="button" 
                            variant="destructive" 
                            :disabled="deleting" 
                            @click="confirmDelete(editing)"
                        >
                            Supprimer
                        </Button>
                        <Button 
                            type="submit" 
                            :disabled="!isFormValid || saving"
                        >
                            <span v-if="saving" class="flex items-center">
                                <span class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                                {{ editing ? 'Modification...' : 'Création...' }}
                            </span>
                            <span v-else>{{ editing ? 'Modifier' : 'Créer' }}</span>
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>

        <AlertDialog v-model:open="deleteModal">
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>Confirmation de suppression</AlertDialogTitle>
                    <AlertDialogDescription>
                        Êtes-vous sûr de vouloir supprimer le type d'interaction "{{ typeToDelete?.name }}" ? 
                        Cette action est irréversible.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Annuler</AlertDialogCancel>
                    <AlertDialogAction 
                        @click="deleteInteractionType" 
                        :disabled="deleting"
                        class="bg-red-600 hover:bg-red-700"
                    >
                        <span v-if="deleting" class="flex items-center">
                            <span class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
                            Suppression...
                        </span>
                        <span v-else>Supprimer</span>
                    </AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useFetcher } from "@/common/composables/fetcher"
import { toast } from 'vue-sonner'

import { Card, CardContent } from '@/common/components/ui/card'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/common/components/ui/table'
import { Button } from '@/common/components/ui/button'
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/common/components/ui/dropdown-menu'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/common/components/ui/dialog'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
} from '@/common/components/ui/alert-dialog'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import { Popover, PopoverContent, PopoverTrigger } from '@/common/components/ui/popover'
import {
    GripHorizontal,
    MoreHorizontal,
    Plus,
    Trash,
    Pencil,
    ChartLine,
} from 'lucide-vue-next'
import { IconViewer, IconPicker } from "@/common/components/ui/icon/index.js";

const fetcher = useFetcher()

const loadingTable = ref(false)
const interactionTypes = ref([])
const showModal = ref(false)
const editing = ref(null)
const saving = ref(false)
const deleting = ref(false)
const deleteModal = ref(false)
const typeToDelete = ref(null)
const draggedItem = ref(null)
const draggedIndex = ref(null)
const dragOverIndex = ref(null)

const form = ref({
    name: '',
    value: '',
    sequence: 0,
    icone: ''
})

const errors = ref({
    name: '',
    value: '',
    icone: ''
})

const isFormValid = computed(() => {
    return form.value.name.trim() !== '' && 
           form.value.value.trim() !== '' && 
           !errors.value.name && 
           !errors.value.value && 
           !errors.value.icone
})

const validateField = (field) => {
    errors.value[field] = ''
    
    switch (field) {
        case 'name':
            if (!form.value.name.trim()) {
                errors.value.name = 'Le nom du type est requis'
            }
            break
        case 'value':
            if (!form.value.value.trim()) {
                errors.value.value = 'La valeur est requise'
            } else if (!/^[a-z0-9_]+$/.test(form.value.value)) {
                errors.value.value = 'La valeur ne peut contenir que des lettres minuscules, chiffres et underscores'
            }
            break
        case 'icone':
            if (form.value.icone.trim() && !/^[A-Za-z0-9]+$/.test(form.value.icone)) {
                errors.value.icone = 'Le nom d\'icône ne peut contenir que des lettres et chiffres'
            }
            break
    }
}

const validateForm = () => {
    validateField('name')
    validateField('value')
    validateField('icone')
    return isFormValid.value
}

const fetchInteractionTypes = async () => {
    loadingTable.value = true
    try {
        const { data } = await fetcher.get(`/admin/interaction-types`)
        interactionTypes.value = data.items
    } catch (error) {
        console.error('Erreur lors du chargement des types d\'interaction:', error)
        toast.error('Erreur lors du chargement des types d\'interaction')
    } finally {
        loadingTable.value = false
    }
}

const openCreateModal = () => {
    editing.value = null
    form.value = {
        name: '',
        value: '',
        sequence: 0,
        icone: ''
    }
    errors.value = {
        name: '',
        value: '',
        icone: ''
    }
    showModal.value = true
}

const selectIcon = (iconName) => {
    form.value.icone = iconName
    if (errors.value.icone) {
        validateField('icone')
    }
}

const editType = (type) => {
    editing.value = type
    form.value = {
        name: type.name,
        value: type.value,
        sequence: type.sequence,
        icone: type.icone
    }
    errors.value = {
        name: '',
        value: '',
        icone: ''
    }
    showModal.value = true
}

const closeModal = () => {
    showModal.value = false
    editing.value = null
}

const confirmDelete = (type) => {
    typeToDelete.value = type
    deleteModal.value = true
    if (showModal.value) {
        showModal.value = false
    }
}

const save = async () => {
    if (!validateForm()) return

    saving.value = true
    try {
        const data = { ...form.value }

        if (editing.value) {
            await fetcher.patch(`/admin/interaction-types/${editing.value.id}`, data)
            toast.success('Type d\'interaction modifié avec succès')
        } else {
            await fetcher.post(`/admin/interaction-types`, data)
            toast.success('Type d\'interaction créé avec succès')
        }

        await fetchInteractionTypes()
        closeModal()
    } catch (error) {
        console.error('Erreur lors de la sauvegarde:', error)
        toast.error('Erreur lors de la sauvegarde')
    } finally {
        saving.value = false
    }
}

const deleteInteractionType = async () => {
    if (!typeToDelete.value) return
    
    deleting.value = true
    try {
        await fetcher.delete(`/admin/interaction-types/${typeToDelete.value.id}`)
        toast.success('Type d\'interaction supprimé avec succès')
        await fetchInteractionTypes()
        deleteModal.value = false
    } catch (error) {
        console.error('Erreur lors de la suppression:', error)
        toast.error('Erreur lors de la suppression')
    } finally {
        deleting.value = false
    }
}

const onDragStart = (event, item, index) => {
    draggedItem.value = item
    draggedIndex.value = index
    event.dataTransfer.effectAllowed = 'move'
    event.target.classList.add('opacity-50')
}

const onDragOver = (event, index) => {
    event.preventDefault()
    dragOverIndex.value = index
}

const onDrop = async (event, index) => {
    event.preventDefault()
    dragOverIndex.value = null

    if (draggedIndex.value === null || draggedIndex.value === index) {
        return
    }

    const newItems = [...interactionTypes.value]
    const draggedItemData = newItems.splice(draggedIndex.value, 1)[0]
    newItems.splice(index, 0, draggedItemData)

    interactionTypes.value = newItems

    const reorderedIds = newItems.map(item => item.id)

    try {
        await fetcher.post(`/admin/interaction-types/reorder`, reorderedIds)
        toast.success('Ordre des types d\'interaction mis à jour')
        await fetchInteractionTypes()
    } catch (error) {
        console.error('Erreur lors de la réorganisation:', error)
        toast.error('Erreur lors de la réorganisation')
        await fetchInteractionTypes()
    }
}

const onDragEnd = (event) => {
    event.target.classList.remove('opacity-50')
    draggedItem.value = null
    draggedIndex.value = null
    dragOverIndex.value = null
}



onMounted(() => {
    fetchInteractionTypes()
})
</script> 
