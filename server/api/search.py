from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
import asyncio
from models.user import User
from api.auth import get_current_user

router = APIRouter()
