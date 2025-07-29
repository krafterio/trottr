"""
Delete action for auto-routes.
"""
from typing import Callable, Any, Coroutine

from edgy import ObjectNotFound, QuerySet
from fastapi import APIRouter, HTTPException, Path

from core.api_route_model.actions import BaseApiRouteAction

from core.api_route_model.registry import TypeModel, RouteModelActionOptions


class DeleteApiRouteAction(BaseApiRouteAction):
    """Action for deleting model instance."""
    
    name = "delete"
    
    @classmethod
    def register_route(
        cls,
        router: APIRouter,
        model_cls: TypeModel,
        options: RouteModelActionOptions
    ) -> None:
        """Register the delete route."""
        router.add_api_route(**{
            "path": "/{item_id}",
            "endpoint": generate_delete_item(model_cls),
            "methods": ["DELETE"],
            "summary": f"Delete {model_cls.__name__}",
            "description": f"Delete a {model_cls.__name__} by its ID",
            "status_code": 204,
            **options,
        })


def generate_delete_item[M = TypeModel](model_cls: M) -> Callable[[int], Coroutine[Any, Any, None]]:
    async def delete_item(
            item_id: int = Path(..., description="Item ID"),
    ) -> None:
        return await delete_item_action(
            model_cls,
            item_id,
        )

    return delete_item


async def delete_item_action[M = TypeModel](
    model_cls: M,
    item_id: int,
    query: QuerySet | None = None,
    not_found_message: str = "Enregistrement non trouvé",
) -> None:
    try:
        query = query or model_cls.query
        item = await query.filter(id=item_id).get()
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=not_found_message)

    await item.delete()

    return None
