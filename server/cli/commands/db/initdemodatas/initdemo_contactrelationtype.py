from rich.console import Console
from models.contact_relation_type import ContactRelationType
from models.workspace import Workspace

console = Console()


async def init_contact_relation_types(workspace: Workspace):
    """Initialise les types de relations contact pour un workspace"""
    console.print("[yellow]Initialisation des types de relations contact...[/yellow]")
    
    relation_types = [
        {"sequence": 1, "name": "Responsable site"},
        {"sequence": 2, "name": "Propriétaire"},
        {"sequence": 3, "name": "Occupant"},
        {"sequence": 4, "name": "Gestionnaire"},
        {"sequence": 5, "name": "Gardien / Agent local"},
        {"sequence": 6, "name": "Chargé d'exploitation"},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for relation_data in relation_types:
        existing = await ContactRelationType.query.filter(
            workspace=workspace,
            name=relation_data["name"]
        ).first()
        
        if existing:
            console.print(f"[yellow]  - {relation_data['name']} (existe déjà)[/yellow]")
            skipped_count += 1
        else:
            await ContactRelationType.query.create(
                workspace=workspace,
                sequence=relation_data["sequence"],
                name=relation_data["name"]
            )
            console.print(f"[green]  + {relation_data['name']} (créé)[/green]")
            created_count += 1
    
    console.print(f"[blue]Types de relations contact: {created_count} créés, {skipped_count} existants[/blue]") 