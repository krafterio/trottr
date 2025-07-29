from typing import Type, Callable, TypeVar
from edgy import Model

from core.api_route_model.registry import route_model_registry, admin_route_model_registry, RouteModelOptions


M = TypeVar('M', bound=Type[Model])


def api_route_model(
    **kwargs: RouteModelOptions,
) -> Callable[[M], M]:
    """
    Decorator to mark a model for auto-generating API routes.

    Args:
        **kwargs: Map of standard endpoint types to be enabled or disabled

    Returns:
        The decorated model class
    """
    def decorator(model_cls: M) -> M:
        route_model_registry.register_model(model_cls, kwargs)

        return model_cls

    return decorator


def admin_api_route_model(
    **kwargs: RouteModelOptions,
) -> Callable[[M], M]:
    """
    Decorator to mark a model for auto-generating API routes for admin-users.

    Args:
        **kwargs: Map of standard endpoint types to be enabled or disabled

    Returns:
        The decorated model class
    """
    def decorator(model_cls: M) -> M:
        admin_route_model_registry.register_model(model_cls, kwargs)

        return model_cls

    return decorator
