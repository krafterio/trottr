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
                            <Badge v-if="job?.status"
                                :style="{ backgroundColor: job.status.color + '20', color: job.status.color }">
                                <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                {{ job.status.name }}
                            </Badge>
                            <Badge v-if="!job?.operator" class="bg-yellow-50 text-yellow-700 cursor-pointer"
                                @click="openPlannerDialog">
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
                    <Button variant="outline" @click="openPlannerDialog">
                        <UserPlus class="h-4 w-4" />
                        Assigner et planifier
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
                            <Badge v-if="job?.status"
                                :style="{ backgroundColor: job.status.color + '20', color: job.status.color }">
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
                            <div class="flex items-start space-x-3">
                                <Avatar class="h-8 w-8 rounded-sm" v-if="job?.operator">
                                    <AvatarImage v-if="job?.operator?.avatar"
                                        :src="`/storage/download/${job?.operator?.avatar}`" v-fetcher-src.lazy
                                        :alt="job?.operator?.name" class="h-8 w-8" />
                                    <AvatarFallback v-else class="bg-neutral-800 text-neutral-300 rounded-sm">
                                        {{ getOperatorInitials(job.operator) }}
                                    </AvatarFallback>
                                </Avatar>
                                <User v-else class="h-7 w-7 text-neutral-400" :stroke-width="1.1" />
                                <div>
                                    <p class="text-sm font-medium text-neutral-900" v-if="job?.operator">{{
                                        job?.operator?.name }}</p>
                                    <p class="text-sm font-medium text-neutral-900" v-else>À assigner</p>
                                    <p class="text-xs text-neutral-500">Opérateur</p>
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
                            <TabsTrigger v-if="workspaceStore.workspace?.use_diagnostics" value="diagnostics">
                                Diagnostics</TabsTrigger>
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
                            </div>
                        </TabsContent>

                        <TabsContent value="diagnostics">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Diagnostics</h2>
                                    <Button @click="openDiagnosticDialog">
                                        <Plus class="h-4 w-4" />
                                        Ajouter un diagnostic
                                    </Button>
                                </div>

                                <div v-if="diagnostics.length === 0" class="text-center py-8 text-neutral-500">
                                    <p>Aucun diagnostic ajouté</p>
                                    <p class="text-sm mt-2">Ajoutez des diagnostics pour documenter les problèmes
                                        rencontrés</p>
                                </div>

                                <div v-else>
                                    <VueDraggable v-model="diagnostics" :animation="200" handle=".drag-handle"
                                        @end="onDiagnosticReorder" class="grid grid-cols-1 gap-4">
                                        <div v-for="diagnostic in diagnostics" :key="diagnostic.id"
                                            class="bg-white border rounded-lg p-4 hover:shadow-md transition-shadow">
                                            <div class="flex items-start justify-between mb-3">
                                                <div class="flex items-center space-x-2">
                                                    <div
                                                        class="drag-handle cursor-move text-neutral-400 hover:text-neutral-600">
                                                        <GripVertical class="h-4 w-4" />
                                                    </div>
                                                    <h3 class="font-medium text-neutral-900">{{
                                                        diagnostic.job_diagnostic.name }}</h3>
                                                </div>
                                                <DropdownMenu>
                                                    <DropdownMenuTrigger asChild>
                                                        <Button variant="ghost" size="sm" class="h-6 w-6 p-0">
                                                            <MoreVertical class="h-4 w-4" />
                                                        </Button>
                                                    </DropdownMenuTrigger>
                                                    <DropdownMenuContent align="end">
                                                        <DropdownMenuItem @click="handleEditDiagnostic(diagnostic)">
                                                            <Pen class="h-4 w-4" />
                                                            Modifier
                                                        </DropdownMenuItem>
                                                        <DropdownMenuItem @click="handleDeleteDiagnostic(diagnostic)">
                                                            <Trash class="text-destructive h-4 w-4" />
                                                            Supprimer
                                                        </DropdownMenuItem>
                                                    </DropdownMenuContent>
                                                </DropdownMenu>
                                            </div>
                                            <p class="text-sm text-neutral-600 mb-3">{{ diagnostic.description }}</p>
                                            <div class="flex items-center justify-between text-xs text-neutral-500">
                                                <span>{{ formatDate(diagnostic.created_at) }}</span>
                                                <span v-if="diagnostic.created_by">{{ diagnostic.created_by.email
                                                    }}</span>
                                            </div>
                                        </div>
                                    </VueDraggable>
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
                            </div>
                        </TabsContent>

                        <TabsContent value="rapports">
                            <div class="p-4">
                                <div class="flex items-center justify-between mb-4">
                                    <h2 class="text-lg font-semibold text-neutral-900">Rapports d'intervention</h2>
                                </div>

                                <div class="text-center py-8 text-neutral-500">
                                    <p>Fonctionnalité en cours de développement</p>
                                    <p class="text-sm mt-2">La génération de rapports sera bientôt disponible</p>
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
                            </div>
                        </TabsContent>
                    </Tabs>
                </div>
            </div>

            <div v-if="!inDialog" class="w-140 bg-white border-l p-6 overflow-y-auto">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-neutral-900">Détails de l'intervention</h3>
                        <DropdownMenu v-if="job?.status">
                            <DropdownMenuTrigger as-child>
                                <Button :style="{ backgroundColor: job.status.color + '20', color: job.status.color }"
                                    class="hover:opacity-80 cursor-pointer">
                                    <Circle class="fill-current" style="height: 6px; width: 6px;" />
                                    {{ job.status.name }}
                                    <ChevronDown class="h-4 w-4" />
                                </Button>
                            </DropdownMenuTrigger>
                            <DropdownMenuContent class="w-56" align="end">
                                <DropdownMenuItem v-for="status in jobStatuses" :key="status.id"
                                    @click="updateJobStatus(status.id)" class="flex items-center gap-2 cursor-pointer">
                                    <Circle class="fill-current" style="height: 8px; width: 8px;"
                                        :style="{ color: status.color }" />
                                    <span>{{ status.name }}</span>
                                </DropdownMenuItem>
                            </DropdownMenuContent>
                        </DropdownMenu>
                    </div>

                    <div class="space-y-4">
                        <div>
                            <h4 class="text-sm font-medium text-neutral-700">Référence intervention</h4>
                            <p class="text-xl font-mono text-neutral-900">{{ job?.reference || 'Chargement...' }}</p>
                            <p class="text-xs text-neutral-400">Créé le {{ job?.created_at ? formatDate(job.created_at)
                                : 'Chargement...' }}</p>
                        </div>

                        <div class="ps-8 relative">
                            <div class="bg-neutral-100 border rounded-lg p-3 flex items-center justify-between mb-2 relative cursor-pointer hover:bg-secondary-light hover:border-secondary"
                                @click="openPlannerDialog">
                                <Circle
                                    class="absolute translate-x-[-50%] top-50% -left-5 fill-neutral-300 stroke-neutral-300"
                                    style="height: 10px; width: 10px;" />
                                <span class="text-sm font-medium text-neutral-700">Démarrage prévu</span>
                                <span class="text-sm text-neutral-900">{{ job?.scheduled_start ?
                                    formatDate(job.scheduled_start) : 'Non planifié' }}</span>
                            </div>

                            <span
                                class="absolute left-3 top-6 w-0.5 h-12 border-l-1 border-dashed border-neutral-300"></span>

                            <div class="border rounded-lg p-3 flex items-center justify-between relative cursor-pointer hover:bg-secondary-light hover:border-secondary"
                                :class="job?.scheduled_end ? 'bg-secondary-light border-secondary ' : 'bg-neutral-100'"
                                @click="openPlannerDialog">
                                <span
                                    class="absolute translate-x-[-50%] top-50% -left-5 ring-1 ring-offset-2 rounded-full"
                                    :class="job?.scheduled_end ? 'bg-secondary ring-secondary' : 'bg-neutral-300 ring-neutral-300'"
                                    style="height: 10px; width: 10px;" />
                                <span class="text-sm font-medium text-neutral-700">Fin prévue</span>
                                <div class="text-sm">
                                    <span class="text-secondary-dark me-2" v-if="job?.scheduled_end">{{ getDuration()
                                    }}</span>

                                    <span class="text-neutral-900">{{ job?.scheduled_end ? formatDate(job.scheduled_end)
                                        : 'Non planifié' }}</span>
                                </div>
                            </div>
                        </div>

                        <Separator />

                        <h3 class="font-medium flex items-center justify-between">
                            Informations générales
                            <Button variant="outline" size="sm" @click="openJobDialog">
                                <Edit class="h-3 w-3 mr-1" />
                                Éditer
                            </Button>
                        </h3>

                        <div class="grid grid-cols-2 gap-5 items-center">
                            <div class="flex gap-2 items-center">
                                <component :is="getClientInfo.icon" class="h-7 w-7 flex-shrink-0" :stroke-width="1.2" />
                                <div class="flex flex-col gap-0 min-w-0 flex-1">
                                    <p class="text-xs font-medium text-neutral-700 !mb-0">
                                        {{ getClientInfo.label }}
                                    </p>
                                    <p v-if="getClientInfo.link"
                                        class="truncate cursor-pointer font-medium hover:text-primary hover:underline"
                                        @click="$router.push(getClientInfo.link)">
                                        {{ getClientInfo.name }}
                                    </p>
                                    <p v-else class="font-mono uppercase truncate">
                                        {{ getClientInfo.name }}
                                    </p>
                                </div>
                            </div>

                            <div class="flex gap-2 items-center">
                                <component :is="getPriorityConfig(job?.priority).icon" class="h-8 w-8 p-2 rounded-md"
                                    :class="getPriorityConfig(job?.priority).bgColor + ' ' + getPriorityConfig(job?.priority).color" />
                                <div class="flex flex-col gap-0 min-w-0 flex-1">
                                    <p class="text-xs font-medium text-neutral-700 !mb-0">
                                        Priorité
                                    </p>
                                    <p class="truncate font-medium">
                                        {{ getPriorityConfig(job?.priority).label }}
                                    </p>
                                </div>
                            </div>

                            <div class="flex gap-2 items-center">
                                <CircleDot class="h-7 w-7 flex-shrink-0" :stroke-width="3"
                                    :stroke="job?.category?.color" v-if="job?.category?.name" />
                                <CircleDot class="h-7 w-7 stroke-neutral-400 flex-shrink-0" :stroke-width="1.5"
                                    v-else />
                                <div class="flex flex-col gap-0 min-w-0 flex-1">
                                    <p class="text-xs font-medium text-neutral-700 !mb-0">
                                        Catégorie d'intervention
                                    </p>
                                    <p class="truncate font-medium" v-if="job?.category?.name">{{
                                        job?.category?.name }}
                                    </p>
                                    <p class="truncate" v-else>-</p>
                                </div>
                            </div>

                            <div class="flex gap-2 items-center">
                                <Asterisk class="h-7 w-7 flex-shrink-0" :stroke-width="1.2" />
                                <div class="flex flex-col gap-0 min-w-0 flex-1">
                                    <p class="text-xs font-medium text-neutral-700 !mb-0">
                                        Référence client
                                    </p>
                                    <p class="truncate font-medium" v-if="job?.customer_reference">{{
                                        job?.customer_reference }}</p>
                                    <p class="truncate" v-else>-</p>
                                </div>
                            </div>
                        </div>

                        <Card class="p-4 gap-0 items-start relative cursor-pointer hover:bg-neutral-100"
                            @click="openEditDialog">
                            <div class="flex absolute top-3 right-3 gap-2">
                                <Button variant="outline" class="h-8 w-8" size="icon" @click="openEditDialog">
                                    <Edit class="h-3 w-3" />
                                </Button>
                            </div>
                            <div class="flex items-center gap-1 mb-2">
                                <ScrollText class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Description de l'intervention</h4>
                            </div>
                            <p class="text-sf font-medium">{{ job?.name || 'Aucun sujet' }}</p>
                            <p class="text-sm text-neutral-400 mt-1">{{ job?.description || 'Aucune description' }}</p>
                        </Card>

                        <Card class="p-4 gap-0 items-start relative cursor-pointer hover:bg-neutral-100"
                            @click="openSiteDialog">
                            <div class="flex absolute top-3 right-3 gap-2">
                                <Button variant="outline" class="h-8 w-8" size="icon" @click="openSiteDialog">
                                    <Edit class="h-3 w-3" />
                                </Button>
                            </div>
                            <div class="flex items-center gap-1 mb-2">
                                <MapPinned class="h-4 w-4" />
                                <h4 class="text-sm font-medium">Site d'intervention</h4>
                            </div>
                            <div class="text-sm text-neutral-600">
                                <p v-if="job?.site?.name" class="cursor-pointer hover:text-primary underline"
                                    @click.stop="viewSite(job.site)">{{ job.site.name }}</p>
                                <p v-if="job?.site?.street">{{ job.site.street }}</p>
                                <p v-if="job?.site?.zip && job?.site?.city">{{ job.site.zip }} {{ job.site.city }}</p>
                                <p v-if="!job?.site">Aucun site défini</p>
                            </div>
                        </Card>

                        <Card
                            class="p-4 gap-0 border-dashed flex items-center justify-center cursor-pointer hover:bg-neutral-50"
                            @click="openPlannerDialog">
                            <UserPlus class="h-10 w-10 mb-3 text-neutral-500" :stroke-width="1.2" />
                            <p class="text-sm text-neutral-500">Assigner un technicien</p>
                        </Card>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Dialog :open="editDialogOpen" @update:open="editDialogOpen = false">
        <DialogContent class="sm:max-w-[625px]">
            <DialogHeader>
                <DialogTitle>Modifier l'intervention</DialogTitle>
                <DialogDescription>
                    Modifiez le nom et la description de l'intervention.
                </DialogDescription>
            </DialogHeader>
            <div class="grid gap-4 py-4">
                <div class="grid gap-2">
                    <Label for="name">Nom de l'intervention</Label>
                    <Input id="name" v-model="editForm.name" placeholder="Nom de l'intervention" />
                </div>
                <div class="grid gap-2">
                    <Label for="description">Description</Label>
                    <Textarea id="description" v-model="editForm.description"
                        placeholder="Description de l'intervention" />
                </div>
            </div>
            <DialogFooter>
                <Button variant="outline" @click="editDialogOpen = false">Annuler</Button>
                <Button @click="saveEdit" :disabled="loading">Enregistrer</Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>

    <!-- Dialog pour ajouter un diagnostic -->
    <Dialog :open="diagnosticDialogOpen" @update:open="diagnosticDialogOpen = false">
        <DialogContent class="sm:max-w-[500px]">
            <DialogHeader>
                <DialogTitle>{{ isEditDiagnostic ? 'Modifier le diagnostic' : 'Ajouter un diagnostic' }}</DialogTitle>
                <DialogDescription>Modifiez le diagnostic et sa description</DialogDescription>
            </DialogHeader>
            <form @submit.prevent="handleDiagnosticSubmit" class="space-y-4">
                <div class="grid gap-2">
                    <Label for="diagnostic">Diagnostic *</Label>
                    <Select v-model="diagnosticForm.job_diagnostic" @update:model-value="handleDiagnosticChange">
                        <SelectTrigger class="w-full">
                            <SelectValue placeholder="Sélectionnez un diagnostic" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem v-for="diagnostic in availableDiagnostics" :key="diagnostic.id"
                                :value="diagnostic.id">
                                {{ diagnostic.name }}
                            </SelectItem>
                        </SelectContent>
                    </Select>
                </div>

                <div class="grid gap-2">
                    <Label for="description">Description</Label>
                    <Textarea v-model="diagnosticForm.description" placeholder="Description détaillée du diagnostic..."
                        rows="4" />
                </div>
            </form>
            <DialogFooter>
                <Button variant="outline" @click="diagnosticDialogOpen = false">Annuler</Button>
                <Button @click="handleDiagnosticSubmit" :disabled="loading">
                    {{ loading ? 'Enregistrement...' : (isEditDiagnostic ? 'Modifier' : 'Ajouter') }}
                </Button>
            </DialogFooter>
        </DialogContent>
    </Dialog>

    <PlannerDialog :open="plannerDialogOpen" :job="job" @update:open="plannerDialogOpen = $event"
        @assigned="handleJobAssigned" />
</template>

<script setup>
import { Avatar, AvatarFallback, AvatarImage } from '@/common/components/ui/avatar'
import Badge from '@/common/components/ui/badge/Badge.vue'
import { Button } from '@/common/components/ui/button'
import Card from '@/common/components/ui/card/Card.vue'
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/common/components/ui/dialog'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/common/components/ui/dropdown-menu'
import Input from '@/common/components/ui/input/Input.vue'
import Label from '@/common/components/ui/label/Label.vue'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/common/components/ui/select'
import Separator from '@/common/components/ui/separator/Separator.vue'
import Tabs from '@/common/components/ui/tabs/Tabs.vue'
import TabsContent from '@/common/components/ui/tabs/TabsContent.vue'
import TabsList from '@/common/components/ui/tabs/TabsList.vue'
import TabsTrigger from '@/common/components/ui/tabs/TabsTrigger.vue'
import { Textarea } from '@/common/components/ui/textarea'
import { bus, useBus } from '@/common/composables/bus'
import { useFetcher } from '@/common/composables/fetcher'
import { useJob } from '@/common/composables/useJob'
import { useWorkspaceStore } from '@/main/stores/workspace'
import {
    AlertTriangle,
    ArrowLeft,
    Asterisk,
    Building2,
    Calendar,
    CalendarArrowUp,
    ChevronDown,
    Circle,
    CircleDot,
    Clock,
    Edit,
    File,
    Folder,
    GripVertical,
    MapPin,
    MapPinned,
    MoreVertical,
    Pen,
    Play,
    Plus,
    ScanSearch,
    ScrollText,
    ShieldAlert,
    Trash,
    User,
    UserPlus,
    UserRoundX
} from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'
import { VueDraggable } from 'vue-draggable-plus'
import { useRoute, useRouter } from 'vue-router'
import { toast } from 'vue-sonner'
import PlannerDialog from './PlannerDialog.vue'

const props = defineProps({
    inDialog: {
        type: Boolean,
        default: false
    }
})

const route = useRoute()
const router = useRouter()
const fetcher = useFetcher()
const { getPriorityConfig } = useJob()
const workspaceStore = useWorkspaceStore()

const job = ref(null)
const loading = ref(true)
const inDialog = ref(false)
const jobStatuses = ref([])

const fetchJobStatuses = async () => {
    try {
        const response = await fetcher.get('/job-status')
        jobStatuses.value = response.data
    } catch (error) {
        console.error('Erreur lors du chargement des statuts:', error)
    }
}

const updateJobStatus = async (statusId) => {
    try {
        await fetcher.patch(`/jobs/${job.value.id}`, { status: statusId })
        toast.success('Statut modifié avec succès')

        // Mettre à jour uniquement le statut localement
        const newStatus = jobStatuses.value.find(status => status.id === statusId)
        if (newStatus && job.value) {
            job.value.status = newStatus
        }
    } catch (error) {
        console.error('Erreur lors de la modification du statut:', error)
        toast.error('Erreur lors de la modification du statut')
    }
}

// Variables pour les diagnostics
const diagnostics = ref([])
const diagnosticDialogOpen = ref(false)
const isEditDiagnostic = ref(false)
const editingDiagnosticId = ref(null)
const selectedDiagnosticForDelete = ref(null)
const diagnosticForm = ref({
    job_diagnostic: null,
    description: ''
})
const availableDiagnostics = ref([])

const editDialogOpen = ref(false)
const editForm = ref({
    name: '',
    description: ''
})

const plannerDialogOpen = ref(false)

const fetchJob = async () => {
    loading.value = true
    try {
        const jobId = route.params.id
        const response = await fetcher.get(`/jobs/${jobId}`)
        job.value = response.data

        // Charger les diagnostics si use_diagnostics est activé
        if (workspaceStore.workspace?.use_diagnostics) {
            await fetchDiagnostics()
            await fetchAvailableDiagnostics()
        }
    } catch (error) {
        console.error('Erreur lors du chargement du job:', error)
        toast.error('Erreur lors du chargement du job')
    } finally {
        loading.value = false
    }
}

const fetchDiagnostics = async () => {
    try {
        const jobId = route.params.id
        const response = await fetcher.get('/job-job-diagnostic', { params: { job_id: jobId } })
        diagnostics.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des diagnostics:', error)
    }
}

const fetchAvailableDiagnostics = async () => {
    try {
        const response = await fetcher.get('/job-diagnostics')
        availableDiagnostics.value = response.data || []
    } catch (error) {
        console.error('Erreur lors du chargement des diagnostics disponibles:', error)
    }
}

const openDiagnosticDialog = () => {
    isEditDiagnostic.value = false
    diagnosticForm.value = {
        job_diagnostic: null,
        description: ''
    }
    diagnosticDialogOpen.value = true
}

const handleDiagnosticSubmit = async () => {
    if (!diagnosticForm.value.job_diagnostic) {
        toast.error('Veuillez sélectionner un diagnostic')
        return
    }

    try {
        const jobId = route.params.id
        const payload = {
            job: jobId,
            job_diagnostic: diagnosticForm.value.job_diagnostic,
            description: diagnosticForm.value.description
        }

        if (isEditDiagnostic.value && editingDiagnosticId.value) {
            await fetcher.put(`/job-job-diagnostic/${editingDiagnosticId.value}`, payload)
            toast.success('Diagnostic modifié avec succès')
        } else {
            payload.sequence = diagnostics.value.length + 1
            await fetcher.post('/job-job-diagnostic', payload)
            toast.success('Diagnostic ajouté avec succès')
        }
        diagnosticDialogOpen.value = false
        await fetchDiagnostics()
    } catch (error) {
        console.error('Erreur lors de l\'ajout/modification du diagnostic:', error)
        toast.error('Erreur lors de l\'ajout/modification du diagnostic')
    }
}

const handleDiagnosticChange = () => {
    if (diagnosticForm.value.job_diagnostic) {
        const selectedDiagnostic = availableDiagnostics.value.find(d => d.id === diagnosticForm.value.job_diagnostic)
        if (selectedDiagnostic) {
            diagnosticForm.value.description = selectedDiagnostic.description || ''
        }
    }
}

const onDiagnosticReorder = async () => {
    try {
        const reorderData = diagnostics.value.map((diagnostic, index) => ({
            id: diagnostic.id,
            sequence: index + 1
        }))

        await fetcher.put('/job-job-diagnostic/reorder', { diagnostics: reorderData })
        toast.success('Diagnostics réorganisés avec succès')
    } catch (error) {
        console.error('Erreur lors du réordonnancement:', error)
        toast.error('Erreur lors du réordonnancement')
        await fetchDiagnostics() // Recharger l'ordre original
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

const getOperatorInitials = (operator) => {
    if (!operator) return 'U'
    if (operator.initials) return operator.initials
    if (operator.name) {
        return operator.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
    }
    return operator.email?.[0]?.toUpperCase() || 'U'
}

const getClientInfo = computed(() => {
    if (!job.value) return { name: 'Client non défini', icon: User, type: 'none', label: 'Client' }

    // Si il y a une société ET un contact, c'est la société le client
    if (job.value.customer_company) {
        return {
            name: job.value.customer_company.name,
            icon: Building2,
            type: 'company',
            label: 'Client (société)',
            link: { name: 'company', params: { id: job.value.customer_company.id } }
        }
    }

    // Si il y a seulement un contact (pas de société)
    if (job.value.customer_contact) {
        return {
            name: job.value.customer_contact.full_name,
            icon: User,
            type: 'contact',
            label: 'Client (particulier)',
            link: { name: 'contact', params: { id: job.value.customer_contact.id } }
        }
    }

    return { name: 'Client non défini', icon: User, type: 'none', label: 'Client', link: null }
})

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

const openJobDialog = () => {
    bus.trigger('open-job-dialog', job.value)
}

const openEditDialog = () => {
    editForm.value = {
        name: job.value?.name || '',
        description: job.value?.description || ''
    }
    editDialogOpen.value = true
}

const saveEdit = async () => {
    loading.value = true
    try {
        const jobId = route.params.id
        await fetcher.patch(`/jobs/${jobId}`, editForm.value)
        toast.success('Intervention modifiée avec succès')
        fetchJob() // Refresh job data
        editDialogOpen.value = false
    } catch (error) {
        console.error('Erreur lors de la sauvegarde de l\'intervention:', error)
        toast.error('Erreur lors de la sauvegarde de l\'intervention')
    } finally {
        loading.value = false
    }
}

const openSiteDialog = () => {
    const dialogData = {
        job: job.value,
        customerCompany: job.value?.customer_company,
        customerContact: job.value?.customer_contact,
        currentSite: job.value?.site
    }

    bus.trigger('open-job-site-dialog', dialogData)
}

const viewSite = (site) => {
    if (site?.id) {
        router.push({ name: 'site', params: { id: site.id } })
    }
}

const openPlannerDialog = () => {
    plannerDialogOpen.value = true
}

const handleJobAssigned = (data) => {
    if (data.updatedJob) {
        job.value = data.updatedJob
        toast.success(`Intervention assignée à ${data.operator.name}`)
    } else {
        toast.success(`Intervention assignée à ${data.operator.name}`)
        fetchJob()
    }
}

const handleEditDiagnostic = (diagnostic) => {
    isEditDiagnostic.value = true
    editingDiagnosticId.value = diagnostic.id
    diagnosticForm.value = {
        job_diagnostic: diagnostic.job_diagnostic.id,
        description: diagnostic.description
    }
    diagnosticDialogOpen.value = true
}

const handleDeleteDiagnostic = (diagnostic) => {
    selectedDiagnosticForDelete.value = diagnostic
    bus.trigger('confirm-delete', {
        title: 'Supprimer le diagnostic',
        message: 'Êtes-vous sûr de vouloir supprimer ce diagnostic ?',
        itemName: diagnostic.job_diagnostic.name,
        confirmationText: 'Cette action est irréversible.',
        confirmEvent: 'confirm-delete-job-diagnostic:confirmed'
    })
}

const deleteDiagnostic = async () => {
    if (!selectedDiagnosticForDelete.value) return

    try {
        await fetcher.delete(`/job-job-diagnostic/${selectedDiagnosticForDelete.value.id}`)
        toast.success('Diagnostic supprimé avec succès')
        bus.trigger('confirm-delete-dialog:close')
        await fetchDiagnostics()
        selectedDiagnosticForDelete.value = null
    } catch (error) {
        console.error('Erreur lors de la suppression du diagnostic:', error)
        toast.error('Erreur lors de la suppression du diagnostic')
        bus.trigger('confirm-delete-dialog:close')
    }
}

useBus(bus, 'job-saved', () => {
    fetchJob()
})

useBus(bus, 'job-created-stay', () => {
    fetchJob()
})

useBus(bus, 'site-created-stay', () => {
    fetchJob()
})



useBus(bus, 'confirm-delete-job-diagnostic:confirmed', () => {
    deleteDiagnostic()
})

useBus(bus, 'job-site-updated', (data) => {
    // Recharger le job pour avoir les données mises à jour
    fetchJob()
})

onMounted(() => {
    fetchJob()
    fetchJobStatuses()
})
</script>