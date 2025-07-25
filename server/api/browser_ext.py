from fastapi import APIRouter, Depends, Query, BackgroundTasks

from api.auth import get_current_user
from schemas.base import List
from services.storage import StorageService


router = APIRouter()
