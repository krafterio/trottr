from abc import ABC, abstractmethod
from typing import Any

from edgy import QuerySet
from pydantic import BaseModel
from starlette.requests import Request

from schemas.base import Pagination


class BaseViewTransformer(ABC):
    """Base class for all view transformers."""
    pass


class PrePaginateViewTransformer(BaseViewTransformer):
    @abstractmethod
    async def pre_paginate(self, request: Request, query: QuerySet, context: dict[str, Any]) -> QuerySet:...


class PostPaginateViewTransformer[M = BaseModel](BaseViewTransformer):
    @abstractmethod
    async def post_paginate(self, request: Request, pagination: Pagination[M], context: dict[str, Any]) -> None:...


class GetViewsTransformer[M = BaseModel](BaseViewTransformer):
    @abstractmethod
    async def get_views(self, request: Request, items: list[M], context: dict[str, Any]) -> None:...


class GetViewTransformer[M = BaseModel](BaseViewTransformer):
    @abstractmethod
    async def get_view(self, request: Request, item: M, item_dump: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:...
