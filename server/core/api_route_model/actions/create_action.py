"""
Create action for auto-routes.
"""
from typing import Callable, Coroutine, Any

from fastapi import APIRouter, Body
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError, BaseModel
from starlette.requests import Request

from core.api_route_model.actions import BaseApiRouteAction, generate_input_create_model, generate_output_model
from core.api_route_model.params import FieldSelectorHeader, filter_selected_fields

from core.api_route_model.registry import TypeModel, RouteModelActionOptions, view_transformer_registry
from core.api_route_model.view_transformer import GetViewTransformer


class CreateApiRouteAction(BaseApiRouteAction):
    """Action for creating model instance."""
    
    name = "create"
    
    @classmethod
    def register_route(
        cls,
        router: APIRouter,
        model_cls: TypeModel,
        options: RouteModelActionOptions
    ) -> None:
        """Register the create route."""
        router.add_api_route(**{
            "path": "",
            "endpoint": generate_create_item(model_cls),
            "methods": ["POST"],
            "summary": f"Create {model_cls.__name__}",
            "description": f"Create a new {model_cls.__name__} item",
            **options,
        })


def generate_create_item[M = TypeModel](model_cls: M) -> Callable[[Request, M], Coroutine[Any, Any, M]]:
    async def create_item(
            request: Request,
            item_data: generate_input_create_model(model_cls) = Body(...),
            fields: str | None = FieldSelectorHeader(),
    ) -> type[generate_output_model(model_cls)] | dict[str, Any]:
        return await create_item_action(
            request,
            model_cls,
            item_data,
            fields=fields,
        )

    return create_item


async def create_item_action[M = TypeModel](
    request: Request,
    model_cls: M,
    item_data: BaseModel,
    fields: str | None = None,
) -> type[M] | dict[str, Any]:
    try:
        item = model_cls(**item_data.model_dump())
        await item.save()

        item_dump = filter_selected_fields(item, fields)

        for transformer in view_transformer_registry.get_transformers(GetViewTransformer, model_cls):
            item_dump = transformer.get_view(request, item, item_dump)

        return item_dump
    except ValidationError as e:
        raise RequestValidationError(e.errors())
