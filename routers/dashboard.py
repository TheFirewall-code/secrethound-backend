from fastapi import APIRouter, Request
from services.dashboardService import DashboardService
#from aws_cognito.auth import auth_required
router = APIRouter()

@router.get("/getDash")
#@auth_required()
async def getDashboard(request: Request,start_index: int= 0, end_index: int=10) :
    return DashboardService.getDash(start_index, end_index)