<template>
    <Dialog v-model:open="dialogOpen" :modal="true">
        <DialogContent class="sm:max-w-[800px]">
            <DialogHeader>
                <DialogTitle>Ajouter des pièces jointes</DialogTitle>
                <DialogDescription>
                    {{ showExistingPictures ? 'Sélectionnez des photos existantes ou ajoutez de nouveaux fichiers' :
                        'Glissez-déposez vos fichiers ici ou cliquez pour sélectionner' }}
                </DialogDescription>
            </DialogHeader>

            <div v-if="showExistingPictures" class="space-y-4">
                <Tabs v-model="activeTab" class="w-full">
                    <TabsList class="grid w-full grid-cols-2">
                        <TabsTrigger value="upload">Nouveaux fichiers</TabsTrigger>
                        <TabsTrigger value="gallery">Photos existantes</TabsTrigger>
                    </TabsList>

                    <TabsContent value="upload" class="space-y-6">
                        <div class="border-2 border-dashed border-neutral-300 rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer"
                            @click="triggerFileInput" @dragover.prevent="handleDragOver"
                            @dragleave.prevent="handleDragLeave" @drop.prevent="handleDrop"
                            :class="{ 'border-primary bg-primary/5': isDragOver }">
                            <div v-if="!isDragOver">
                                <Upload class="h-12 w-12 mx-auto mb-4 text-neutral-400" />
                                <p class="text-lg font-medium text-neutral-900 mb-2">Glissez vos fichiers ici</p>
                                <p class="text-sm text-neutral-500 mb-4">ou cliquez pour sélectionner des fichiers</p>
                                <p class="text-xs text-neutral-400">PNG, JPG, PDF, DOC, XLS jusqu'à 10MB</p>
                            </div>
                            <div v-else class="text-primary">
                                <Upload class="h-12 w-12 mx-auto mb-4" />
                                <p class="text-lg font-medium">Déposez vos fichiers ici</p>
                            </div>
                        </div>

                        <input ref="fileInput" type="file" multiple accept="image/*,.pdf,.doc,.docx,.xls,.xlsx"
                            class="hidden" @change="handleFileSelect" />

                        <div v-if="uploadedFiles.length > 0" class="space-y-4">
                            <div class="flex items-center justify-between">
                                <h3 class="font-medium text-neutral-900">Fichiers sélectionnés</h3>
                                <Button variant="outline" size="sm" @click="clearFiles">
                                    <Trash2 class="h-4 w-4 mr-2" />
                                    Tout supprimer
                                </Button>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div v-for="file in uploadedFiles" :key="file.id"
                                    class="border rounded-lg p-3 bg-white">
                                    <div class="flex items-start gap-3">
                                        <div class="flex-shrink-0">
                                            <div v-if="file.type === 'image'"
                                                class="w-12 h-12 rounded border overflow-hidden">
                                                <img :src="file.preview" :alt="file.name"
                                                    class="w-full h-full object-cover" />
                                            </div>
                                            <div v-else
                                                class="w-12 h-12 rounded border bg-neutral-100 flex items-center justify-center">
                                                <FileText class="h-6 w-6 text-neutral-500" />
                                            </div>
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <p class="text-sm font-medium text-neutral-900 truncate">{{ file.name }}</p>
                                            <p class="text-xs text-neutral-500">{{ formatFileSize(file.size) }}</p>
                                            <div class="flex items-center gap-2 mt-2">
                                                <Badge :variant="file.type === 'image' ? 'default' : 'secondary'"
                                                    class="text-xs">
                                                    {{ file.type === 'image' ? 'Photo' : 'Document' }}
                                                </Badge>
                                                <Badge variant="outline" class="text-xs">
                                                    {{ file.extension.toUpperCase() }}
                                                </Badge>
                                            </div>
                                        </div>
                                        <Button variant="ghost" size="sm" @click="removeFile(file.id)"
                                            class="flex-shrink-0">
                                            <X class="h-4 w-4" />
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </TabsContent>

                    <TabsContent value="gallery" class="space-y-4">
                        <div v-if="loadingGallery" class="flex items-center justify-center py-8">
                            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
                        </div>

                        <div v-else-if="existingPictures.length === 0" class="text-center py-8 text-neutral-500">
                            <Image class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
                            <p>Aucune photo disponible</p>
                            <p class="text-sm mt-2">Aucune photo n'a été trouvée dans la galerie</p>
                        </div>

                        <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                            <div v-for="picture in existingPictures" :key="picture.id"
                                class="relative group cursor-pointer" @click="togglePictureSelection(picture)">
                                <div class="aspect-square rounded-lg overflow-hidden transition-all"
                                    :class="picture.selected ? 'ring-3 ring-primary' : 'border-neutral-200 hover:border-neutral-300'">
                                    <img :src="picture.url" :alt="picture.name" class="w-full h-full object-cover" />
                                    <div v-if="picture.selected"
                                        class="absolute top-2 right-2 w-6 h-6 bg-primary rounded-full flex items-center justify-center">
                                        <Check class="h-4 w-4 text-white" />
                                    </div>
                                </div>
                            </div>
                        </div>

                    </TabsContent>
                </Tabs>

                <div class="flex items-center justify-between pt-4 border-t">
                    <div class="text-sm text-neutral-500">
                        <span v-if="activeTab === 'upload' && uploadedFiles.length > 0">
                            {{ uploadedFiles.length }} fichier(s) sélectionné(s)
                        </span>
                        <span v-else-if="activeTab === 'gallery' && selectedPicturesCount > 0">
                            {{ selectedPicturesCount }} photo(s) sélectionnée(s)
                        </span>
                        <span v-else>Aucun fichier sélectionné</span>
                    </div>
                    <div class="flex gap-2">
                        <Button variant="outline" @click="dialogOpen = false">
                            Annuler
                        </Button>
                        <Button @click="uploadFiles"
                            :disabled="(activeTab === 'upload' && uploadedFiles.length === 0) || (activeTab === 'gallery' && selectedPicturesCount === 0)">
                            <Upload class="h-4 w-4 mr-2" />
                            <span v-if="activeTab === 'upload'">
                                Envoyer {{ uploadedFiles.length }} fichier(s)
                            </span>
                            <span v-else>
                                Sélectionner {{ selectedPicturesCount }} photo(s)
                            </span>
                        </Button>
                    </div>
                </div>
            </div>

            <div v-else class="space-y-6">
                <div class="border-2 border-dashed border-neutral-300 rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer"
                    @click="triggerFileInput" @dragover.prevent="handleDragOver" @dragleave.prevent="handleDragLeave"
                    @drop.prevent="handleDrop" :class="{ 'border-primary bg-primary/5': isDragOver }">
                    <div v-if="!isDragOver">
                        <Upload class="h-12 w-12 mx-auto mb-4 text-neutral-400" />
                        <p class="text-lg font-medium text-neutral-900 mb-2">Glissez vos fichiers ici</p>
                        <p class="text-sm text-neutral-500 mb-4">ou cliquez pour sélectionner des fichiers</p>
                        <p class="text-xs text-neutral-400">PNG, JPG, PDF, DOC, XLS jusqu'à 10MB</p>
                    </div>
                    <div v-else class="text-primary">
                        <Upload class="h-12 w-12 mx-auto mb-4" />
                        <p class="text-lg font-medium">Déposez vos fichiers ici</p>
                    </div>
                </div>

                <input ref="fileInput" type="file" multiple accept="image/*,.pdf,.doc,.docx,.xls,.xlsx" class="hidden"
                    @change="handleFileSelect" />

                <div v-if="uploadedFiles.length > 0" class="space-y-4">
                    <div class="flex items-center justify-between">
                        <h3 class="font-medium text-neutral-900">Fichiers sélectionnés</h3>
                        <Button variant="outline" size="sm" @click="clearFiles">
                            <Trash2 class="h-4 w-4 mr-2" />
                            Tout supprimer
                        </Button>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div v-for="file in uploadedFiles" :key="file.id" class="border rounded-lg p-3 bg-white">
                            <div class="flex items-start gap-3">
                                <div class="flex-shrink-0">
                                    <div v-if="file.type === 'image'" class="w-12 h-12 rounded border overflow-hidden">
                                        <img :src="file.preview" :alt="file.name" class="w-full h-full object-cover" />
                                    </div>
                                    <div v-else
                                        class="w-12 h-12 rounded border bg-neutral-100 flex items-center justify-center">
                                        <FileText class="h-6 w-6 text-neutral-500" />
                                    </div>
                                </div>
                                <div class="flex-1 min-w-0">
                                    <p class="text-sm font-medium text-neutral-900 truncate">{{ file.name }}</p>
                                    <p class="text-xs text-neutral-500">{{ formatFileSize(file.size) }}</p>
                                    <div class="flex items-center gap-2 mt-2">
                                        <Badge :variant="file.type === 'image' ? 'default' : 'secondary'"
                                            class="text-xs">
                                            {{ file.type === 'image' ? 'Photo' : 'Document' }}
                                        </Badge>
                                        <Badge variant="outline" class="text-xs">
                                            {{ file.extension.toUpperCase() }}
                                        </Badge>
                                    </div>
                                </div>
                                <Button variant="ghost" size="sm" @click="removeFile(file.id)" class="flex-shrink-0">
                                    <X class="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div class="flex items-center justify-between pt-4 border-t">
                        <div class="text-sm text-neutral-500">
                            {{ uploadedFiles.length }} fichier(s) sélectionné(s)
                        </div>
                        <div class="flex gap-2">
                            <Button variant="outline" @click="dialogOpen = false">
                                Annuler
                            </Button>
                            <Button @click="uploadFiles" :disabled="uploadedFiles.length === 0">
                                <Upload class="h-4 w-4 mr-2" />
                                Envoyer {{ uploadedFiles.length }} fichier(s)
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </DialogContent>
    </Dialog>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/common/components/ui/tabs'
import { bus, useBus } from '@/common/composables/bus'

import { Check, FileText, Image, Trash2, Upload, X } from 'lucide-vue-next'
import { computed, reactive, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const dialogOpen = ref(false)
const isDragOver = ref(false)
const fileInput = ref(null)
const uploadedFiles = reactive([])
const activeTab = ref('upload')
const showExistingPictures = ref(false)
const loadingGallery = ref(false)
const existingPictures = reactive([])
let fileIdCounter = 0

const selectedPicturesCount = computed(() => {
    return existingPictures.filter(p => p.selected).length
})

const triggerFileInput = () => {
    fileInput.value?.click()
}

const handleDragOver = (e) => {
    isDragOver.value = true
}

const handleDragLeave = (e) => {
    isDragOver.value = false
}

const handleDrop = (e) => {
    isDragOver.value = false
    const files = Array.from(e.dataTransfer.files)
    processFiles(files)
}

const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    processFiles(files)
    e.target.value = '' // Reset input
}

const processFiles = (files) => {
    files.forEach(file => {
        if (file.size > 10 * 1024 * 1024) { // 10MB limit
            toast.error(`Le fichier ${file.name} est trop volumineux (max 10MB)`)
            return
        }

        const extension = file.name.split('.').pop().toLowerCase()
        const isImage = file.type.startsWith('image/')

        const fileObj = {
            id: ++fileIdCounter,
            file: file,
            name: file.name,
            size: file.size,
            type: isImage ? 'image' : 'document',
            extension: extension,
            preview: null
        }

        uploadedFiles.push(fileObj)
        
        if (isImage) {
            const reader = new FileReader()
            reader.onload = (e) => {
                const index = uploadedFiles.findIndex(f => f.id === fileObj.id)
                if (index > -1) {
                    uploadedFiles[index].preview = e.target.result
                }
            }
            reader.readAsDataURL(file)
        }
    })
}

const removeFile = (fileId) => {
    const index = uploadedFiles.findIndex(f => f.id === fileId)
    if (index > -1) {
        uploadedFiles.splice(index, 1)
    }
}

const clearFiles = () => {
    uploadedFiles.length = 0
}

const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const loadExistingPictures = async () => {
    loadingGallery.value = true
    try {
        const demoPictures = [
            {
                id: 'baignoire_1',
                name: 'Baignoire 1',
                url: '/pictures/baignoire_1.jpg',
                selected: false
            },
            {
                id: 'baignoire_2',
                name: 'Baignoire 2',
                url: '/pictures/baignoire_2.png',
                selected: false
            },
            {
                id: 'robinet_1',
                name: 'Robinet 1',
                url: '/pictures/robinet_1.jpg',
                selected: false
            },
            {
                id: 'robinet_2',
                name: 'Robinet 2',
                url: '/pictures/robinet_2.jpg',
                selected: false
            },
            {
                id: 'robinet_3',
                name: 'Robinet 3',
                url: '/pictures/robinet_3.jpg',
                selected: false
            }
        ]

        existingPictures.length = 0
        demoPictures.forEach(picture => {
            existingPictures.push(picture)
        })
    } catch (error) {
        console.error('Erreur lors du chargement des photos:', error)
        toast.error('Erreur lors du chargement des photos')
    } finally {
        loadingGallery.value = false
    }
}

const togglePictureSelection = (picture) => {
    picture.selected = !picture.selected
}

const uploadFiles = async () => {
    try {
        if (activeTab.value === 'upload') {
            toast.success(`${uploadedFiles.length} fichier(s) envoyé(s) avec succès`)
        } else {
            const selectedPictures = existingPictures.filter(p => p.selected)
            toast.success(`${selectedPictures.length} photo(s) sélectionnée(s) avec succès`)
        }
        dialogOpen.value = false
        clearFiles()
        // Reset selected pictures
        existingPictures.forEach(p => p.selected = false)
    } catch (error) {
        console.error('Erreur lors de l\'upload:', error)
        toast.error('Erreur lors de l\'envoi des fichiers')
    }
}

const handleTabChange = (newTab) => {
    if (uploadedFiles.length > 0 && newTab === 'gallery') {
        if (confirm('Vous avez des fichiers sélectionnés. Les changer de tab supprimera ces fichiers. Continuer ?')) {
            clearFiles()
            activeTab.value = newTab
        }
    } else {
        activeTab.value = newTab
    }
}



useBus(bus, 'open-attach-file-dialog', (event) => {
    console.log('Received event:', event)
    const data = event.detail || event
    console.log('Extracted data:', data)
    showExistingPictures.value = data?.attachExistingPicture || false
    console.log('showExistingPictures:', showExistingPictures.value)
    dialogOpen.value = true
    if (showExistingPictures.value) {
        loadExistingPictures()
    }
})

useBus(bus, 'close-attach-file-dialog', () => {
    dialogOpen.value = false
})

watch(activeTab, handleTabChange)
</script>
