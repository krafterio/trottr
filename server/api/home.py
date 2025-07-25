from fastapi import APIRouter, Depends
from datetime import datetime
from sqlalchemy import func, select

from api.auth import get_current_user
from services.workspace import get_user_workspace
from models.user import User
from models.workspace import Workspace

router = APIRouter(prefix="/home", tags=["home"])
    