from core.api_route_model.actions import api_route_action_registry
from core.api_route_model.actions.create_action import CreateApiRouteAction
from core.api_route_model.actions.delete_action import DeleteApiRouteAction
from core.api_route_model.actions.export_action import ExportApiRouteAction
from core.api_route_model.actions.get_action import GetApiRouteAction
from core.api_route_model.actions.list_action import ListApiRouteAction
from core.api_route_model.actions.patch_action import PatchApiRouteAction


def register_standard_api_route_model_actions():
    """Register all standard api route model actions."""
    api_route_action_registry.register_action(ListApiRouteAction)
    api_route_action_registry.register_action(ExportApiRouteAction)
    api_route_action_registry.register_action(GetApiRouteAction)
    api_route_action_registry.register_action(CreateApiRouteAction)
    api_route_action_registry.register_action(PatchApiRouteAction)
    api_route_action_registry.register_action(DeleteApiRouteAction)
