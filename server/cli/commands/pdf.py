from starlette.requests import Request

import cli
from core import context

from core.app import CliApp
from services.pdf_generator import PdfGenerator
from models.user import User
from models.workspace_user import WorkspaceUser


@cli.command()
@cli.argument('user_email', type=str)
@cli.pass_app
async def pdf_test(app: CliApp, user_email: str = None):
    """Generate PDF for test"""
    cli.echo("Generating PDF for test with user {}".format(user_email))

    async with app.lifespan():
        user_obj = await User.query.filter(email=user_email).first()
        if not user_obj:
            cli.echo(f"❌ Utilisateur non trouvé avec l'email: {user_email}", err=True)
            return

        workspace_user = await WorkspaceUser.query.select_related("workspace").filter(user=user_obj).first()
        if not workspace_user:
            cli.echo(f"❌ Aucun workspace trouvé pour l'utilisateur: {user_email}", err=True)
            return

        workspace = workspace_user.workspace
        cli.echo(f"✅ Utilisateur trouvé: {user_obj.name} ({user_obj.email})")
        cli.echo(f"✅ Workspace: {workspace.name}")

        context.set_request(Request({
            "type": "http",
            "method": "GET",
            "path": "/",
            "query_string": b"",
            "headers": [],
        }))
        context.set_user(user_obj)
        context.set_workspace(workspace)
        context.set_workspace_user(workspace_user)

        test_context = {
            'title': 'Document de Test PDF',
            'company_name': 'Trottr SaaS',
            'date': '2024-01-15',
            'client_name': 'Société Test Client',
            'project_name': 'Projet de démonstration',
            'items': [
                {'name': 'Service 1', 'description': 'Description du service 1', 'quantity': 2, 'price': 150.0},
                {'name': 'Service 2', 'description': 'Description du service 2', 'quantity': 1, 'price': 300.0},
                {'name': 'Service 3', 'description': 'Description du service 3', 'quantity': 3, 'price': 75.0},
            ]
        }

        pdf_generator = await app.depends(PdfGenerator)
        file = await pdf_generator.generate('test.html', test_context)

        cli.echo(f"✅ PDF généré : {file}")
