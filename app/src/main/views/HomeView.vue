<template>
    <div class="h-full flex flex-col">
        <!-- Bandeau supérieur avec actions et KPIs -->
        <div class="bg-white border-b px-6 py-4">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h1 class="text-2xl font-bold text-neutral-900">Interventions</h1>
                    <p class="text-neutral-600">Gestion des interventions terrain</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2 bg-accent rounded-md p-2 h-9">
                        <p class="text-sm text-neutral-600">Afficher KPIs</p>
                        <Switch />
                    </div>
                    <Button variant="outline">
                        <Download class="h-4 w-4" />
                        Exporter
                    </Button>
                    <Button>
                        <Plus class="h-4 w-4" />
                        Nouvelle intervention
                    </Button>
                </div>
            </div>

            <!-- KPIs compacts -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Calendar class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Aujourd'hui</p>
                        <p class="text-lg font-semibold text-neutral-900">12</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <AlertTriangle class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">En retard</p>
                        <p class="text-lg font-semibold text-neutral-900">3</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <Clock class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">En cours</p>
                        <p class="text-lg font-semibold text-neutral-900">8</p>
                    </div>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 bg-neutral-100 rounded-lg flex items-center justify-center">
                        <CheckCircle class="h-4 w-4 text-neutral-600" />
                    </div>
                    <div>
                        <p class="text-sm text-neutral-600">Terminées</p>
                        <p class="text-lg font-semibold text-neutral-900">27</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Contenu principal avec sidebar -->
        <div class="flex-1 flex overflow-hidden">
            <div class="w-64 bg-neutral-50 border-r p-4 overflow-y-auto">
                <h3 class="font-semibold text-neutral-900 mb-4">Filtres</h3>

                <!-- Statut -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Statut</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Planifiée</span>
                            <span class="ml-auto text-xs text-neutral-400">15</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">En cours</span>
                            <span class="ml-auto text-xs text-neutral-400">8</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">En retard</span>
                            <span class="ml-auto text-xs text-neutral-400">3</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox />
                            <span class="ml-2 text-sm text-neutral-600">Terminée</span>
                            <span class="ml-auto text-xs text-neutral-400">27</span>
                        </label>
                    </div>
                </div>

                <!-- Priorité -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Priorité</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Urgente</span>
                            <span class="ml-auto text-xs text-neutral-400">5</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Élevée</span>
                            <span class="ml-auto text-xs text-neutral-400">12</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Normale</span>
                            <span class="ml-auto text-xs text-neutral-400">26</span>
                        </label>
                    </div>
                </div>

                <!-- Type d'intervention -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Type</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Maintenance</span>
                            <span class="ml-auto text-xs text-neutral-400">18</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Dépannage</span>
                            <span class="ml-auto text-xs text-neutral-400">15</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Installation</span>
                            <span class="ml-auto text-xs text-neutral-400">10</span>
                        </label>
                    </div>
                </div>

                <!-- Opérateur -->
                <div class="mb-6">
                    <h4 class="text-sm font-medium text-neutral-700 mb-2">Opérateur</h4>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Jean Martin</span>
                            <span class="ml-auto text-xs text-neutral-400">8</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox checked />
                            <span class="ml-2 text-sm text-neutral-600">Sophie Dubois</span>
                            <span class="ml-auto text-xs text-neutral-400">6</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox />
                            <span class="ml-2 text-sm text-neutral-600">Pierre Leclerc</span>
                            <span class="ml-auto text-xs text-neutral-400">4</span>
                        </label>
                        <label class="flex items-center">
                            <Checkbox />
                            <span class="ml-2 text-sm text-neutral-600">Marie Rousseau</span>
                            <span class="ml-auto text-xs text-neutral-400">5</span>
                        </label>
                    </div>
                </div>

                <Button variant="outline" size="sm" class="w-full">
                    <RotateCcw class="h-4 w-4 mr-2" />
                    Réinitialiser
                </Button>
            </div>

            <!-- Tableau des interventions -->
            <div class="flex-1 overflow-y-auto">
                <div class="">
                    <div class="px-6 py-4 border-b">
                        <div class="flex items-center justify-between">
                            <h3 class="text-lg font-semibold text-neutral-900">Liste des interventions</h3>
                            <div class="flex items-center space-x-3">
                                <span class="text-sm text-muted-foreground">26 interventions</span>
                                <Button variant="outline" size="sm" class="w-8">
                                    <MoreVertical class="h-4 w-4" />
                                </Button>
                                <Button variant="outline">
                                    <Columns class="h-4 w-4" />
                                    Colonnes
                                    <ChevronDown class="h-4 w-4" />
                                </Button>
                            </div>
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-neutral-50 border-b">
                                <tr>
                                    <th
                                        class="px-3 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider w-8">
                                        <Checkbox />
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Réf.
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Intervention
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Client
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Opérateur
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Date/Heure
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Statut
                                    </th>
                                    <th
                                        class="px-6 py-3 text-left text-xs font-medium text-neutral-500 uppercase tracking-wider">
                                        Priorité
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="bg-white divide-y divide-neutral-200">
                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">TR42K8</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Panne électrique</div>
                                            <div class="text-sm text-neutral-500">Dépannage urgent</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">SARL Martin</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            15 rue de la République
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-neutral-600 rounded-full flex items-center justify-center text-white text-xs font-medium mr-3">
                                                JM
                                            </div>
                                            <div class="text-sm text-neutral-900">Jean Martin</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Aujourd'hui 14:00</div>
                                        <div class="text-xs text-red-600">En retard de 30min</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                            En retard
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                            Urgente
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">MP7X3L</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Maintenance préventive
                                            </div>
                                            <div class="text-sm text-neutral-500">Contrôle mensuel</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Hotel Plaza</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            42 av. Champs-Élysées
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-neutral-600 rounded-full flex items-center justify-center text-white text-xs font-medium mr-3">
                                                SD
                                            </div>
                                            <div class="text-sm text-neutral-900">Sophie Dubois</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Aujourd'hui 16:30</div>
                                        <div class="text-xs text-neutral-600">Dans 2h</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Planifiée
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                                            Élevée
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">IN9R4V</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Installation équipement
                                            </div>
                                            <div class="text-sm text-neutral-500">Nouvel équipement</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Café Central</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            8 place de la Bastille
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-neutral-600 rounded-full flex items-center justify-center text-white text-xs font-medium mr-3">
                                                PL
                                            </div>
                                            <div class="text-sm text-neutral-900">Pierre Leclerc</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Demain 09:00</div>
                                        <div class="text-xs text-neutral-500">Durée: 2h</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Planifiée
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Normale
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">RP8M2N</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Réparation urgente</div>
                                            <div class="text-sm text-neutral-500">Système défaillant</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Boulangerie Paul</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            23 rue de Rivoli
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-neutral-600 rounded-full flex items-center justify-center text-white text-xs font-medium mr-3">
                                                MR
                                            </div>
                                            <div class="text-sm text-neutral-900">Marie Rousseau</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Aujourd'hui 13:15</div>
                                        <div class="text-xs text-green-600">En cours</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                                            En cours
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                            Urgente
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">CT5B7Q</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Contrôle technique</div>
                                            <div class="text-sm text-neutral-500">Vérification annuelle</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Garage Moderne</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            67 boulevard Voltaire
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                            À assigner
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Mercredi 10:00</div>
                                        <div class="text-xs text-neutral-500">Durée: 1h30</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Planifiée
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Normale
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">DP3X9K</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Dépannage climatisation
                                            </div>
                                            <div class="text-sm text-neutral-500">Panne système de refroidissement</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Restaurant Le Gourmet</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            12 rue Saint-Antoine
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                            À assigner
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Aujourd'hui 15:00</div>
                                        <div class="text-xs text-red-600">Urgent - client attend</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                            En attente
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                            Urgente
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">MN6Y2R</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Maintenance chaudière
                                            </div>
                                            <div class="text-sm text-neutral-500">Entretien saisonnier</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Résidence Les Jardins</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            45 avenue de la Liberté
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="flex items-center">
                                            <div
                                                class="w-8 h-8 bg-neutral-600 rounded-full flex items-center justify-center text-white text-xs font-medium mr-3">
                                                JM
                                            </div>
                                            <div class="text-sm text-neutral-900">Jean Martin</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Vendredi 14:00</div>
                                        <div class="text-xs text-neutral-500">Durée: 3h</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Planifiée
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                                            Élevée
                                        </span>
                                    </td>
                                </tr>

                                <tr class="hover:bg-neutral-50">
                                    <td class="px-3 py-4 whitespace-nowrap">
                                        <Checkbox />
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span class="text-sm font-mono text-neutral-900">RQ4L8P</span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div>
                                            <div class="text-sm font-medium text-neutral-900">Remplacement pièce</div>
                                            <div class="text-sm text-neutral-500">Composant défectueux</div>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <div class="text-sm text-neutral-900">Pharmacie du Centre</div>
                                        <div class="text-sm text-neutral-500 flex items-center">
                                            33 place de la République
                                            <Button variant="ghost" size="sm" class="h-6 w-6 p-0 ml-2">
                                                <MapPin class="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                                            À assigner
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap text-sm text-neutral-900">
                                        <div>Lundi 11:00</div>
                                        <div class="text-xs text-neutral-500">Durée: 45min</div>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Planifiée
                                        </span>
                                    </td>
                                    <td class="px-6 py-4 whitespace-nowrap">
                                        <span
                                            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-neutral-100 text-neutral-800">
                                            Normale
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

        <!-- Pagination fixe -->
        <TablePagination :current-page="1" :total-pages="3" :total-items="26" :items-per-page="10"
            position-classes="bottom-0 left-80 right-0" @page-change="handlePageChange"
            @items-per-page-change="handleItemsPerPageChange" />
    </div>
</template>

<script setup>
import { Button } from '@/common/components/ui/button'
import { Checkbox } from '@/common/components/ui/checkbox'
import Switch from '@/common/components/ui/switch/Switch.vue'
import TablePagination from '@/main/components/TablePagination.vue'
import {
    AlertTriangle,
    Calendar,
    CheckCircle,
    ChevronDown,
    Clock,
    Columns,
    Download,
    MapPin,
    MoreVertical,
    Plus,
    RotateCcw
} from 'lucide-vue-next'

const handlePageChange = (page) => {
    console.log('Page changed to:', page)
}

const handleItemsPerPageChange = (itemsPerPage) => {
    console.log('Items per page changed to:', itemsPerPage)
}
</script>