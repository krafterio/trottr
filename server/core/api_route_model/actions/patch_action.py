"""
Patch action for auto-routes.
"""
from typing import Callable, Any, Coroutine

from edgy import ObjectNotFound, QuerySet
from fastapi import APIRouter, HTTPException, Path, Body
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request

from core.api_route_model.actions import BaseApiRouteAction, generate_input_patch_model, generate_output_model
from core.api_route_model.params import FieldSelectorHeader, filter_selected_fields, optimize_query_filter_fields

from core.api_route_model.registry import TypeModel, RouteModelActionOptions, view_transformer_registry
from core.api_route_model.view_transformer import GetViewTransformer


class PatchApiRouteAction(BaseApiRouteAction):
    """Action for patching model instance."""
    
    name = "patch"
    
    @classmethod
    def register_route(
        cls,
        router: APIRouter,
        model_cls: TypeModel,
        options: RouteModelActionOptions
    ) -> None:
        """Register the patch route."""
        router.add_api_route(**{
            "path": "/{item_id}",
            "endpoint": generate_patch_item(model_cls),
            "methods": ["PATCH"],
            "summary": f"Update {model_cls.__name__}",
            "description": f"Update an existing {model_cls.__name__} by its ID",
            **options,
        })


def generate_patch_item[M = TypeModel](model_cls: M) -> Callable[[Request, int, M], Coroutine[Any, Any, M]]:
    async def patch_item(
            request: Request,
            item_id: int = Path(..., description="Item ID"),
            item_data: generate_input_patch_model(model_cls) = Body(),
            fields: str | None = FieldSelectorHeader(),
    ) -> type[generate_output_model(model_cls)] | dict[str, Any]:
        return await patch_item_action(
            request,
            model_cls,
            item_id,
            item_data,
            fields=fields,
        )

    return patch_item


async def patch_item_action[M = TypeModel](
    request: Request,
    model_cls: M,
    item_id: int,
    item_data: type[M],
    query: QuerySet | None = None,
    fields: str | None = None,
) -> type[M] | dict[str, Any]:
    query = query or model_cls.query
    query = query.filter(id=item_id)
    query = optimize_query_filter_fields(query, fields)

    try:
        item = await query.get()

        for key in item_data.model_fields_set:
            setattr(item, key, getattr(item_data, key))

        await item.save()

        item_dump = filter_selected_fields(item, fields)

        for transformer in view_transformer_registry.get_transformers(GetViewTransformer, model_cls):
            item_dump = await transformer.get_view(request, item, item_dump, {})

        return item_dump
    except ObjectNotFound:
        raise HTTPException(status_code=404, detail=f"{model_cls.__name__} not found")
    except ValidationError as e:
        raise RequestValidationError(e.errors())
