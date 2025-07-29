"""
Route registration and initialization for auto-generated API endpoints.
"""
import logging

from fastapi import APIRouter
from core.api_route_model.generator import get_all_generated_routers, get_all_generated_admin_routers


logger = logging.getLogger('api_route_model.router')


def register_api_route_models(api_router: APIRouter) -> None:
    """
    Register all generated routes in the FastAPI application.

    Args:
        api_router: The FastAPI router
    """
    # Get all generated routers
    routers = get_all_generated_routers()

    for prefix, router in routers.items():
        logger.debug(f"Adding model router with prefix: {prefix}")
        api_router.include_router(router, prefix=prefix)


def register_admin_api_route_models(api_router: APIRouter) -> None:
    """
    Register all generated routes in the FastAPI application for admin-users.

    Args:
        api_router: The FastAPI router
    """
    # Get all generated routers
    routers = get_all_generated_admin_routers()

    for prefix, router in routers.items():
        logger.debug(f"Adding model router with prefix: {prefix}")
        api_router.include_router(router, prefix=prefix)
