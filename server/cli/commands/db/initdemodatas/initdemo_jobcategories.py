from rich.console import Console
from models.job_category import JobCategory
from models.workspace import Workspace

console = Console()


async def init_job_categories(workspace: Workspace):
    """Initialise les catégories d'intervention pour un workspace"""
    console.print("[yellow]Initialisation des catégories d'intervention...[/yellow]")
    
    job_categories = [
        {"sequence": 1, "color": "#714F82", "name": "Dépannage simple"},
        {"sequence": 2, "color": "#F54740", "name": "Dépannage urgent"},
        {"sequence": 3, "color": "#6187B4", "name": "État des lieux"},
    ]
    
    created_count = 0
    skipped_count = 0
    
    for category_data in job_categories:
        existing = await JobCategory.query.filter(
            workspace=workspace,
            name=category_data["name"]
        ).first()
        
        if existing:
            console.print(f"[yellow]  - {category_data['name']} (existe déjà)[/yellow]")
            skipped_count += 1
        else:
            await JobCategory.query.create(
                workspace=workspace,
                sequence=category_data["sequence"],
                color=category_data["color"],
                name=category_data["name"]
            )
            console.print(f"[green]  + {category_data['name']} (créé)[/green]")
            created_count += 1
    
    console.print(f"[blue]Catégories d'intervention: {created_count} créées, {skipped_count} existantes[/blue]") 