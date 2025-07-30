from rich.console import Console
from models.contact import Contact
from models.company import Company
from models.workspace import Workspace
import random

console = Console()


async def init_contacts(workspace: Workspace):
    """Initialise les contacts pour un workspace"""
    console.print("[yellow]Initialisation des contacts...[/yellow]")
    
    # Supprimer tous les contacts existants du workspace
    existing_contacts = await Contact.query.filter(workspace=workspace).all()
    deleted_count = 0
    for contact in existing_contacts:
        await contact.delete()
        deleted_count += 1
    
    if deleted_count > 0:
        console.print(f"[red]  - {deleted_count} contacts existants supprimés[/red]")
    
    contacts_data = [
        {"first_name": "Jean", "last_name": "Martin", "full_name": "Jean Martin", "company_siret": "10483218196001", "email": "j.martin@laurent-fils.fr", "mobile": "06 12 34 56 78", "phone": "01 42 33 44 55", "function": "Directeur général"},
        {"first_name": "Sophie", "last_name": "Dubois", "full_name": "Sophie Dubois", "company_siret": "89083863704208", "email": "s.dubois@auger-delahaye.fr", "mobile": "06 23 45 67 89", "phone": None, "function": "Responsable maintenance"},
        {"first_name": "Pierre", "last_name": "Leclerc", "full_name": "Pierre Leclerc", "company_siret": "23511615594078", "email": "p.leclerc@barre.fr", "mobile": "06 34 56 78 90", "phone": "01 47 88 92 34", "function": "Manager"},
        {"first_name": "Marie", "last_name": "Rousseau", "full_name": "Marie Rousseau", "company_siret": "18499310434119", "email": "m.rousseau@rey-sa.fr", "mobile": None, "phone": "01 53 67 89 01", "function": "Responsable qualité"},
        {"first_name": "Antoine", "last_name": "Bernard", "full_name": "Antoine Bernard", "company_siret": "75255341928327", "email": "a.bernard@gillet.fr", "mobile": "06 45 67 89 01", "phone": "01 48 95 73 26", "function": "Technicien"},
        {"first_name": "François", "last_name": "Lambert", "full_name": "François Lambert", "company_siret": "83503656431395", "email": "f.lambert@weiss.fr", "mobile": "06 56 78 90 12", "phone": "01 44 82 67 39", "function": "Directeur technique"},
        {"first_name": "Sylvie", "last_name": "Moreau", "full_name": "Sylvie Moreau", "company_siret": "67242388495965", "email": "s.moreau@robin.fr", "mobile": "06 67 89 01 23", "phone": "01 49 73 84 52", "function": "Gérante"},
        {"first_name": "Thomas", "last_name": "Durand", "full_name": "Thomas Durand", "company_siret": "87101236916697", "email": "t.durand@lecoq.fr", "mobile": "06 78 90 12 34", "phone": "01 56 91 42 78", "function": "Pharmacien"},
        {"first_name": "Isabelle", "last_name": "Moreau", "full_name": "Isabelle Moreau", "company_siret": None, "email": "i.moreau@gmail.com", "mobile": "06 89 01 23 45", "phone": "01 43 87 65 21", "function": "Ingénieure"},
        {"first_name": "Laurent", "last_name": "Petit", "full_name": "Laurent Petit", "company_siret": "80194514607008", "email": "l.petit@bosson-ledoux.fr", "mobile": "06 90 12 34 56", "phone": "01 48 52 73 94", "function": "Chef de projet"},
        {"first_name": "Julie", "last_name": "Moreau", "full_name": "Julie Moreau", "company_siret": None, "email": "julie.moreau@free.fr", "mobile": "06 11 22 33 44", "phone": None, "function": "Résidente"},
        {"first_name": "Paul", "last_name": "Gardien", "full_name": "Paul Gardien", "company_siret": "14893252880557", "email": "p.gardien@samson.fr", "mobile": "06 55 66 77 88", "phone": "01 23 45 67 89", "function": "Gardien"},
        {"first_name": "Céline", "last_name": "Dupont", "full_name": "Céline Dupont", "company_siret": "54303911718227", "email": "c.dupont@blondel.fr", "mobile": "06 12 98 76 54", "phone": "01 45 67 89 23", "function": "Comptable"},
        {"first_name": "Nicolas", "last_name": "Lemaire", "full_name": "Nicolas Lemaire", "company_siret": "48963834657871", "email": "n.lemaire@mercier-david.fr", "mobile": "06 23 87 65 43", "phone": "01 56 78 90 12", "function": "Responsable commercial"},
        {"first_name": "Estelle", "last_name": "Roux", "full_name": "Estelle Roux", "company_siret": None, "email": "e.roux@orange.fr", "mobile": "06 34 76 54 32", "phone": "01 67 89 01 34", "function": "Consultante"},
        {"first_name": "Maxime", "last_name": "Fournier", "full_name": "Maxime Fournier", "company_siret": "15988399010310", "email": "m.fournier@pereira-fils.fr", "mobile": "06 45 65 43 21", "phone": "01 78 90 12 45", "function": "Ingénieur"},
        {"first_name": "Caroline", "last_name": "Girard", "full_name": "Caroline Girard", "company_siret": "83473829973763", "email": "c.girard@vidal.com", "mobile": "06 56 54 32 10", "phone": "01 89 01 23 56", "function": "Directrice RH"},
        {"first_name": "Alexandre", "last_name": "Mercier", "full_name": "Alexandre Mercier", "company_siret": "65867910551333", "email": "a.mercier@marechal.fr", "mobile": "06 67 43 21 09", "phone": "01 90 12 34 67", "function": "Chef d'équipe"},
        {"first_name": "Sandrine", "last_name": "Durand", "full_name": "Sandrine Durand", "company_siret": None, "email": "s.durand@free.fr", "mobile": "06 78 32 10 98", "phone": None, "function": "Architecte"},
        {"first_name": "Julien", "last_name": "Garnier", "full_name": "Julien Garnier", "company_siret": "26247137810809", "email": "j.garnier@boyer.net", "mobile": "06 89 21 09 87", "phone": "01 12 34 56 78", "function": "Responsable technique"},
        {"first_name": "Nathalie", "last_name": "Fabre", "full_name": "Nathalie Fabre", "company_siret": "67738026064748", "email": "n.fabre@colas.fr", "mobile": "06 90 10 98 76", "phone": "01 23 45 67 89", "function": "Secrétaire générale"},
        {"first_name": "Stéphane", "last_name": "Roussel", "full_name": "Stéphane Roussel", "company_siret": "97234398065009", "email": "s.roussel@payet.com", "mobile": "06 01 09 87 65", "phone": "01 34 56 78 90", "function": "Acheteur"},
        {"first_name": "Valérie", "last_name": "Muller", "full_name": "Valérie Muller", "company_siret": None, "email": "v.muller@gmail.com", "mobile": "06 12 87 65 54", "phone": "01 45 67 89 01", "function": "Freelance"},
        {"first_name": "Fabien", "last_name": "Lefebvre", "full_name": "Fabien Lefebvre", "company_siret": "82081219136193", "email": "f.lefebvre@moulin.fr", "mobile": "06 23 76 54 43", "phone": "01 56 78 90 12", "function": "Développeur"},
        {"first_name": "Patricia", "last_name": "Leroy", "full_name": "Patricia Leroy", "company_siret": "91598856453346", "email": "p.leroy@maillard.com", "mobile": "06 34 65 43 32", "phone": "01 67 89 01 23", "function": "Responsable qualité"},
        {"first_name": "Olivier", "last_name": "Simon", "full_name": "Olivier Simon", "company_siret": None, "email": "o.simon@hotmail.com", "mobile": "06 45 54 32 21", "phone": None, "function": "Consultant"},
        {"first_name": "Amélie", "last_name": "Michel", "full_name": "Amélie Michel", "company_siret": "47510799118384", "email": "a.michel@traore-pichon.fr", "mobile": "06 56 43 21 10", "phone": "01 78 90 12 34", "function": "Chargée de projet"},
        {"first_name": "Christophe", "last_name": "Garcia", "full_name": "Christophe Garcia", "company_siret": "13542794984041", "email": "c.garcia@lacroix.net", "mobile": "06 67 32 10 09", "phone": "01 89 01 23 45", "function": "Responsable maintenance"},
        {"first_name": "Aurélie", "last_name": "David", "full_name": "Aurélie David", "company_siret": "11824463938847", "email": "a.david@bouchet.fr", "mobile": "06 78 21 09 98", "phone": "01 90 12 34 56", "function": "Gestionnaire"},
        {"first_name": "Romain", "last_name": "Thomas", "full_name": "Romain Thomas", "company_siret": None, "email": "r.thomas@yahoo.fr", "mobile": "06 89 10 98 87", "phone": "01 01 23 45 67", "function": "Designer"}
    ]
    
    created_count = 0
    
    for contact_data in contacts_data:
        # Récupérer l'ID de l'entreprise par SIRET si elle existe
        company_id = None
        if contact_data["company_siret"]:
            company = await Company.query.filter(
                workspace=workspace,
                siret=contact_data["company_siret"]
            ).first()
            if company:
                company_id = company.id
                console.print(f"[blue]    - Associé à {company.name} (SIRET: {contact_data['company_siret']})[/blue]")
            else:
                console.print(f"[yellow]    - Entreprise SIRET {contact_data['company_siret']} non trouvée[/yellow]")
        
        await Contact.query.create(
            workspace=workspace,
            first_name=contact_data["first_name"],
            last_name=contact_data["last_name"],
            full_name=contact_data["full_name"],
            email=contact_data["email"],
            mobile=contact_data.get("mobile"),
            phone=contact_data.get("phone"),
            function=contact_data.get("function"),
            company=company_id
        )
        console.print(f"[green]  + {contact_data['first_name']} {contact_data['last_name']} (créé)[/green]")
        created_count += 1
    
    console.print(f"[blue]Contacts: {created_count} créés[/blue]") 