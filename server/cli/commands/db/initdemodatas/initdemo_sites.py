from rich.console import Console
from models.site import Site, BuildingType
from models.workspace import Workspace
from models.country import Country
from models.company import Company
import random

console = Console()


async def init_sites(workspace: Workspace):
    """Initialise les sites pour un workspace"""
    console.print("[yellow]Initialisation des sites...[/yellow]")
    
    # Récupération du pays France par défaut
    france = await Country.query.filter(iso_code="FR").first()
    
    # Récupération de toutes les companies du workspace pour les rattacher aux sites
    companies = await Company.query.filter(workspace=workspace).all()
    company_sirets = [c.siret for c in companies if c.siret]
    
    sites_data = [
        # Sites avec entreprises (environ 80%)
        {"name": "Résidence Les Jardins", "street": "15 rue des Lilas", "zip": "75015", "city": "Paris", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "10483218196001"},
        {"name": "Villa Dupont", "street": "8 avenue de la Paix", "zip": "69003", "city": "Lyon", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "89083863704208"},
        {"name": "Centre Commercial Bellecour", "street": "23 place Bellecour", "zip": "69002", "city": "Lyon", "building_type": BuildingType.LOCAL_COMMERCIAL, "company_siret": "23511615594078"},
        {"name": "Immeuble Saint-Michel", "street": "42 boulevard Saint-Michel", "zip": "75006", "city": "Paris", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "18499310434119"},
        {"name": "Tour de bureaux Défense", "street": "1 esplanade du Général de Gaulle", "zip": "92400", "city": "Courbevoie", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "75255341928327"},
        {"name": "Maison Martin", "street": "67 rue de la République", "zip": "13001", "city": "Marseille", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "83503656431395"},
        {"name": "Résidence Atlantique", "street": "156 avenue de l'Atlantique", "zip": "44000", "city": "Nantes", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "67242388495965"},
        {"name": "Bureaux Tech Center", "street": "9 rue de l'Innovation", "zip": "31000", "city": "Toulouse", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "87101236916697"},
        {"name": "Villa Rochefort", "street": "34 chemin des Pins", "zip": "06400", "city": "Cannes", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "80194514607008"},
        {"name": "Centre d'affaires Lille", "street": "88 rue Nationale", "zip": "59000", "city": "Lille", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "14893252880557"},
        {"name": "Résidence Les Chênes", "street": "45 avenue Victor Hugo", "zip": "69001", "city": "Lyon", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "54303911718227"},
        {"name": "Galerie Marchande Croix-Rousse", "street": "12 rue des Tables Claudiennes", "zip": "69001", "city": "Lyon", "building_type": BuildingType.LOCAL_COMMERCIAL, "company_siret": "48963834657871"},
        {"name": "Maison Pereira", "street": "78 rue de Gerland", "zip": "69007", "city": "Lyon", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "15988399010310"},
        {"name": "Immeuble Vidal", "street": "56 cours Lafayette", "zip": "69003", "city": "Lyon", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "83473829973763"},
        {"name": "Entrepôt Maréchal", "street": "23 rue de l'Industrie", "zip": "69120", "city": "Vaulx-en-Velin", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "65867910551333"},
        {"name": "Résidence Boyer", "street": "18 quai des Célestins", "zip": "69002", "city": "Lyon", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "26247137810809"},
        {"name": "Centre Colas", "street": "34 rue de la Part-Dieu", "zip": "69003", "city": "Lyon", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "67738026064748"},
        {"name": "Magasin Payet", "street": "67 rue Mercière", "zip": "69002", "city": "Lyon", "building_type": BuildingType.LOCAL_COMMERCIAL, "company_siret": "97234398065009"},
        {"name": "Usine Moulin", "street": "89 avenue Lacassagne", "zip": "69003", "city": "Lyon", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "82081219136193"},
        {"name": "Résidence Maillard", "street": "45 rue Garibaldi", "zip": "69006", "city": "Lyon", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "91598856453346"},
        {"name": "Bureaux Traore", "street": "12 avenue Berthelot", "zip": "69007", "city": "Lyon", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "47510799118384"},
        {"name": "Villa Lacroix", "street": "78 rue Paul Bert", "zip": "69003", "city": "Lyon", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "13542794984041"},
        {"name": "Résidence Bouchet", "street": "23 cours Emile Zola", "zip": "69100", "city": "Villeurbanne", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "11824463938847"},
        {"name": "Tour Laurent", "street": "56 avenue Henri Barbusse", "zip": "69100", "city": "Villeurbanne", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "64005242786801"},
        {"name": "Centre Commercial Barre", "street": "89 rue de la République", "zip": "69100", "city": "Villeurbanne", "building_type": BuildingType.LOCAL_COMMERCIAL, "company_siret": "28059620245505"},
        {"name": "Maison Perret", "street": "12 avenue Jean Jaurès", "zip": "69200", "city": "Venissieux", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "31586923226025"},
        {"name": "Résidence Chauvet", "street": "34 rue de la Liberté", "zip": "69230", "city": "Saint-Genis-Laval", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "34216073576431"},
        {"name": "Villa Jacquet", "street": "67 chemin des Fontaines", "zip": "69340", "city": "Francheville", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": "36541458885014"},
        {"name": "Immeuble Costa", "street": "23 quai de la Pêcherie", "zip": "69300", "city": "Caluire-et-Cuire", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "40196556881693"},
        {"name": "Bureaux Faivre", "street": "45 avenue de la Paix", "zip": "69110", "city": "Sainte-Foy-lès-Lyon", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "60885515951450"},
        {"name": "Résidence Les Pins", "street": "78 rue du Commandant Charcot", "zip": "69005", "city": "Lyon", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": "10483218196001"},
        {"name": "Centre Commercial Partonnax", "street": "12 place des Terreaux", "zip": "69001", "city": "Lyon", "building_type": BuildingType.LOCAL_COMMERCIAL, "company_siret": "89083863704208"},
        {"name": "Tour Horizon", "street": "34 rue de la Bourse", "zip": "69002", "city": "Lyon", "building_type": BuildingType.BATIMENT_TERTIAIRE, "company_siret": "23511615594078"},
        
        # Sites sans entreprise (environ 20%)
        {"name": "Villa Indépendante", "street": "15 rue des Roses", "zip": "69004", "city": "Lyon", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": None},
        {"name": "Maison Particulière", "street": "78 avenue de la République", "zip": "69160", "city": "Tassin-la-Demi-Lune", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": None},
        {"name": "Villa du Parc", "street": "23 chemin du Parc", "zip": "69130", "city": "Ecully", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": None},
        {"name": "Résidence Privée", "street": "45 rue de la Paix", "zip": "69140", "city": "Rillieux-la-Pape", "building_type": BuildingType.RESIDENCE_COLLECTIVE, "company_siret": None},
        {"name": "Maison de Campagne", "street": "67 chemin des Vignes", "zip": "69210", "city": "L'Arbresle", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": None},
        {"name": "Villa Moderne", "street": "89 avenue des Platanes", "zip": "69290", "city": "Craponne", "building_type": BuildingType.MAISON_INDIVIDUELLE, "company_siret": None},
        {"name": "Loft Artistique", "street": "12 rue de l'Art", "zip": "69004", "city": "Lyon", "building_type": BuildingType.AUTRE, "company_siret": None},
        {"name": "Atelier d'Artiste", "street": "34 rue des Artistes", "zip": "69001", "city": "Lyon", "building_type": BuildingType.AUTRE, "company_siret": None},
        {"name": "Studio Créatif", "street": "56 place des Arts", "zip": "69002", "city": "Lyon", "building_type": BuildingType.AUTRE, "company_siret": None},
        {"name": "Espace Culturel", "street": "78 avenue de la Culture", "zip": "69008", "city": "Lyon", "building_type": BuildingType.AUTRE, "company_siret": None},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for site_data in sites_data:
        # Vérifier si le site existe déjà par son nom et adresse
        existing = await Site.query.filter(
            workspace=workspace,
            name=site_data["name"],
            street=site_data["street"]
        ).first()
        
        if existing:
            skipped_count += 1
        else:
            # Récupérer la company si elle existe
            company = None
            company_siret = site_data.pop("company_siret", None)
            
            if company_siret and company_siret in company_sirets:
                company = await Company.query.filter(
                    workspace=workspace,
                    siret=company_siret
                ).first()
            
            # Ajouter le workspace, le pays et la company à la donnée
            site_data["workspace"] = workspace
            site_data["country"] = france
            if company:
                site_data["company"] = company
            
            await Site.query.create(**site_data)
            created_count += 1
    
    console.print(f"[blue]Sites: {created_count} créés, {skipped_count} existants[/blue]") 