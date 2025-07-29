"""
Get action for auto-routes.
"""
from typing import Callable, Coroutine, Any

from edgy import ObjectNotFound, QuerySet
from fastapi import APIRouter, HTTPException, Path
from starlette.requests import Request

from core.api_route_model.actions import BaseApiRouteAction, generate_output_model
from core.api_route_model.params import FieldSelectorHeader, filter_selected_fields, optimize_query_filter_fields

from core.api_route_model.registry import TypeModel, RouteModelActionOptions, view_transformer_registry
from core.api_route_model.view_transformer import GetViewTransformer


class GetApiRouteAction(BaseApiRouteAction):
    """Action for retrieveing model instance."""
    
    name = "get"
    
    @classmethod
    def register_route(
        cls,
        router: APIRouter,
        model_cls: TypeModel,
        options: RouteModelActionOptions
    ) -> None:
        """Register the get route."""
        router.add_api_route(**{
            "path": "/{item_id}",
            "endpoint": generate_get_item(model_cls),
            "methods": ["GET"],
            "summary": f"Get {model_cls.__name__}",
            "description": f"Retrieve a single {model_cls.__name__} by its ID",
            **options,
        })


def generate_get_item[M = TypeModel](model_cls: M) -> Callable[[Request, int], Coroutine[Any, Any, M]]:
    async def get_item(
            request: Request,
            item_id: int = Path(..., description="Item ID"),
            fields: str | None = FieldSelectorHeader(),
    ) -> type[generate_output_model(model_cls)] | dict[str, Any]:
        return await get_item_action(
            request,
            model_cls,
            item_id,
            fields=fields,
        )

    return get_item


async def get_item_action[M = TypeModel](
    request: Request,
    model_cls: M,
    item_id: int,
    query: QuerySet | None = None,
    fields: str | None = None,
) -> type[M] | dict[str, Any]:
    query = query or model_cls.query
    query = query.filter(id=item_id)
    query = optimize_query_filter_fields(query, fields)

    try:
        item = await query.get()
        item_dump = filter_selected_fields(item, fields)

        for transformer in view_transformer_registry.get_transformers(GetViewTransformer, model_cls):
            item_dump = transformer.get_view(request, item, item_dump)

        return item_dump
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"{model_cls.__name__} not found")
