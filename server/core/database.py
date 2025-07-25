from functools import lru_cache

from edgy import Database, Registry
from core.config import get_settings

settings = get_settings()

database = Database(
    settings.database_url,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow,
)

@lru_cache()
def get_database_registry():
    return Registry(database=database)


registry = get_database_registry()
