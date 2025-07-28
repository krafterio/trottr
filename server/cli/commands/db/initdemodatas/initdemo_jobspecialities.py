from rich.console import Console
from models.job_speciality import JobSpeciality
from models.workspace import Workspace

console = Console()


async def init_job_specialities(workspace: Workspace):
    """Initialise les spécialités d'opérateur pour un workspace"""
    console.print("[yellow]Initialisation des spécialités d'opérateur...[/yellow]")
    
    job_specialities = [
        {"sequence": 1, "color": "#A7E00A", "name": "Électricité"},
        {"sequence": 2, "color": "#6187B4", "name": "Plomberie"},
        {"sequence": 3, "color": "#C2433A", "name": "Chauffage"},
        {"sequence": 4, "color": "#bfbfbf", "name": "Climatisation"},
        {"sequence": 5, "color": "#343731", "name": "Généraliste"},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for speciality_data in job_specialities:
        existing = await JobSpeciality.query.filter(
            workspace=workspace,
            name=speciality_data["name"]
        ).first()
        
        if existing:
            console.print(f"[yellow]  - {speciality_data['name']} (existe déjà)[/yellow]")
            skipped_count += 1
        else:
            await JobSpeciality.query.create(
                workspace=workspace,
                sequence=speciality_data["sequence"],
                color=speciality_data["color"],
                name=speciality_data["name"]
            )
            console.print(f"[green]  + {speciality_data['name']} (créé)[/green]")
            created_count += 1
    
    console.print(f"[blue]Spécialités d'opérateur: {created_count} créées, {skipped_count} existantes[/blue]") 