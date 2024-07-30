from fastapi import APIRouter, Request
from models.config import Config
from aws_cognito.auth import auth_required
from aws_cognito.auth_admin import auth_admin
from services.helpers.logService import LogService
router = APIRouter()

@router.get("/getLogs")
@auth_admin()
async def getLogs(request: Request, start_index: int= 0, end_index: int=10) :
    return LogService.getLogs(start_index, end_index)