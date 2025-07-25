from contextvars import ContextVar, Token

from starlette.requests import Request

from models.user import User
from models.workspace import Workspace
from models.workspace_user import WorkspaceUser


_current_request: ContextVar[Request | None] = ContextVar("current_request", default=None)


def set_request(request: Request | None) -> Token:
    return _current_request.set(request)


def get_request() -> Request | None:
    return _current_request.get()


def reset_request(token: Token) -> None:
    _current_request.reset(token)


def set_user(user: User | None) -> None:
    req = get_request()
    if req:
        req.state.user = user


def get_user() -> User | None:
    req = get_request()

    return req.state.user if req and hasattr(req.state, "user") else None


def set_workspace(workspace: Workspace | None) -> None:
    req = get_request()
    if req:
        req.state.workspace = workspace


def get_workspace() -> Workspace | None:
    req = get_request()

    return req.state.workspace if req and hasattr(req.state, "workspace") else None


def set_workspace_user(workspace_user: WorkspaceUser | None) -> None:
    req = get_request()
    if req:
        req.state.workspace_user = workspace_user


def get_workspace_user() -> WorkspaceUser | None:
    req = get_request()

    return req.state.workspace_user if req and hasattr(req.state, "workspace_user") else None
