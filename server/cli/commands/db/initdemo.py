import cli
from rich.console import Console
from cli.commands.db import db
from core.app import CliApp
from models.workspace import Workspace
from cli.commands.db.initdemodatas.initdemo_contactrelationtype import init_contact_relation_types
from cli.commands.db.initdemodatas.initdemo_jobstatuses import init_job_statuses
from cli.commands.db.initdemodatas.initdemo_jobcategories import init_job_categories
from cli.commands.db.initdemodatas.initdemo_companies import init_companies
from cli.commands.db.initdemodatas.initdemo_sites import init_sites

console = Console()


@db.command()
@cli.argument("workspace", type=int)
@cli.pass_app  
async def init_demo(app: CliApp, workspace: int):
    """Init demo data for specific workspace"""
    async with app.lifespan():
        workspace_obj = await Workspace.query.filter(id=workspace).first()
        if not workspace_obj:
            console.print(f"[red]Workspace avec l'ID {workspace} non trouvé[/red]")
            return

        console.print(f"[blue]Initialisation des données de démo pour le workspace {workspace} ({workspace_obj.name})[/blue]")
        
        await init_contact_relation_types(workspace_obj)
        await init_job_statuses(workspace_obj)
        await init_job_categories(workspace_obj)
        await init_companies(workspace_obj)
        await init_sites(workspace_obj)
        
        console.print(f"[green]Données de démo initialisées avec succès pour le workspace {workspace}[/green]") 