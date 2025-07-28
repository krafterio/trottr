from rich.console import Console
from models.user import User
from models.workspace_user import WorkspaceUser, WorkspaceUserRole
from models.job_speciality import JobSpeciality
from models.workspace import Workspace
from services.storage import StorageService
import random
import os
from pathlib import Path

console = Console()


async def init_operators(workspace: Workspace):
    """Initialise les opérateurs pour un workspace"""
    console.print("[yellow]Initialisation des opérateurs...[/yellow]")
    
    async def upload_demo_avatar(demo_path: str, storage_service: StorageService, user: User, workspace: Workspace) -> None:
        """Upload un avatar de démonstration en utilisant directement le StorageService"""
        try:
            source_path = Path(demo_path)
            if not source_path.exists():
                return
            
            import uuid
            
            # Lire le fichier
            with open(source_path, "rb") as f:
                content = f.read()
            
            # Générer un nom de fichier unique comme dans StorageService.upload
            ext = source_path.suffix.lstrip('.')
            filename = str(uuid.uuid4()) + f'.{ext}'
            
            # Forcer le chemin avec le workspace_id
            workspace_dir = Path(storage_service.settings.storage_data_path) / str(workspace.id) / "users"
            workspace_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = workspace_dir / filename
            relative_path = f"users/{filename}"
            
            # Écrire le fichier
            with open(file_path, "wb") as f:
                f.write(content)
            
            # Supprimer l'ancien avatar et sauvegarder le nouveau
            await storage_service.delete(user.avatar)
            user.avatar = relative_path
            await user.save()
                
        except Exception as e:
            console.print(f"[red]Erreur lors de l'upload de l'avatar {demo_path}: {e}[/red]")
    
    operators_data = [
        {"name": "Pierre Martin", "email": "pierre.martin@trottr.io", "phone": "06 12 34 56 78", "zone": "Paris", "avatar": "uploads/demo/operators/pierre.png", "specialities": ["Électricité"]},
        {"name": "Marie Dubois", "email": "marie.dubois@trottr.io", "phone": "06 98 76 54 32", "zone": "Île-de-France", "avatar": "uploads/demo/operators/marie.png", "specialities": ["Plomberie"]},
        {"name": "Jean Dupont", "email": "jean.dupont@trottr.io", "phone": "06 45 67 89 12", "zone": "Paris", "avatar": "uploads/demo/operators/jean.png", "specialities": ["Chauffage"]},
        {"name": "Sophie Leroy", "email": "sophie.leroy@trottr.io", "phone": "06 23 45 67 89", "zone": "Île-de-France", "avatar": "uploads/demo/operators/sophie.png", "specialities": ["Climatisation"]},
        {"name": "Thomas Bernard", "email": "thomas.bernard@trottr.io", "phone": "06 78 90 12 34", "zone": "National", "avatar": "uploads/demo/operators/thomas.png", "specialities": ["Généraliste", "Électricité", "Plomberie"]},
        {"name": "Émilie Moreau", "email": "emilie.moreau@trottr.io", "phone": "06 56 78 90 12", "zone": "Paris", "avatar": "uploads/demo/operators/émilie.png", "specialities": ["Électricité"]},
        {"name": "Nicolas Rousseau", "email": "nicolas.rousseau@trottr.io", "phone": "06 34 56 78 90", "zone": "Île-de-France", "avatar": "uploads/demo/operators/nicolas.png", "specialities": ["Plomberie", "Chauffage"]},
        {"name": "Lucie Simon", "email": "lucie.simon@trottr.io", "phone": "06 12 78 90 34", "zone": "Paris", "avatar": "uploads/demo/operators/lucie.png", "specialities": ["Chauffage", "Climatisation"]},
    ]
    
    created_count = 0
    skipped_count = 0
    
    from core.config import get_settings
    from core import context
    settings = get_settings()
    
    context.set_workspace(workspace)
    
    # Debug pour vérifier le contexte
    current_workspace = context.get_workspace()
    console.print(f"[blue]Workspace dans le contexte: {current_workspace.id if current_workspace else 'None'}[/blue]")
    
    storage_service = StorageService(settings)
    
    specialities_cache = {}
    all_specialities = await JobSpeciality.query.filter(workspace=workspace).all()
    for speciality in all_specialities:
        specialities_cache[speciality.name] = speciality
    
    for operator_data in operators_data:
        existing_user = await User.query.filter(email=operator_data["email"]).first()
        
        if existing_user:
            existing_workspace_user = await WorkspaceUser.query.filter(
                workspace=workspace,
                user=existing_user
            ).first()
            
            if existing_workspace_user:
                console.print(f"[yellow]  - {operator_data['name']} (existe déjà)[/yellow]")
                skipped_count += 1
                continue
        
        if not existing_user:
            user = await User.query.create(
                name=operator_data["name"],
                email=operator_data["email"],
                phone=operator_data.get("phone"),
                zone=operator_data.get("zone"),
                password="demo123!",
                is_active=True,
                is_verified=True
            )
            
            if "avatar" in operator_data:
                await upload_demo_avatar(operator_data["avatar"], storage_service, user, workspace)
        else:
            user = existing_user
        
        workspace_user = await WorkspaceUser.query.create(
            workspace=workspace,
            user=user,
            role=WorkspaceUserRole.OPERATOR
        )
        
        if "specialities" in operator_data:
            for speciality_name in operator_data["specialities"]:
                if speciality_name in specialities_cache:
                    await user.job_specialities.add(specialities_cache[speciality_name])
        
        console.print(f"[green]  + {operator_data['name']} (créé)[/green]")
        created_count += 1
    
    console.print(f"[blue]Opérateurs: {created_count} créés, {skipped_count} existants[/blue]") 