from rich.console import Console
from models.job_status import JobStatus
from models.workspace import Workspace

console = Console()


async def init_job_statuses(workspace: Workspace):
    """Initialise les statuts d'intervention pour un workspace"""
    console.print("[yellow]Initialisation des statuts d'intervention...[/yellow]")
    
    job_statuses = [
        {"sequence": 1, "color": "#bfbfbf", "name": "Brouillon"},
        {"sequence": 2, "color": "#6187B4", "name": "Confirmé"},
        {"sequence": 3, "color": "#A7E00A", "name": "Planifié"},
        {"sequence": 4, "color": "#e59303", "name": "En cours"},
        {"sequence": 5, "color": "#5DB451", "name": "Effectué"},
        {"sequence": 6, "color": "#F54740", "name": "Annulé"},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for status_data in job_statuses:
        existing = await JobStatus.query.filter(
            workspace=workspace,
            name=status_data["name"]
        ).first()
        
        if existing:
            console.print(f"[yellow]  - {status_data['name']} (existe déjà)[/yellow]")
            skipped_count += 1
        else:
            await JobStatus.query.create(
                workspace=workspace,
                sequence=status_data["sequence"],
                color=status_data["color"],
                name=status_data["name"]
            )
            console.print(f"[green]  + {status_data['name']} (créé)[/green]")
            created_count += 1
    
    console.print(f"[blue]Statuts d'intervention: {created_count} créés, {skipped_count} existants[/blue]") 