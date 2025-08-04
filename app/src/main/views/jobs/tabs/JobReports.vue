<template>
    <div class="space-y-4">
        <div class="flex items-center justify-between">
            <h2 class="text-lg font-semibold text-neutral-900">Rapports d'intervention</h2>
            <Button @click="openCreateDialog">
                <Plus class="h-4 w-4" />
                Nouveau rapport
            </Button>
        </div>

        <div v-if="loading" class="flex items-center justify-center py-8">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
        </div>

        <div v-else-if="reports.length === 0" class="text-center py-8 text-neutral-500">
            <FileText class="h-12 w-12 mx-auto mb-4 text-neutral-300" />
            <p class="text-sm">Aucun rapport créé pour cette intervention</p>
            <p class="text-xs mt-1">Créez votre premier rapport pour documenter cette intervention</p>
        </div>

        <div v-else class="space-y-3">
            <Card v-for="report in reports" :key="report.id" class="bg-white border rounded-lg !py-0 gap-0">
                <CardContent class="p-4">
                    <h3 class="font-medium text-neutral-900 mb-1">{{ report.name }}</h3>
                    <p class="text-sm text-neutral-500 line-clamp-2">{{ report.content }}</p>

                    <div class="flex mt-3 gap-2 justify-between">
                        <div class="flex gap-2">
                            <Badge v-if="report.include_diagnostics" variant="outline" class="text-xs">
                                <Check class="h-4 w-4" />
                                Diagnostics
                            </Badge>
                            <Badge v-if="report.include_tasks" variant="outline" class="text-xs">
                                <Check class="h-4 w-4" />
                                Tâches
                            </Badge>
                        </div>
                        <div class="flex gap-2 text-xs text-neutral-500">
                            <span>Créé le {{ formatDate(report.created_at) }}</span>
                            <span>par {{ report.created_by.first_name }} {{ report.created_by.name }}</span>
                        </div>
                    </div>
                </CardContent>
                <CardFooter class="!p-4 !py-2 border-t flex gap-2 justify-between bg-neutral-50">
                    <div class="flex gap-2">
                        <Button variant="outline" class="p-0" size="sm" @click="generatePDF(report)">
                            <FileText class="h-4 w-4" />
                            Générer PDF
                        </Button>
                        <Button variant="outline" class="p-0" size="sm" @click="openAttachFileDialog">
                            <Camera class="h-4 w-4" />
                            Joindre photos
                        </Button>
                        <Button variant="outline" class="p-0" size="sm" @click="openEditDialog(report)">
                            <Pen class="h-4 w-4" />
                            Editer
                        </Button>
                    </div>
                    <Button @click="handleDeleteReport(report)" class="w-9" variant="outline" size="sm">
                        <Trash2 class="h-4 w-4" />
                    </Button>
                </CardFooter>
            </Card>
        </div>

        <Dialog v-model:open="dialogOpen" :modal="true">
            <DialogContent class="sm:max-w-[600px]">
                <DialogHeader>
                    <DialogTitle>{{ editingReport ? 'Modifier le rapport' : 'Nouveau rapport' }}</DialogTitle>
                    <DialogDescription>
                        Créez un rapport détaillé de cette intervention
                    </DialogDescription>
                </DialogHeader>

                <form @submit.prevent="saveReport" class="space-y-4">
                    <div class="space-y-2">
                        <Label for="name">Nom du rapport</Label>
                        <Input id="name" v-model="form.name" placeholder="Ex: Rapport d'intervention du 15/01/2024" />
                    </div>

                    <div class="space-y-2">
                        <Label for="content">Contenu</Label>
                        <Textarea id="content" v-model="form.content"
                            placeholder="Décrivez les travaux effectués, les observations, les recommandations..."
                            rows="4" />
                    </div>

                    <Collapsible>
                        <CollapsibleTrigger
                            class="flex items-center justify-between w-full px-3 py-2 text-sm font-medium text-neutral-700 cursor-pointer border rounded-md hover:bg-neutral-100 transition-colors">
                            <div class="flex items-center gap-2">
                                <Settings2 class="h-4 w-4" />
                                <span>Afficher les options du rapport</span>
                            </div>
                            <ChevronDown class="h-4 w-4 transition-transform" />
                        </CollapsibleTrigger>
                        <CollapsibleContent class="space-y-4 py-3 border-b">
                            <div class="flex items-center justify-between">
                                <Label for="include_diagnostics" class="text-sm font-medium">Inclure les
                                    diagnostics</Label>
                                <Switch :model-value="form.include_diagnostics"
                                    @update:model-value="form.include_diagnostics = $event" />
                            </div>
                            <div class="flex items-center justify-between">
                                <Label for="include_tasks" class="text-sm font-medium">Inclure les tâches</Label>
                                <Switch :model-value="form.include_tasks"
                                    @update:model-value="form.include_tasks = $event" />
                            </div>
                        </CollapsibleContent>
                    </Collapsible>

                    <div class="grid grid-cols-2 gap-4 mt-6">
                        <div class="space-y-3">
                            <Label>Signature client</Label>
                            <div class="border-2 border-dashed border-neutral-300 rounded-lg p-4 text-center cursor-pointer hover:border-primary h-30 flex flex-col items-center justify-center"
                                @click="openSignatureDialog('customer')">
                                <div v-if="form.customer_signature" class="w-full h-full">
                                    <img :src="form.customer_signature" alt="Signature client"
                                        class="w-full h-full object-contain" />
                                </div>
                                <div v-else class="text-sm text-neutral-500">
                                    <Pen class="h-8 w-8 mx-auto mb-2" />
                                    Cliquer pour signer
                                </div>
                            </div>
                        </div>
                        <div class="space-y-3">
                            <Label>Signature opérateur</Label>
                            <div class="border-2 border-dashed border-neutral-300 rounded-lg p-4 text-center cursor-pointer hover:border-primary h-30 flex flex-col items-center justify-center"
                                @click="openSignatureDialog('operator')">
                                <div v-if="form.operator_signature" class="w-full h-full">
                                    <img :src="form.operator_signature" alt="Signature opérateur"
                                        class="w-full h-full object-contain" />
                                </div>
                                <div v-else class="text-sm text-neutral-500">
                                    <Pen class="h-8 w-8 mx-auto mb-2" />
                                    Cliquer pour signer
                                </div>
                            </div>
                        </div>
                    </div>

                    <DialogFooter>
                        <Button type="button" variant="outline" @click="dialogOpen = false">
                            Annuler
                        </Button>
                        <Button type="submit" :disabled="saving">
                            <div v-if="saving" class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2">
                            </div>
                            <SaveIcon class="h-4 w-4" />
                            {{ editingReport ? 'Modifier' : 'Enregistrer' }}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>

        <Dialog v-model:open="signatureDialogOpen" :modal="true">
            <DialogContent class="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Signature {{ currentSignatureType === 'customer' ? 'client' : 'opérateur' }}
                    </DialogTitle>
                </DialogHeader>
                <div class="space-y-4">
                    <div class="border rounded-lg p-4 bg-neutral-50">
                        <canvas ref="signatureCanvas" class="w-full h-48 border bg-white cursor-crosshair"></canvas>
                    </div>
                    <div class="flex justify-between">
                        <Button type="button" variant="outline" @click="clearSignature">
                            Effacer
                        </Button>
                        <div class="space-x-2">
                            <Button type="button" variant="outline" @click="signatureDialogOpen = false">
                                Annuler
                            </Button>
                            <Button type="button" @click="saveSignature">
                                Valider
                            </Button>
                        </div>
                    </div>
                </div>
            </DialogContent>
        </Dialog>
    </div>
</template>

<script setup>
import { Badge } from '@/common/components/ui/badge'
import { Button } from '@/common/components/ui/button'
import Card from '@/common/components/ui/card/Card.vue'
import CardContent from '@/common/components/ui/card/CardContent.vue'
import CardFooter from '@/common/components/ui/card/CardFooter.vue'
import Collapsible from '@/common/components/ui/collapsible/Collapsible.vue'
import CollapsibleContent from '@/common/components/ui/collapsible/CollapsibleContent.vue'
import CollapsibleTrigger from '@/common/components/ui/collapsible/CollapsibleTrigger.vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { Input } from '@/common/components/ui/input'
import { Label } from '@/common/components/ui/label'
import Switch from '@/common/components/ui/switch/Switch.vue'
import { Textarea } from '@/common/components/ui/textarea'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { Camera, Check, ChevronDown, FileText, Pen, Plus, SaveIcon, Settings2, Trash2 } from 'lucide-vue-next'
import { nextTick, onMounted, reactive, ref, watch } from 'vue'
import { toast } from 'vue-sonner'

const props = defineProps({
    jobId: {
        type: Number,
        required: true
    }
})

const fetcher = useFetcher()

const loading = ref(false)
const saving = ref(false)
const reports = ref([])
const dialogOpen = ref(false)
const signatureDialogOpen = ref(false)
const editingReport = ref(null)
const currentSignatureType = ref('customer')
const signatureCanvas = ref(null)
const signatureContext = ref(null)
const selectedReportForDelete = ref(null)

const form = reactive({
    name: '',
    content: '',
    include_diagnostics: true,
    include_tasks: true,
    customer_signature: null,
    operator_signature: null
})

const loadReports = async () => {
    loading.value = true
    try {
        const response = await fetcher.get(`/job-reports?job=${props.jobId}`)
        reports.value = response.data
    } catch (error) {
        console.error('Erreur lors du chargement des rapports:', error)
    } finally {
        loading.value = false
    }
}

const openCreateDialog = () => {
    editingReport.value = null
    resetForm()

    const today = new Date()
    const day = String(today.getDate()).padStart(2, '0')
    const month = String(today.getMonth() + 1).padStart(2, '0')
    const year = today.getFullYear()
    const formattedDate = `${day}/${month}/${year}`

    form.name = `Rapport d'intervention du ${formattedDate}`
    dialogOpen.value = true
}

const openEditDialog = (report) => {
    editingReport.value = report
    form.name = report.name
    form.content = report.content
    form.include_diagnostics = report.include_diagnostics
    form.include_tasks = report.include_tasks
    form.customer_signature = report.customer_signature
    form.operator_signature = report.operator_signature
    dialogOpen.value = true
}

const resetForm = () => {
    form.name = ''
    form.content = ''
    form.include_diagnostics = true
    form.include_tasks = true
    form.customer_signature = null
    form.operator_signature = null
}

const saveReport = async () => {
    if (!form.name.trim() || !form.content.trim()) {
        return
    }

    saving.value = true
    try {
        const data = {
            ...form,
            job: props.jobId
        }

        if (editingReport.value) {
            await fetcher.put(`/job-reports/${editingReport.value.id}`, data)
        } else {
            await fetcher.post('/job-reports', data)
        }

        dialogOpen.value = false
        await loadReports()
        bus.trigger('job-report:saved')
    } catch (error) {
        console.error('Erreur lors de la sauvegarde du rapport:', error)
    } finally {
        saving.value = false
    }
}

const openSignatureDialog = (type) => {
    currentSignatureType.value = type
    signatureDialogOpen.value = true
    nextTick(() => {
        if (signatureCanvas.value) {
            initSignatureCanvas()
        }
    })
}

const initSignatureCanvas = () => {
    const canvas = signatureCanvas.value
    if (!canvas) {
        console.warn('Canvas not found')
        return
    }

    const ctx = canvas.getContext('2d')
    if (!ctx) {
        console.warn('Could not get 2D context')
        return
    }

    signatureContext.value = ctx

    const rect = canvas.getBoundingClientRect()
    if (rect.width === 0 || rect.height === 0) {
        console.warn('Canvas has zero dimensions')
        return
    }

    canvas.width = rect.width
    canvas.height = rect.height

    ctx.strokeStyle = '#000'
    ctx.lineWidth = 2
    ctx.lineCap = 'round'

    let isDrawing = false
    let lastX = 0
    let lastY = 0

    canvas.addEventListener('mousedown', startDrawing)
    canvas.addEventListener('mousemove', draw)
    canvas.addEventListener('mouseup', stopDrawing)
    canvas.addEventListener('mouseout', stopDrawing)

    function startDrawing(e) {
        isDrawing = true
        const rect = canvas.getBoundingClientRect()
        lastX = e.clientX - rect.left
        lastY = e.clientY - rect.top
    }

    function draw(e) {
        if (!isDrawing) return
        const rect = canvas.getBoundingClientRect()
        const x = e.clientX - rect.left
        const y = e.clientY - rect.top

        ctx.beginPath()
        ctx.moveTo(lastX, lastY)
        ctx.lineTo(x, y)
        ctx.stroke()

        lastX = x
        lastY = y
    }

    function stopDrawing() {
        isDrawing = false
    }
}

const clearSignature = () => {
    if (signatureContext.value && signatureCanvas.value) {
        signatureContext.value.clearRect(0, 0, signatureCanvas.value.width, signatureCanvas.value.height)
    }
}

const saveSignature = () => {
    if (signatureCanvas.value) {
        const signatureData = signatureCanvas.value.toDataURL()
        if (currentSignatureType.value === 'customer') {
            form.customer_signature = signatureData
        } else {
            form.operator_signature = signatureData
        }
        signatureDialogOpen.value = false
    }
}

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const openAttachFileDialog = () => {
    bus.trigger('open-attach-file-dialog', {
        jobId: props.jobId,
        attachExistingPicture: true
    })
}

const handleDeleteReport = (report) => {
    bus.trigger('confirm-delete', {
        title: 'Supprimer le rapport',
        message: 'Êtes-vous sûr de vouloir supprimer ce rapport ?',
        itemName: report.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-job-report:confirmed'
    })
    selectedReportForDelete.value = report
}

const deleteReport = async () => {
    if (!selectedReportForDelete.value) return

    try {
        await fetcher.delete(`/job-reports/${selectedReportForDelete.value.id}`)
        toast.success('Rapport supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        await loadReports()
        selectedReportForDelete.value = null
    } catch (error) {
        console.error('Erreur lors de la suppression du rapport:', error)
        toast.error('Erreur lors de la suppression du rapport')
        bus.trigger('confirm-delete-dialog:close')
    }
}

onMounted(() => {
    loadReports()
})

watch(() => props.jobId, () => {
    if (props.jobId) {
        loadReports()
    }
})

useBus(bus, 'confirm-delete-job-report:confirmed', () => {
    deleteReport()
})

const generatePDF = async (report) => {
    try {
        const response = await fetcher.get(`/job-reports/${report.id}/pdf`)

        const contentType = response.headers.get('content-type')

        if (contentType && contentType.includes('text/html')) {
            const htmlContent = await response.text()
            const newWindow = window.open('', '_blank')
            newWindow.document.write(htmlContent)
            newWindow.document.close()
            toast.success('Aperçu HTML ouvert dans un nouvel onglet')
        } else {
            const blob = await response.blob()
            const url = URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = url
            link.download = `rapport_intervention_${report.job?.reference || report.id}.pdf`
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            URL.revokeObjectURL(url)
            toast.success('PDF généré avec succès')
        }
    } catch (error) {
        console.error('Erreur lors de la génération du PDF:', error)
        toast.error('Erreur lors de la génération du PDF')
    }
}


</script>
