from typing import Any

from edgy import QuerySet
from fastapi import APIRouter
from starlette.requests import Request

from core.api_route_model.params import filter_selected_fields
from core.api_route_model.registry import view_transformer_registry
from core.api_route_model.view_transformer import PrePaginateViewTransformer, GetViewTransformer, GetViewsTransformer
from models.job_activity import JobActivity
from models.job_status import JobStatus
from models.user import User

router = APIRouter(prefix='/job_activities', tags=['job_activities'])


class JobActivityPrePaginateViewTransformer(PrePaginateViewTransformer):
    async def pre_paginate(self, request: Request, query: QuerySet, context: dict[str, Any]) -> QuerySet:
        return query.select_related('created_by')


class JobActivityGetViewsTransformer(GetViewsTransformer):
    async def get_views(self, request: Request, items: list[JobActivity], context: dict[str, Any]) -> None:
        status_ids = set()
        statuses = {}
        operator_ids = set()
        operators = {}
        for item in items:
            if item.field_name == 'status':
                if item.old_value:
                    status_ids.add(int(item.old_value))
                if item.new_value:
                    status_ids.add(int(item.new_value))
            if item.field_name == 'operator':
                if item.old_value:
                    operator_ids.add(int(item.old_value))
                if item.new_value:
                    operator_ids.add(int(item.new_value))

        job_statuses = await JobStatus.query.filter(id__in=status_ids).all()
        for job_status in job_statuses:
            statuses[job_status.id] = filter_selected_fields(job_status, ','.join(['name']))
        context['statuses'] = statuses

        job_operators = await User.query.filter(id__in=operator_ids).all()
        for job_operator in job_operators:
            operators[job_operator.id] = filter_selected_fields(job_operator, ','.join(['name', 'avatar']))
        context['operators'] = operators


class JobActivityGetViewTransformer(GetViewTransformer):
    async def get_view(self, request: Request, item: JobActivity, item_dump: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
        if item.field_name == 'status':
            if item.old_value:
                item_dump['old_status'] = context['statuses'][int(item.old_value)] if int(item.old_value) in context['statuses'] else None
            if item.new_value:
                item_dump['new_status'] = context['statuses'][int(item.new_value)] if int(item.new_value) in context['statuses'] else None

        if item.field_name == 'operator':
            if item.old_value:
                item_dump['old_operator'] = context['operators'][int(item.old_value)] if int(item.old_value) in context['operators'] else None
            if item.new_value:
                item_dump['new_operator'] = context['operators'][int(item.new_value)] if int(item.new_value) in context['operators'] else None

        return item_dump

view_transformer_registry.register_transformer(JobActivityPrePaginateViewTransformer, JobActivity)
view_transformer_registry.register_transformer(JobActivityGetViewsTransformer, JobActivity)
view_transformer_registry.register_transformer(JobActivityGetViewTransformer, JobActivity)
