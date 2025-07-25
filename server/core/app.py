from edgy import Database, Registry
from fastapi import FastAPI
from typing import Callable, cast, AsyncContextManager, TypeVar

from core.config import Settings
from core.dependencies import depends

T = TypeVar('T')


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset_presence_on_start = True
        self.warmup_models_cache_on_start = True

    @property
    def settings(self) -> Settings:
        return cast(Settings, self.extra.get('settings'))

    @property
    def db(self) -> Database:
        return cast(Database, self.extra.get('db'))

    @property
    def db_registry(self) -> Registry:
        return cast(Registry, self.extra.get('db_registry'))

    def initialize(self):
        pass


class CliApp:
    def __init__(self, app_factory: Callable[..., App]):
        self._application_factory: Callable[..., App] = app_factory
        self._app: App | None = None

    @property
    def app(self) -> App:
        if self._app is None:
            self._app = self._application_factory()
            self._app.reset_presence_on_start = False
            self._app.warmup_models_cache_on_start = False
        return self._app
    
    @property
    def title(self) -> str:
        return self.app.title
    
    @property
    def settings(self) -> Settings:
        return self.app.settings

    @property
    def db(self) -> Database:
        return self.app.db

    @property
    def db_registry(self) -> Registry:
        return self.app.db_registry

    @property
    def reset_presence_on_start(self):
        return self.app.reset_presence_on_start

    def initialize(self):
        self.app.initialize()

    def lifespan(self) -> AsyncContextManager:
        return self.app.router.lifespan_context(self.app)

    async def depends(self, call: Callable[..., T]) -> T:
        return await depends(self.app, call)
