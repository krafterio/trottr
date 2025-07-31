"""
List action for auto-routes.
"""
from typing import Callable, Coroutine, Any, cast

from edgy import QuerySet
from fastapi import APIRouter, Query, HTTPException
from starlette.requests import Request

from core.api_route_model.actions import BaseApiRouteAction, generate_output_model
from core.api_route_model.params import inject_order_by, OrderByQuery, FieldSelectorHeader, filter_selected_fields, \
    optimize_query_filter_fields, FilterHeader, filter_query, InvalidFilterError

from core.api_route_model.registry import TypeModel, RouteModelActionOptions, view_transformer_registry
from core.api_route_model.view_transformer import PrePaginateViewTransformer, PostPaginateViewTransformer, \
    GetViewTransformer, GetViewsTransformer
from schemas.base import Pagination


class ListApiRouteAction(BaseApiRouteAction):
    """Action for listing model instances."""

    name = "list"

    @classmethod
    def register_route(
        cls,
        router: APIRouter,
        model_cls: TypeModel,
        options: RouteModelActionOptions
    ) -> None:
        """Register the list route."""
        router.add_api_route(**{
            "path": "",
            "endpoint": generate_list_items(model_cls),
            "methods": ["GET"],
            "summary": f"List {model_cls.__name__} items",
            "description": f"Retrieve a paginated list of {model_cls.__name__} items",
            **options,
        })


def generate_list_items[M = TypeModel](model_cls: type[M]) -> Callable[[Request, int, int, str, str], Coroutine[Any, Any, Pagination[M]]]:
    async def list_items(
            request: Request,
            limit: int = Query(50, ge=1, le=1000),
            offset: int = Query(0, ge=0),
            order_by: str | None = OrderByQuery(),
            fields: str | None = FieldSelectorHeader(),
            filters: str | None = FilterHeader(),
    ) -> Pagination[type[generate_output_model(model_cls)] | dict[str, Any]]:
        return await list_items_action(
            request,
            model_cls,
            limit=limit,
            offset=offset,
            order_by=order_by,
            fields=fields,
            filters=filters,
        )

    return list_items


async def list_items_action[M = TypeModel](
    request: Request,
    model_cls: type[M],
    query: QuerySet | None = None,
    limit: int = None,
    offset: int = 0,
    order_by: str | None = None,
    fields: str | None = None,
    filters: str | None = None,
) -> Pagination[type[M] | dict[str, Any]]:
    context: dict[str, Any] = {}

    try:
        query = query or model_cls.query
        query = filter_query(query, filters)
        query = inject_order_by(query, order_by)
        query = optimize_query_filter_fields(query, fields)

        for transformer in view_transformer_registry.get_transformers(PrePaginateViewTransformer, model_cls):
            query = await transformer.pre_paginate(request, query, context)

        total = await query.count()
        items = await query.limit(limit).offset(offset).all()
    except InvalidFilterError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        if filters:
            raise HTTPException(status_code=422, detail='Invalid filters')
        else:
            raise e

    for transformer in view_transformer_registry.get_transformers(GetViewsTransformer, model_cls):
        await transformer.get_views(request, items, context)

    result_items = []

    for item in items:
        item_dump = filter_selected_fields(item, fields)

        for transformer in view_transformer_registry.get_transformers(GetViewTransformer, model_cls):
            item_dump = await transformer.get_view(request, item, item_dump, context)

        result_items.append(item_dump)

    result = Pagination(
        items=result_items,
        total=total,
        limit=limit,
        offset=offset,
    )

    for transformer in view_transformer_registry.get_transformers(PostPaginateViewTransformer, model_cls):
        await transformer.post_paginate(request, result, context)

    return cast(Pagination[type[M]], result)
