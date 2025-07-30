from models.job_diagnostic import JobDiagnostic
from models.workspace import Workspace


async def init_demo_diagnostics(workspace_id: int):
    workspace = await Workspace.query.get(id=workspace_id)
    if not workspace:
        print(f"Workspace {workspace_id} not found")
        return
    
    # Supprimer tous les diagnostics existants du workspace
    existing_diagnostics = await JobDiagnostic.query.filter(workspace=workspace).all()
    deleted_count = 0
    for diagnostic in existing_diagnostics:
        await diagnostic.delete()
        deleted_count += 1

    if deleted_count > 0:
        print(f"Deleted {deleted_count} existing diagnostics")

    diagnostics_data = [
        # Climatisation
        {
            "name": "Compresseur défaillant",
            "description": "Le compresseur ne démarre pas ou fonctionne de manière irrégulière. Vérification du système électrique et du réfrigérant nécessaire.",
            "sequence": 1
        },
        {
            "name": "Fuite de réfrigérant",
            "description": "Détection d'une fuite dans le circuit frigorifique. Recherche du point de fuite et réparation du circuit.",
            "sequence": 2
        },
        {
            "name": "Évaporateur gelé",
            "description": "Formation de glace sur l'évaporateur empêchant le bon fonctionnement. Défaut de dégivrage ou problème de ventilation.",
            "sequence": 3
        },
        {
            "name": "Thermostat déréglé",
            "description": "Le thermostat ne maintient pas la température souhaitée. Calibration ou remplacement du capteur de température.",
            "sequence": 4
        },

        # Plomberie
        {
            "name": "Fuite de canalisation",
            "description": "Découverte d'une fuite dans les canalisations d'eau. Localisation précise et réparation du tuyau endommagé.",
            "sequence": 5
        },
        {
            "name": "Chauffe-eau défaillant",
            "description": "Le chauffe-eau ne produit plus d'eau chaude. Vérification de l'élément chauffant et du thermostat.",
            "sequence": 6
        },
        {
            "name": "Bouchon dans les canalisations",
            "description": "Écoulement ralenti ou bloqué dans les canalisations. Débouchage mécanique ou chimique selon la nature du bouchon.",
            "sequence": 7
        },
        {
            "name": "Vanne de sécurité défaillante",
            "description": "La vanne de sécurité ne fonctionne plus correctement. Remplacement de la vanne pour assurer la sécurité.",
            "sequence": 8
        },

        # Électricité
        {
            "name": "Court-circuit électrique",
            "description": "Détection d'un court-circuit dans l'installation électrique. Recherche de la cause et réparation du circuit défaillant.",
            "sequence": 9
        },
        {
            "name": "Disjoncteur qui saute",
            "description": "Le disjoncteur se déclenche régulièrement. Vérification de la charge électrique et du câblage.",
            "sequence": 10
        },
        {
            "name": "Prise électrique défaillante",
            "description": "Une prise électrique ne fonctionne plus ou présente des signes de surchauffe. Remplacement de la prise défectueuse.",
            "sequence": 11
        },
        {
            "name": "Éclairage de sécurité défaillant",
            "description": "Les luminaires de sécurité ne s'allument pas en cas de panne. Vérification de la batterie et du circuit.",
            "sequence": 12
        },

        # Facility Management
        {
            "name": "Système d'alarme incendie défaillant",
            "description": "Le système d'alarme incendie ne répond plus aux tests. Vérification des détecteurs et de la centrale d'alarme.",
            "sequence": 13
        },
        {
            "name": "Contrôle d'accès en panne",
            "description": "Le système de contrôle d'accès ne reconnaît plus les badges. Réinitialisation du système ou remplacement du lecteur.",
            "sequence": 14
        },
        {
            "name": "Ascenseur bloqué",
            "description": "Un ascenseur est bloqué entre deux étages. Intervention d'urgence pour libérer les passagers.",
            "sequence": 15
        },
        {
            "name": "Ventilation VMC défaillante",
            "description": "Le système de ventilation ne fonctionne plus correctement. Vérification du moteur et des filtres.",
            "sequence": 16
        },

        # Réseau/Network
        {
            "name": "Switch réseau défaillant",
            "description": "Un switch réseau ne transmet plus les données correctement. Remplacement du switch ou réinitialisation.",
            "sequence": 17
        },
        {
            "name": "Câble réseau endommagé",
            "description": "Détection d'un câble réseau sectionné ou endommagé. Remplacement du câble pour rétablir la connectivité.",
            "sequence": 18
        },
        {
            "name": "Point d'accès WiFi défaillant",
            "description": "Le point d'accès WiFi ne diffuse plus le signal. Redémarrage ou remplacement de l'équipement.",
            "sequence": 19
        },
        {
            "name": "Serveur en surchauffe",
            "description": "Le serveur présente des signes de surchauffe. Vérification du système de refroidissement et nettoyage.",
            "sequence": 20
        }
    ]

    for diagnostic_data in diagnostics_data:
        diagnostic = JobDiagnostic(
            workspace=workspace,
            **diagnostic_data
        )
        await diagnostic.save()

    print(f"Created {len(diagnostics_data)} demo diagnostics for workspace {workspace_id}") 