<template>
    <div class="h-full flex flex-col bg-neutral-50">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <Button variant="outline" @click="$router.go(-1)" class="h-13 w-13">
                        <ArrowLeft :size="20" />
                    </Button>
                    <div class="flex flex-col gap-1">
                        <div class="flex items-center space-x-3">
                            <h1 class="text-xl text-neutral-900 font-mono">#TR42K8</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge class="bg-green-100 text-green-800">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                Planifié
                            </Badge>
                            <Badge variant="outline">
                                <Folder class="h-4 w-4" />
                                Intervention simple
                            </Badge>
                            <Badge variant="outline">
                                <Calendar class="h-4 w-4" />
                                20 Oct 2024 - 10:00
                            </Badge>
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <MessageSquare class="h-4 w-4" />
                        Communiquer
                    </Button>
                    <Button variant="outline">
                        <FileText class="h-4 w-4" />
                        Associer devis
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Ajouter une action
                        <ChevronDown class="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div class="flex-1 p-6 overflow-y-auto">
                <div class="bg-white rounded-lg border">
                    <Tabs class="border-b p-4 py-3">
                        <TabsList>
                            <TabsTrigger value="historique">Historique</TabsTrigger>
                            <TabsTrigger value="details">Opérations</TabsTrigger>
                            <TabsTrigger value="stock">Pièces détachées</TabsTrigger>
                            <TabsTrigger value="reports">Rapports</TabsTrigger>
                            <TabsTrigger value="questionnaire">Questionnaire satisfaction</TabsTrigger>
                        </TabsList>
                    </Tabs>

                    <div class="p-4">
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-lg font-semibold text-neutral-900">Historique</h2>
                            <div class="flex items-center space-x-2">
                                <Button variant="outline">
                                    <File class="h-4 w-4" />
                                    Ajouter une pièce jointe
                                </Button>
                                <Button variant="outline">
                                    <Plus class="h-4 w-4" />
                                    Ajouter une note
                                </Button>
                            </div>
                        </div>


                        <div class="space-y-6">
                            <div class="relative">
                                <div class="absolute left-4 top-8 -bottom-10 w-px bg-neutral-200"></div>

                                <div class="flex items-start space-x-4">
                                    <div
                                        class="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                                        <StickyNote class="h-4 w-4 text-white" />
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <div class="rounded-lg p-4 border">
                                            <div class="flex items-center justify-between mb-2">
                                                <div class="flex items-center space-x-2">
                                                    <h3>Note interne de</h3>
                                                    <span class="font-medium">Marc Dupont</span>
                                                </div>
                                                <span class="text-xs flex items-center text-neutral-500">
                                                    <Calendar class="h-3 w-3 mr-2" />
                                                    Lun, 27 Oct 2022 - 12:03
                                                </span>
                                            </div>

                                            <p class="text-sm text-neutral-600">La cliente sera présente chez elle
                                                entre 10h et 12h, attention à ne pas déranger les enfants</p>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="relative">
                                <div class="absolute left-4 top-8 -bottom-10 w-px bg-neutral-200"></div>

                                <div class="flex items-start space-x-4">
                                    <div
                                        class="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                                        <CalendarCheck class="h-4 w-4 text-white" />
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <div class="rounded-lg p-4 border">
                                            <div class="flex items-center justify-between mb-2">
                                                <h3 class="font-medium text-neutral-900">Intervention planifiée</h3>
                                                <span class="text-xs flex items-center text-neutral-500">
                                                    <Calendar class="h-3 w-3 mr-2" />
                                                    Lun, 27 Oct 2022 - 12:03
                                                </span>
                                            </div>
                                            <p class="text-sm text-neutral-600 mb-3">{{ activityDescription }}</p>

                                            <div class="grid grid-cols-2 gap-4 text-sm">
                                                <div>
                                                    <span class="text-neutral-500">Référence intervention</span>
                                                    <p class="font-mono">{{ jobNumber }}</p>
                                                </div>
                                                <div>
                                                    <span class="text-neutral-500">Quand</span>
                                                    <p>{{ scheduleDate }} {{ scheduleTime }}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="relative">
                                <div class="flex items-start space-x-4">
                                    <div
                                        class="w-8 h-8 bg-primary rounded-full flex items-center justify-center flex-shrink-0">
                                        <Mail class="h-4 w-4 text-white" />
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <div class="bg-white border rounded-lg p-4">
                                            <div class="flex items-center justify-between mb-2">
                                                <div class="flex items-center space-x-2">
                                                    <h3>Email envoyé depuis</h3>
                                                    <span class="font-medium">{{ senderName }}</span>
                                                </div>
                                                <span class="text-xs flex items-center text-neutral-500">
                                                    <Calendar class="h-4 w-4 mr-1" />
                                                    {{ emailDate }}
                                                </span>
                                            </div>

                                            <div class="mb-3">
                                                <p class="text-sm text-neutral-700"><strong>Pour :</strong> {{
                                                    recipientName }}</p>
                                                <p class="text-sm text-neutral-700"><strong>Sujet :</strong> {{
                                                    emailSubject }}</p>
                                            </div>

                                            <div class="text-sm text-neutral-600 mb-4">
                                                <p>{{ emailContent }}</p>
                                            </div>

                                            <div class="flex items-center space-x-4">
                                                <div class="flex items-center space-x-2">
                                                    <FileText class="h-4 w-4 text-neutral-500" />
                                                    <span class="text-sm text-neutral-700">{{ attachmentName }}</span>
                                                    <span class="text-xs text-neutral-500">{{ attachmentSize }}</span>
                                                </div>
                                                <div class="flex items-center space-x-2">
                                                    <Image class="h-4 w-4 text-neutral-500" />
                                                    <span class="text-sm text-neutral-700">{{ imageName }}</span>
                                                    <span class="text-xs text-neutral-500">{{ imageSize }}</span>
                                                </div>
                                                <div class="flex items-center space-x-2">
                                                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
                                                        <Check class="h-3 w-3 inline mr-1" />
                                                        Ouvert
                                                    </span>
                                                </div>
                                            </div>

                                            <div class="mt-3 text-xs text-neutral-500">
                                                <p><strong>De :</strong> {{ senderName }}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="mt-6 text-center">
                            <Button variant="outline">
                                Lire plus
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="w-140 bg-white border-l p-6 overflow-y-auto">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-neutral-900">Détails de l'intervention</h3>
                        <Button
                            class="bg-green-100 text-green-800 hover:bg-green-200 hover:text-green-900 cursor-pointer">
                            <Circle class="fill-current" style="height: 6px; width: 6px;" />
                            Planifié
                            <ChevronDown class="h-4 w-4" />
                        </Button>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <h4 class="text-sm font-medium text-neutral-700">Référence intervention</h4>
                            <p class="text-xl font-mono text-neutral-900">{{ jobNumber }}</p>
                        </div>

                        <div class="bg-accent rounded-lg p-3">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-sm font-medium text-neutral-700">Démarrage prévu</span>
                                <span class="text-sm text-neutral-900">{{ startDate }}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-sm font-medium text-neutral-700">À terminer</span>
                                <div class="text-sm">
                                    <span class="text-neutral-900">{{ endDate }}</span>
                                    <span class="text-neutral-600 ml-2">{{ duration }}</span>
                                </div>
                            </div>
                        </div>


                        <Card class="p-4 gap-0 items-start relative">
                            <Button variant="outline" class="absolute top-3 right-3 h-8 w-8 rounded-full" size="icon">
                                <Edit class="h-3 w-3" />
                            </Button>

                            <div class="flex items-center gap-1 mb-2">
                                <ScrollText class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Description de l'intervention</h4>
                            </div>
                            <p class="text-sm text-neutral-600">{{ jobDescription }}</p>

                        </Card>

                        <Card class="p-4 gap-0 items-start relative">
                            <Button variant="outline" class="absolute top-3 right-3 h-8 w-8 rounded-full" size="icon">
                                <Edit class="h-3 w-3" />
                            </Button>
                            <div class="flex items-center gap-1 mb-2">
                                <MapPinned class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Adresse d'intervention</h4>
                            </div>
                            <p class="text-sm text-neutral-600">123 Rue de la Paix, 75000 Paris</p>
                        </Card>

                        <Card
                            class="p-4 gap-0 border-dashed flex items-center justify-center cursor-pointer hover:bg-neutral-50">
                            <UserPlus class="h-10 w-10 mb-3 text-neutral-500" :stroke-width="1.2" />
                            <p class="text-sm text-neutral-500">Assigner un technicien</p>
                        </Card>

                        <Separator />

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Client commanditaire</Label>
                            <Select>
                                <SelectTrigger class="w-full col-span-2">
                                    <SelectValue placeholder="Sélectionner un client" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="team1">Client 1</SelectItem>
                                    <SelectItem value="team2">Client 2</SelectItem>
                                    <SelectItem value="team3">Client 3</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Type d'intervention</Label>
                            <Select>
                                <SelectTrigger class="w-full col-span-2">
                                    <SelectValue placeholder="Sélectionner un type d'intervention" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="team1">Dépannage simple</SelectItem>
                                    <SelectItem value="team2">Dépannage urgent</SelectItem>
                                    <SelectItem value="team3">États des lieux</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Référence client</Label>
                            <Input class="col-span-2" placeholder="Précisez la référence client" />
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import Card from '@/common/components/ui/card/Card.vue'
import Input from '@/common/components/ui/input/Input.vue'
import Select from '@/common/components/ui/select/Select.vue'
import SelectContent from '@/common/components/ui/select/SelectContent.vue'
import SelectItem from '@/common/components/ui/select/SelectItem.vue'
import SelectTrigger from '@/common/components/ui/select/SelectTrigger.vue'
import SelectValue from '@/common/components/ui/select/SelectValue.vue'
import Separator from '@/common/components/ui/separator/Separator.vue'
import Tabs from '@/common/components/ui/tabs/Tabs.vue'
import TabsList from '@/common/components/ui/tabs/TabsList.vue'
import TabsTrigger from '@/common/components/ui/tabs/TabsTrigger.vue'
import {
    ArrowLeft,
    Calendar,
    CalendarCheck,
    Check,
    ChevronDown,
    Circle,
    Edit,
    File,
    FileText,
    Folder,
    Image,
    Mail,
    MapPinned,
    MessageSquare,
    Plus,
    ScrollText,
    StickyNote,
    UserPlus
} from 'lucide-vue-next'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const activityDescription = ref('L\'intervention a été planifiée par Marc Dupont')
const jobNumber = ref('#TR42K8')
const scheduleDate = ref('Mar 22 Oct 2024')
const scheduleTime = ref('7:15pm - 7:45pm')

const senderName = ref('Intervention Service Plus')
const emailDate = ref('Lun, 27 Oct 2022 - 12:03 - par John Doe')
const recipientName = ref('John Smith')
const emailSubject = ref('Suivi des documents joints')
const emailContent = ref('Salut John, Veuillez consulter les documents mis à jour associés à l\'estimation. Veuillez nous faire savoir si ceux-ci sont acceptables et nous obtiendrons un devis envoyé. Veuillez également noter que ces matériaux ne seront pas disponibles pendant longtemps car il faut du temps pour les approvisionner.')
const attachmentName = ref('Estimation v1-1.doc')
const attachmentSize = ref('2.3 MB')
const imageName = ref('localisation.jpg')
const imageSize = ref('2.3 MB')

const startDate = ref('20 Oct 2024 - 10:00')
const endDate = ref('25 Oct 2024 - 10:00')
const duration = ref('10j : 3h : 50m : 2s')
const jobDescription = ref('Remettre en place le robinet qui n\'a pas tenu')
</script>