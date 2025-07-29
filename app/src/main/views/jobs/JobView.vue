<template>
    <div v-if="loading" class="h-full flex items-center justify-center">
        <div class="text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
            <p class="text-neutral-600">Chargement de l'intervention...</p>
        </div>
    </div>

    <div v-else class="h-full flex flex-col bg-neutral-100">
        <div class="bg-white border-b">
            <div class="px-6 py-4 flex items-center justify-between">
                <div class="flex items-center space-x-4">
                    <Button v-if="!inDialog" variant="outline" @click="$router.go(-1)" class="h-9 w-9">
                        <ArrowLeft :size="20" />
                    </Button>
                    <div class="flex flex-col gap-1">
                        <div class="flex items-center space-x-3">
                            <h1 class="text-xl text-neutral-900 font-mono">{{ job?.reference || 'Chargement...' }}</h1>
                        </div>
                        <div class="flex gap-2">
                            <Badge v-if="job?.status" class="bg-green-100 text-green-800">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                {{ job.status.name }}
                            </Badge>
                            <Badge v-if="!job?.operator" class="bg-yellow-50 text-yellow-700">
                                <User class="h-4 w-4" />
                                À assigner
                            </Badge>
                            <Badge v-if="job?.category" variant="outline">
                                <Folder class="h-4 w-4" />
                                {{ job.category.name }}
                            </Badge>
                            <Badge v-if="job?.scheduled_start" variant="outline">
                                <Calendar class="h-4 w-4" />
                                {{ formatDate(job.scheduled_start) }}
                            </Badge>
                        </div>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <Button variant="outline">
                        <CalendarArrowUp class="h-4 w-4" />
                        Replanifier
                    </Button>
                    <Button variant="outline">
                        <UserPlus class="h-4 w-4" />
                        Assigner technicien
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Action
                        <ChevronDown class="h-4 w-4" />
                    </Button>
                </div>
            </div>
        </div>

        <div class="flex-1 flex overflow-hidden">
            <div :class="inDialog ? 'flex-1 overflow-y-auto p-6 bg-accent' : 'flex-1 p-6 overflow-y-auto'">
                <Card class="mb-6 py-0">
                    <CardContent class="px-5 py-4">
                        <div class="flex items-start justify-between mb-4">
                            <div class="flex items-start space-x-2">
                                <ScanSearch class="h-8 w-8 text-neutral-400 mt-2 me-3" :stroke-width="1.2" />
                                <div class="flex flex-col">
                                    <h1 class="text-2xl font-semibold">{{ job?.name || 'Chargement...' }}</h1>
                                    <p class="text-neutral-600">{{ getClientName() }} • {{
                                        getClientAddress().split(',')[0] }}
                                    </p>
                                </div>
                            </div>
                            <Badge v-if="job?.status" class="bg-green-100 text-green-800">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                {{ job.status.name }}
                            </Badge>
                        </div>

                        <div class="grid grid-cols-3 gap-4 mb-4 ps-11">
                            <div class="flex items-start space-x-3">
                                <Calendar class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ job?.scheduled_start ?
                                        formatDate(job.scheduled_start) : 'Non planifié' }}</p>
                                    <p class="text-xs text-neutral-500">Début prévu</p>
                                </div>
                            </div>
                            <div class="flex items-start space-x-3">
                                <Clock class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900">{{ getDuration() }}</p>
                                    <p class="text-xs text-neutral-500">Durée prévue</p>
                                </div>
                            </div>
                        </div>

                        <div class="mt-4 pt-4 border-t border-dashed ps-11">
                            <div class="flex items-center justify-between">
                                <div class="flex items-center space-x-4">
                                    <div class="flex items-center space-x-2" v-if="job?.site">
                                        <MapPin class="h-4 w-4 text-neutral-500" />
                                        <span class="text-sm text-neutral-600">{{ getClientAddress().split(',')[1] }},
                                            {{
                                                getClientAddress().split(',')[2] }}</span>
                                    </div>
                                    <Badge class="flex items-center bg-yellow-100 text-yellow-900" v-else>
                                        <MapPin class="h-4 w-4" />
                                        <span class="text-sm">Adresse non définie</span>
                                    </Badge>

                                    <Badge v-if="job?.priority" class="flex items-center space-x-1"
                                        :class="getPriorityConfig(job.priority).bgColor + ' ' + getPriorityConfig(job.priority).color">
                                        <AlertTriangle class="h-4 w-4" />
                                        <span class="text-sm">{{ getPriorityConfig(job.priority).label }}</span>
                                    </Badge>
                                </div>
                                <div class="flex gap-2">
                                    <DropdownMenu>
                                        <DropdownMenuTrigger asChild>
                                            <Button variant="outline">
                                                <AlertTriangle class="h-4 w-4 text-orange-500" />
                                                Signaler intervention
                                                <ChevronDown class="h-4 w-4" />
                                            </Button>
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent align="end">
                                            <DropdownMenuItem>
                                                <UserRoundX class="h-4 w-4 text-orange-500" />
                                                Absence contact
                                            </DropdownMenuItem>
                                            <DropdownMenuItem>
                                                <ShieldAlert class="h-4 w-4 text-orange-500" />
                                                Intervention impossible
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>

                                    <Button>
                                        <Play class="h-3 w-3 fill-current" />
                                        Démarrer
                                    </Button>
                                </div>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <div class="bg-white rounded-lg border">
                    <Tabs default-value="historique" class="border-b p-4 py-3">
                        <TabsList>
                            <TabsTrigger value="historique">Historique</TabsTrigger>
                            <TabsTrigger value="operations">Opérations</TabsTrigger>
                            <TabsTrigger value="pieces">Pièces détachées</TabsTrigger>
                            <TabsTrigger value="rapports">Rapports</TabsTrigger>
                            <TabsTrigger value="questionnaire">Questionnaire satisfaction</TabsTrigger>
                        </TabsList>

                        <TabsContent value="historique">

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

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">L'historique des interventions sera bientôt disponible</p>
                                </div>


                                <div class="space-y-6">
                                    <div class="relative">
                                        <div class="absolute left-4 top-8 -bottom-10 w-px bg-neutral-200"></div>

                                        <div class="flex items-start space-x-4">
                                            <div
                                                class="w-8 h-8 bg-secondary text-secondary-foreground rounded-full flex items-center justify-center flex-shrink-0">
                                                <StickyNote class="h-4 w-4" />
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

                                                    <p class="text-sm text-neutral-600">La cliente sera présente chez
                                                        elle
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
                                                        <h3 class="font-medium text-neutral-900">Intervention planifiée
                                                        </h3>
                                                        <span class="text-xs flex items-center text-neutral-500">
                                                            <Calendar class="h-3 w-3 mr-2" />
                                                            Lun, 27 Oct 2022 - 12:03
                                                        </span>
                                                    </div>
                                                    <p class="text-sm text-neutral-600 mb-3">{{ activityDescription }}
                                                    </p>

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
                                                            <span class="text-sm text-neutral-700">{{ attachmentName
                                                            }}</span>
                                                            <span class="text-xs text-neutral-500">{{ attachmentSize
                                                            }}</span>
                                                        </div>
                                                        <div class="flex items-center space-x-2">
                                                            <Image class="h-4 w-4 text-neutral-500" />
                                                            <span class="text-sm text-neutral-700">{{ imageName
                                                            }}</span>
                                                            <span class="text-xs text-neutral-500">{{ imageSize
                                                            }}</span>
                                                        </div>
                                                        <div class="flex items-center space-x-2">
                                                            <span
                                                                class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">
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
                        </TabsContent>

                        <TabsContent value="operations">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Opérations effectuées</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter une opération
                                    </Button>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La gestion des opérations sera bientôt disponible</p>
                                </div>

                                <div class="space-y-4">
                                    <div class="border rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-2">
                                            <span class="font-medium">Diagnostic initial</span>
                                            <span class="text-sm text-neutral-500">Fait le 20/10/2024 à 14:45</span>
                                        </div>
                                        <p class="text-sm text-neutral-600">Inspection du robinet défaillant et
                                            identification de la cause</p>
                                        <div class="mt-3 flex items-center gap-1 text-xs text-neutral-500">
                                            <Badge class="bg-green-100 text-green-800">Effectué</Badge>
                                            <User class="h-3 w-3" />Pierre Martin
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-2">
                                            <span class="font-medium">Démontage robinet</span>
                                            <span class="text-sm text-neutral-500">Fait le 20/10/2024 à 14:45</span>
                                        </div>
                                        <p class="text-sm text-neutral-600 mb-2">Démontage complet du robinet défaillant
                                        </p>
                                        <div class="mt-3 flex items-center gap-1 text-xs text-neutral-500">
                                            <Badge class="bg-green-100 text-green-800">Effectué</Badge>
                                            <User class="h-3 w-3" />Pierre Martin
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-2">
                                            <span class="font-medium">Installation nouveau robinet</span>
                                            <span class="text-sm text-neutral-500">À faire</span>
                                        </div>
                                        <p class="text-sm text-neutral-600 mb-2">Pose et fixation du nouveau robinet</p>
                                        <div class="mt-3 flex items-center gap-1 text-xs text-neutral-500">
                                            <Badge class="bg-blue-100 text-blue-800">À faire</Badge>
                                        </div>
                                    </div>

                                    <div class="border-dashed border-2 rounded-lg p-4 text-center">
                                        <p class="text-sm text-neutral-500 mb-2">Ajouter une nouvelle opération</p>
                                        <Button variant="outline" size="sm">
                                            <Plus class="h-4 w-4" />
                                            Nouvelle opération
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="pieces">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Pièces détachées utilisées</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Ajouter une pièce
                                    </Button>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La gestion des pièces détachées sera bientôt disponible</p>
                                </div>

                                <div class="overflow-x-auto">
                                    <table class="w-full">
                                        <thead class="bg-neutral-50">
                                            <tr>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">
                                                    Référence</th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">
                                                    Désignation</th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">
                                                    Origine</th>
                                                <th
                                                    class="px-4 py-3 text-left text-xs font-medium text-neutral-500 uppercase">
                                                    Qté</th>
                                            </tr>
                                        </thead>
                                        <tbody class="divide-y divide-neutral-200">
                                            <tr>
                                                <td class="px-4 py-3 text-sm font-mono">ROB-001</td>
                                                <td class="px-4 py-3 text-sm">Robinet mitigeur standard</td>
                                                <td class="px-4 py-3 text-sm flex items-center gap-2">
                                                    <LogOut class="h-3 w-3" />Camion Pierre
                                                </td>
                                                <td class="px-4 py-3 text-sm">1</td>
                                            </tr>
                                            <tr>
                                                <td class="px-4 py-3 text-sm font-mono">JT-205</td>
                                                <td class="px-4 py-3 text-sm">Joint téflon rouleau 10m</td>
                                                <td class="px-4 py-3 text-sm flex items-center gap-2">
                                                    <LogOut class="h-3 w-3" />Camion Pierre
                                                </td>
                                                <td class="px-4 py-3 text-sm">1</td>
                                            </tr>
                                            <tr>
                                                <td class="px-4 py-3 text-sm font-mono">VIS-12</td>
                                                <td class="px-4 py-3 text-sm">Vis fixation x4</td>
                                                <td class="px-4 py-3 text-sm flex items-center gap-2">
                                                    <LogOut class="h-3 w-3" />Camion Pierre
                                                </td>
                                                <td class="px-4 py-3 text-sm">1</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                            </div>
                        </TabsContent>

                        <TabsContent value="rapports">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Rapports d'intervention</h2>
                                    <Button>
                                        <Plus class="h-4 w-4" />
                                        Générer un rapport
                                    </Button>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La génération de rapports sera bientôt disponible</p>
                                </div>

                                <div class="space-y-4">
                                    <div class="border rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-3">
                                            <div class="flex items-center space-x-3">
                                                <FileText class="h-8 w-8" />
                                                <div>
                                                    <h3 class="font-medium">Rapport d'intervention</h3>
                                                    <p class="text-sm text-neutral-500">Rapport technique détaillé</p>
                                                </div>
                                            </div>
                                            <div class="flex items-center space-x-2">
                                                <Badge class="bg-green-100 text-green-800">Généré</Badge>
                                                <Button variant="outline" size="sm">
                                                    Télécharger
                                                </Button>
                                            </div>
                                        </div>
                                        <div class="text-sm text-neutral-600">
                                            <p>Généré le 20/10/2024 à 16:30 par Pierre Martin</p>
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-3">
                                            <div class="flex items-center space-x-3">
                                                <FileText class="h-8 w-8" />
                                                <div>
                                                    <h3 class="font-medium">Certificat Qualigaz</h3>
                                                    <p class="text-sm text-neutral-500">Certificat de conformité gaz</p>
                                                </div>
                                            </div>
                                            <div class="flex items-center space-x-2">
                                                <Badge variant="outline">En attente</Badge>
                                                <Button variant="outline" size="sm" disabled>
                                                    Non disponible
                                                </Button>
                                            </div>
                                        </div>
                                        <div class="text-sm text-neutral-600">
                                            <p>Sera généré après validation du contrôle gaz</p>
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <div class="flex items-center justify-between mb-3">
                                            <div class="flex items-center space-x-3">
                                                <FileText class="h-8 w-8" />
                                                <div>
                                                    <h3 class="font-medium">Photos avant/après</h3>
                                                    <p class="text-sm text-neutral-500">Documentation visuelle</p>
                                                </div>
                                            </div>
                                            <div class="flex items-center space-x-2">
                                                <Badge class="bg-green-100 text-green-800">4 photos</Badge>
                                                <Button variant="outline" size="sm">
                                                    Voir
                                                </Button>
                                            </div>
                                        </div>
                                        <div class="text-sm text-neutral-600">
                                            <p>Photos prises le 20/10/2024 à 15:45</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </TabsContent>

                        <TabsContent value="questionnaire">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Questionnaire de satisfaction
                                    </h2>
                                    <Badge class="bg-green-100 text-green-800">Complété</Badge>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">Les questionnaires de satisfaction seront bientôt
                                        disponibles</p>
                                </div>

                                <div class="space-y-6">
                                    <div class="border rounded-lg p-4">
                                        <h3 class="font-medium mb-3">Êtes-vous satisfait de la qualité du travail
                                            effectué ?</h3>
                                        <div class="flex items-center space-x-2">
                                            <Badge class="bg-green-100 text-green-800">Oui</Badge>
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <h3 class="font-medium mb-3">Le plombier a-t-il laissé les lieux propres après
                                            son intervention ?</h3>
                                        <div class="flex items-center space-x-2">
                                            <Badge class="bg-green-100 text-green-800">Oui</Badge>
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <h3 class="font-medium mb-3">La prise de rendez-vous pour votre intervention
                                            a-t-elle était simple ?</h3>
                                        <div class="flex items-center space-x-2">
                                            <Badge class="bg-green-100 text-green-800">Oui</Badge>
                                        </div>
                                    </div>

                                    <div class="border rounded-lg p-4">
                                        <h3 class="font-medium mb-3">Pourriez-vous noter l'intervention dans son global
                                            ?</h3>
                                        <div class="flex items-center space-x-2">
                                            <Badge class="bg-green-100 text-green-800">10/10</Badge>
                                        </div>
                                    </div>

                                    <div class="bg-green-50 border border-green-200 rounded-lg p-4">
                                        <div class="flex items-center space-x-2 mb-2">
                                            <Check class="h-5 w-5 text-green-600" />
                                            <span class="font-medium text-green-800">Questionnaire complété</span>
                                        </div>
                                        <p class="text-sm text-green-700">Répondu par le client le 20/10/2024 à 17:15
                                        </p>
                                        <p class="text-sm text-green-700">Note globale: 10/10 - Très satisfait</p>
                                    </div>
                                </div>
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>

            <div v-if="!inDialog" class="w-140 bg-white border-l p-6 overflow-y-auto">
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
                            <p class="text-xl font-mono text-neutral-900">{{ job?.reference || 'Chargement...' }}</p>
                            <p class="text-xs text-neutral-400">Créé le {{ job?.created_at ? formatDate(job.created_at)
                                : 'Chargement...' }}</p>
                        </div>

                        <div class="bg-neutral-100 border rounded-lg p-3">
                            <div class="flex items-center justify-between mb-2">
                                <span class="text-sm font-medium text-neutral-700">Démarrage prévu</span>
                                <span class="text-sm text-neutral-900">{{ job?.scheduled_start ?
                                    formatDate(job.scheduled_start) : 'Non planifié' }}</span>
                            </div>
                            <div class="flex items-center justify-between">
                                <span class="text-sm font-medium text-neutral-700">À terminer</span>
                                <div class="text-sm">
                                    <span class="text-neutral-900">{{ job?.scheduled_end ? formatDate(job.scheduled_end)
                                        : 'Non planifié' }}</span>
                                    <span class="text-neutral-600 ml-2">{{ getDuration() }}</span>
                                </div>
                            </div>
                        </div>


                        <Card class="p-4 gap-0 items-start relative">
                            <div class="flex absolute top-3 right-3 gap-2">
                                <Button variant="outline" class="h-8 w-8" size="icon">
                                    <Edit class="h-3 w-3" />
                                </Button>
                            </div>

                            <div class="flex items-center gap-1 mb-2">
                                <ScrollText class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Description de l'intervention</h4>
                            </div>
                            <p class="text-sm text-neutral-600">{{ job?.description || 'Aucune description' }}</p>

                        </Card>

                        <Card class="p-4 gap-0 items-start relative">
                            <div class="flex absolute top-3 right-3 gap-2">
                                <Button variant="outline" class="h-8 w-8" size="icon">
                                    <Edit class="h-3 w-3" />
                                </Button>

                                <Button variant="outline" class=" h-8 w-8" size="icon">
                                    <Map />
                                </Button>
                            </div>
                            <div class="flex items-center gap-1 mb-2">
                                <MapPinned class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Site d'intervention</h4>
                            </div>
                            <div class="text-sm text-neutral-600">
                                <p v-if="job?.site?.name">{{ job.site.name }}</p>
                                <p v-if="job?.site?.street">{{ job.site.street }}</p>
                                <p v-if="job?.site?.zip && job?.site?.city">{{ job.site.zip }} {{ job.site.city }}</p>
                                <p v-if="!job?.site">Aucun site défini</p>
                            </div>
                        </Card>

                        <Card
                            class="p-4 gap-0 border-dashed flex items-center justify-center cursor-pointer hover:bg-neutral-50">
                            <UserPlus class="h-10 w-10 mb-3 text-neutral-500" :stroke-width="1.2" />
                            <p class="text-sm text-neutral-500">Assigner un technicien</p>
                        </Card>

                        <Separator />

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Client commanditaire</Label>
                            <div class="col-span-2">
                                <CompanySelect v-if="job?.customer_company" v-model="job.customer_company.id"
                                    class="w-full" />
                                <ContactSelect v-else-if="job?.customer_contact" v-model="job.customer_contact.id"
                                    class="w-full" />
                                <div v-else class="text-sm text-neutral-500">Aucun client défini</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Priorité</Label>
                            <div class="col-span-2">
                                <PrioritySelect v-if="job?.priority" v-model="job.priority" class="w-full" />
                                <div v-else class="text-sm text-neutral-500">Priorité non définie</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Type d'intervention</Label>
                            <div class="col-span-2">
                                <CategorySelect v-if="job?.category" v-model="job.category.id" class="w-full" />
                                <div v-else class="text-sm text-neutral-500">Catégorie non définie</div>
                            </div>
                        </div>

                        <div class="grid grid-cols-3 gap-4 items-center">
                            <Label class="text-sm font-medium text-neutral-700 !mb-0">Référence client</Label>
                            <div class="col-span-2">
                                <Input v-if="job?.customer_reference !== undefined" v-model="job.customer_reference"
                                    class="w-full" placeholder="Référence client" />
                                <div v-else class="text-sm text-neutral-500">Aucune référence client</div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import CategorySelect from '@/common/components/form/category-select/CategorySelect.vue'
import CompanySelect from '@/common/components/form/company-select/CompanySelect.vue'
import ContactSelect from '@/common/components/form/contact-select/ContactSelect.vue'
import PrioritySelect from '@/common/components/form/priority-select/PrioritySelect.vue'
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import Card from '@/common/components/ui/card/Card.vue'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import Input from '@/common/components/ui/input/Input.vue'
import Label from '@/common/components/ui/label/Label.vue'
import Separator from '@/common/components/ui/separator/Separator.vue'
import Tabs from '@/common/components/ui/tabs/Tabs.vue'
import TabsContent from '@/common/components/ui/tabs/TabsContent.vue'
import TabsList from '@/common/components/ui/tabs/TabsList.vue'
import TabsTrigger from '@/common/components/ui/tabs/TabsTrigger.vue'
import { useFetcher } from '@/common/composables/fetcher'
import { useJob } from '@/common/composables/useJob'
import {
    AlertTriangle,
    ArrowLeft,
    Calendar,
    CalendarArrowUp,
    CalendarCheck,
    Check,
    ChevronDown,
    Circle,
    Clock,
    Edit,
    File,
    FileText,
    Folder,
    Image,
    LogOut,
    Mail,
    Map,
    MapPin,
    MapPinned,
    Play,
    Plus,
    ScanSearch,
    ScrollText,
    ShieldAlert,
    StickyNote,
    User,
    UserPlus,
    UserRoundX
} from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'

const props = defineProps({
    inDialog: {
        type: Boolean,
        default: false
    }
})

const route = useRoute()
const fetcher = useFetcher()
const { getPriorityConfig } = useJob()

const job = ref(null)
const loading = ref(false)

const fetchJob = async () => {
    loading.value = true
    try {
        const jobId = route.params.id
        const response = await fetcher.get(`/jobs/${jobId}`)
        job.value = response.data
        console.log('Job loaded:', job.value)
    } catch (error) {
        console.error('Erreur lors du chargement du job:', error)
        toast.error('Erreur lors du chargement du job')
    } finally {
        loading.value = false
    }
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const getClientName = () => {
    if (job.value?.customer_company) {
        return job.value.customer_company.name
    }
    if (job.value?.customer_contact) {
        return job.value.customer_contact.full_name
    }
    return 'Client non défini'
}

const getClientAddress = () => {
    if (job.value?.site) {
        const parts = [
            job.value.site.name,
            job.value.site.street,
            job.value.site.zip,
            job.value.site.city
        ].filter(Boolean)
        return parts.join(', ')
    }
    return 'Adresse non définie'
}

const getDuration = () => {
    if (job.value?.scheduled_start && job.value?.scheduled_end) {
        const start = new Date(job.value.scheduled_start)
        const end = new Date(job.value.scheduled_end)
        const diffMs = end - start
        const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
        const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
        return `${diffHours}h ${diffMinutes}min`
    }
    return 'Durée non définie'
}

onMounted(() => {
    fetchJob()
})
</script>