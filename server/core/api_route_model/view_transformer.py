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
    def pre_paginate(self, request: Request, query: QuerySet) -> None:...


class PostPaginateViewTransformer[M = BaseModel](BaseViewTransformer):
    @abstractmethod
    def post_paginate(self, request: Request, pagination: Pagination[M]) -> None:...


class GetViewTransformer[M = BaseModel](BaseViewTransformer):
    @abstractmethod
    def get_view(self, request: Request, item: M, item_dump: dict[str, Any]) -> dict[str, Any]:...
