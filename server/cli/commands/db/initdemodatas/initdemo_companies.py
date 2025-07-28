from rich.console import Console
from models.company import Company, CompanyType
from models.workspace import Workspace
from models.country import Country

console = Console()


async def init_companies(workspace: Workspace):
    """Initialise les entreprises pour un workspace"""
    console.print("[yellow]Initialisation des entreprises...[/yellow]")
    
    # Récupération du pays France par défaut
    france = await Country.query.filter(iso_code="FR").first()
    
    companies_data = [
        {"name": "Laurent et Fils", "company_type": CompanyType.REGIE_GESTIONNAIRE, "reference": "CUST-1000", "invoice_street": "10 Rue de la République", "invoice_zip": "69001", "invoice_city": "Lyon", "phone": "01 33 21 91 96", "email": "martinazerite@ray.com", "siret": "10483218196001"},
        {"name": "Auger Delahaye et Fils", "company_type": CompanyType.DONNEUR_ORDRE, "reference": "CUST-1001", "invoice_street": "25 Cours Vitton", "invoice_zip": "69006", "invoice_city": "Lyon", "phone": "02 37 94 02 65", "email": "honorechermortit@army.com", "siret": "89083863704208"},
        {"name": "Barre", "company_type": CompanyType.SOUS_TRAITANT, "reference": "CUST-1002", "invoice_street": "3 Avenue Jean Jaurès", "invoice_zip": "69007", "invoice_city": "Lyon", "phone": "01 07 81 61 84", "email": "hortense31@pettiot.org", "siret": "23511615594078"},
        {"name": "Rey SA", "company_type": CompanyType.DONNEUR_ORDRE, "reference": "CUST-1003", "invoice_street": "42 Rue du Président Edouard Herriot", "invoice_zip": "69002", "invoice_city": "Lyon", "phone": "01 47 52 55 34", "email": "arnaulducp@geotheix.edu", "siret": "18499310434119"},
        {"name": "Gillet", "company_type": CompanyType.DONNEUR_ORDRE, "reference": "CUST-1004", "invoice_street": "7 Rue de la Part-Dieu", "invoice_zip": "69003", "invoice_city": "Lyon", "phone": "01 83 50 30 56", "email": "christophe39@leconte.fr", "siret": "75255341928327"},
        {"name": "Weiss", "company_type": CompanyType.SOUS_TRAITANT, "reference": "CUST-1005", "invoice_street": "5 Rue du Commandant Charcot", "invoice_zip": "69005", "invoice_city": "Lyon", "phone": "05 24 23 38 49", "email": "zguillon@vasseur.net", "siret": "83503656431395"},
        {"name": "Robin", "company_type": CompanyType.REGIE_GESTIONNAIRE, "reference": "CUST-1006", "invoice_street": "33 Rue Marietton", "invoice_zip": "69009", "invoice_city": "Lyon", "phone": "+33 (0)3 12 26 91 66", "email": "gevrard@bazin.com", "siret": "67242388495965"},
        {"name": "Lecoq", "company_type": CompanyType.DONNEUR_ORDRE, "reference": "CUST-1007", "invoice_street": "12 Rue Garibaldi", "invoice_zip": "69006", "invoice_city": "Lyon", "phone": "05 14 62 70 48", "email": "corinneautier@riou.net", "siret": "87101236916697"},
        {"name": "Bosson Ledoux S.A.", "company_type": CompanyType.FOURNISSEUR, "reference": "CUST-1008", "invoice_street": "18 Avenue Félix Faure", "invoice_zip": "80007", "invoice_city": "Lyon", "phone": "+33 (0)1 95 70 15 43", "email": "guillothelene@cheval.fr", "siret": "80194514607008"},
        {"name": "Samson S.A.S.", "company_type": CompanyType.CLIENT_FINAL, "reference": "CUST-1009", "invoice_street": "21 Rue de Marseille", "invoice_zip": "69007", "invoice_city": "Lyon", "phone": "+33 1 27 92 48 96", "email": "atodelaivre@delannoy.fr", "siret": "14893252880557"},
        {"name": "Blondel", "company_type": CompanyType.REGIE_GESTIONNAIRE, "reference": "CUST-1010", "invoice_street": "4 Rue de Cazenove", "invoice_zip": "69008", "invoice_city": "Lyon", "phone": "04 13 31 59 96", "email": "jacquelinevasseur@lefort.com", "siret": "54303911718227"},
        {"name": "Mercier David SARL", "company_type": CompanyType.REGIE_GESTIONNAIRE, "reference": "CUST-1011", "invoice_street": "18 Rue Lortet", "invoice_zip": "69007", "invoice_city": "Lyon", "phone": "+33 (0)4 83 47 38 29", "email": "yberger@cordier.net", "siret": "48963834657871"},
        {"name": "Pereira et Fils", "company_type": CompanyType.CLIENT_FINAL, "reference": "CUST-1012", "invoice_street": "2 Avenue Barthélémy Buyer", "invoice_zip": "69005", "invoice_city": "Lyon", "phone": "03 56 70 10 66", "email": "susanne13@aubert.info", "siret": "15988399010310"},
        {"name": "Vidal", "company_type": CompanyType.CLIENT_FINAL, "reference": "CUST-1013", "invoice_street": "9 Rue Duguesclin", "invoice_zip": "69006", "invoice_city": "Lyon", "phone": "01 73 17 81 08", "email": "morinodette@brun.fr", "siret": "83473829973763"},
        {"name": "Maréchalppe S.A.", "company_type": CompanyType.SOUS_TRAITANT, "reference": "CUST-1014", "invoice_street": "6 Place Bellecour", "invoice_zip": "69002", "invoice_city": "Lyon", "phone": "01 06 47 46 67", "email": "laurentcollet@boyer.com", "siret": "65867910551333"},
        {"name": "Boyer", "company_type": CompanyType.REGIE_GESTIONNAIRE, "reference": "CUST-1015", "invoice_street": "11 Rue Vaubecour", "invoice_zip": "69002", "invoice_city": "Lyon", "phone": "+33 (0)3 97 82 81", "email": "danielvalentin@weber.fr", "siret": "26247137810809"},
        {"name": "Colas S.A.", "company_type": CompanyType.AUTRE, "reference": "CUST-1016", "invoice_street": "15 Rue Franklin", "invoice_zip": "69002", "invoice_city": "Lyon", "phone": "+33 (0)2 91 69 98 54", "email": "margueriteauger@dupuis.org", "siret": "67738026064748"},
        {"name": "Payet", "company_type": CompanyType.FOURNISSEUR, "reference": "CUST-1017", "invoice_street": "27 Rue des Remparts d'Ainay", "invoice_zip": "69002", "invoice_city": "Lyon", "phone": "03 75 17 91 01", "email": "tanguymarcel@pape.fr", "siret": "97234398065009"},
        {"name": "Moulin SARL", "company_type": CompanyType.FOURNISSEUR, "reference": "CUST-1018", "invoice_street": "8 Rue Antoine Lumière", "invoice_zip": "69008", "invoice_city": "Lyon", "phone": "02 27 84 98 08", "email": "margaud12@ferreira.com", "siret": "82081219136193"},
        {"name": "Maillard Carre S.A.S.", "company_type": CompanyType.AUTRE, "reference": "CUST-1019", "invoice_street": "13 Rue du Dauphiné", "invoice_zip": "69003", "invoice_city": "Lyon", "phone": "+33 5 53 48 74 01", "email": "cbaron@kg.org", "siret": "91598856453346"},
        {"name": "Traore Pichon S.A.S.", "company_type": CompanyType.DONNEUR_ORDRE, "reference": "CUST-1020", "invoice_street": "6 Avenue Jean Mermoz", "invoice_zip": "69008", "invoice_city": "Lyon", "phone": "03 80 11 28 05", "email": "aurorerodriguez@le.com", "siret": "47510799118384"},
        {"name": "Lacroix", "company_type": CompanyType.DONNEUR_ORDRE, "reference": "CUST-1021", "invoice_street": "19 Rue du Président Wilson", "invoice_zip": "69100", "invoice_city": "Villeurbanne", "phone": "08 01 58 69 23", "email": "susanneschmitt@laurent.com", "siret": "13542794984041"},
        {"name": "Bouchet", "company_type": CompanyType.CLIENT_FINAL, "reference": "CUST-1022", "invoice_street": "7 Avenue Roger Salengro", "invoice_zip": "69100", "invoice_city": "Villeurbanne", "phone": "08 04 21 60 73", "email": "theresejacques@olivier.fr", "siret": "11824463938847"},
        {"name": "Laurent Detnas S.A.", "company_type": CompanyType.AUTRE, "reference": "CUST-1023", "invoice_street": "23 Rue Léon Blum", "invoice_zip": "69100", "invoice_city": "Villeurbanne", "phone": "01 54 14 58 68", "email": "antoine14@blin.com", "siret": "64005242786801"},
        {"name": "Barre", "company_type": CompanyType.AUTRE, "reference": "CUST-1024", "invoice_street": "14 Rue Gabriel Péri", "invoice_zip": "69100", "invoice_city": "Villeurbanne", "phone": "04 98 16 39 42", "email": "neveubernadette@ledoux.net", "siret": "28059620245505"},
        {"name": "Perret", "company_type": CompanyType.AUTRE, "reference": "CUST-1025", "invoice_street": "4 Avenue Salvador Allende", "invoice_zip": "69200", "invoice_city": "Venissieux", "phone": "04 59 51 48 46", "email": "anne48@olivier.fr", "siret": "31586923226025"},
        {"name": "Chauvet Colas SARL", "company_type": CompanyType.AUTRE, "reference": "CUST-1026", "invoice_street": "29 Rue Gambetta", "invoice_zip": "69230", "invoice_city": "Saint-Genis-Laval", "phone": "01 80 44 36 99", "email": "chantal77@gros.net", "siret": "34216073576431"},
        {"name": "Jacquet S.A.S.", "company_type": CompanyType.FOURNISSEUR, "reference": "CUST-1027", "invoice_street": "10 Chemin des Muriers", "invoice_zip": "69340", "invoice_city": "Francheville", "phone": "06 34 33 20 00", "email": "christellebourdon@pineau.net", "siret": "36541458885014"},
        {"name": "Costa", "company_type": CompanyType.CLIENT_FINAL, "reference": "CUST-1028", "invoice_street": "6 Rue Centrale", "invoice_zip": "69300", "invoice_city": "Caluire-et-Cuire", "phone": "01 32 61 03 28", "email": "jgirard@riviere.fr", "siret": "40196556881693"},
        {"name": "Faivre", "company_type": CompanyType.AUTRE, "reference": "CUST-1029", "invoice_street": "17 Rue du Docteur Bouchut", "invoice_zip": "69110", "invoice_city": "Sainte-Foy-lès-Lyon", "phone": "04 98 68 72 77", "email": "faustde@eme.info", "siret": "60885515951450"},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for company_data in companies_data:
        # Vérifier si la société existe déjà par son SIRET
        existing = await Company.query.filter(
            workspace=workspace,
            siret=company_data["siret"]
        ).first()
        
        if existing:
            skipped_count += 1
        else:
            # Ajouter le workspace et le pays à la donnée
            company_data["workspace"] = workspace
            company_data["invoice_country"] = france
            
            await Company.query.create(**company_data)
            created_count += 1
    
    console.print(f"[blue]Entreprises: {created_count} créées, {skipped_count} existantes[/blue]") 