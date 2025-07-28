import logging
import os
import sys
import importlib

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from edgy import Instance, monkay
from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

from api import auth, account
from api.auth import get_current_user
from api.workspace import router as workspace_router
from api.health import router as health_router
from api.users import router as users_router
from api.storage import router as storage_router
from api.websocket import router as websocket_router
from api.presence import router as presence_router
from api.search import router as search_router
from api.webhooks import router as webhooks_router

from api.admin import router as admin_router
from api.import_data import router as import_router
from api.recaptcha import router as recaptcha_router
from api.country import router as country_router
from api.job_status import router as job_status_router
from api.job_category import router as job_category_router
from api.job_speciality import router as job_speciality_router
from api.contact_relation_type import router as contact_relation_type_router
from api.operators import router as operators_router
from api.company import router as company_router
from api.contact import router as contact_router
from api.site import router as site_router
from api.job import router as job_router
from core.app import App
from core.config import get_settings
from core.database import database, registry
from core.http import ContextRequestMiddleware
from core.logger import setup_logging
from services.presence import presence_service
from services.user import is_superuser
from services.workspace import get_user_workspace


load_dotenv()
logger = logging.getLogger("main")


def build_path():
    site_root = os.path.dirname(os.path.realpath(__file__))

    if site_root not in sys.path:
        sys.path.append(site_root)
        sys.path.append(os.path.join(site_root, "models"))


def load_models():
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    logger.debug(f"Loading models from {models_dir}")

    for filename in os.listdir(models_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove .py extension
            logger.debug(f"Importing model {module_name}")
            importlib.import_module(f"models.{module_name}")


async def warmup_models_cache():
    for model in registry.models.values():
        if not model.meta.abstract:
            model.query.get_queryset()
            await model.query.first()


@asynccontextmanager
async def lifespan(application: App):
    logger.debug("Connecting to database")
    await application.db.connect()

    if application.warmup_models_cache_on_start:
        logger.info("Warming up models cache")
        await warmup_models_cache()

    if application.reset_presence_on_start:
        logger.debug("Starting presence service cleanup task")
        await presence_service.start_cleanup_task()
        await presence_service.reset_all_presence_statuses()

    try:
        yield
    finally:
        if application.reset_presence_on_start:
            logger.debug("Stopping presence service cleanup task")
            await presence_service.stop_cleanup_task()

        logger.debug("Closing database connection")
        try:
            await application.db.disconnect()   
        except Exception:
            logger.error("Failed to close database connection")


def app(app_class: type[App] = App) -> App:
    settings = get_settings()

    setup_logging(
        level=settings.log_level, 
        output=settings.log_output, 
        format=settings.log_format,
        log_file=settings.log_file_path,
    )

    logger.debug("Initializing application")
    build_path()
    load_models()

    monkay.set_instance(Instance(registry=registry), apply_extensions=False)
    monkay.evaluate_settings(on_conflict="keep")

    application = app_class(
        title=settings.title,
        lifespan=lifespan,
        settings=settings,
        db=database,
        db_registry=registry,
        redirect_slashes=False,
    )

    monkay.set_instance(Instance(registry=registry, app=application))

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(ContextRequestMiddleware)

    public_api_router = APIRouter()
    api_router = APIRouter(dependencies=[
        Depends(get_current_user),
        Depends(get_user_workspace),
    ])
    admin_api_router = APIRouter(dependencies=[
        Depends(get_current_user),
        is_superuser(),
    ])
    
    # Public API routers
    public_api_router.include_router(health_router, tags=["health"])
    public_api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
    public_api_router.include_router(websocket_router, tags=["websocket"])
    public_api_router.include_router(webhooks_router, tags=["webhooks"])
    public_api_router.include_router(recaptcha_router, tags=["recaptcha"])
    
    # API routers
    api_router.include_router(account.router, prefix="/account", tags=["account"])
    api_router.include_router(workspace_router, prefix="/workspace", tags=["workspace"])
    api_router.include_router(users_router, prefix="/users", tags=["users"])
    api_router.include_router(storage_router, tags=["storage"])
    api_router.include_router(country_router, prefix="/countries", tags=["country"])
    api_router.include_router(job_status_router, prefix="/job-status", tags=["job-status"])
    api_router.include_router(job_category_router, prefix="/job-category", tags=["job-category"])
    api_router.include_router(contact_relation_type_router, prefix="/contact-relation-type", tags=["contact-relation-type"])
    api_router.include_router(job_speciality_router, prefix="/job-speciality", tags=["job-speciality"])
    api_router.include_router(operators_router, prefix="/operators", tags=["operators"])
    api_router.include_router(company_router, prefix="/companies", tags=["company"])
    api_router.include_router(contact_router, prefix="/contacts", tags=["contact"])
    api_router.include_router(site_router, prefix="/sites", tags=["site"])
    api_router.include_router(job_router, prefix="/jobs", tags=["job"])
    api_router.include_router(presence_router, tags=["presence"])
    api_router.include_router(search_router, prefix="/search", tags=["search"])
    api_router.include_router(import_router, prefix="/import", tags=["import"])

    # Admin API routers
    admin_api_router.include_router(admin_router, prefix="/admin", tags=["admin"], include_in_schema=settings.debug_admin)

    # Main routers
    application.include_router(public_api_router, prefix="/api")
    application.include_router(api_router, prefix="/api")
    application.include_router(admin_api_router, prefix="/api")

    logger.debug("Application ready")

    return application
