from typing import Type, Callable, TypeVar
from edgy import Model

from core.metadata_model.registry import metadata_model_registry


M = TypeVar('M', bound=Type[Model])


def metadata_model() -> Callable[[M], M]:
    """
    Decorator to mark a model for metadata exposure.

    Returns:
        The decorated model class
    """
    def decorator(model_cls: M) -> M:
        metadata_model_registry.register_model(model_cls)

        return model_cls

    return decorator
