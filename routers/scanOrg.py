from fastapi import APIRouter, BackgroundTasks, Request
from services.scanOrgService import ScanOrgService
from services.scanOrgGetService import ScanOrgGetService
from aws_cognito.auth import auth_required
from aws_cognito.auth_admin import auth_admin

router = APIRouter()

scan_in_progress = False
#this api will take some to execute fully
# Exising scan is running - then just return a string to user, don't execute logic
# Cancel an existing scan - user

def background_task():
    # Simulate a task that takes 2 minutes
    # Your actual task processing code goes here
    global scan_in_progress
    if scan_in_progress == True :
        return {"message": "Scan is still running, please wait."}
    
    scan_in_progress = True
    try : 
        ScanOrgService().scanOrgService("xyz")
        return {"message": "Scan Done"}
    except Exception as e : 
        return {"message": "Scan Failed " + str(e) }
    finally :
        scan_in_progress = False


@router.post("/scanOrg")
@auth_admin()
async def scanOrg(request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task)
    
    # Return a 200 response immediately
    return {"message": "Scan processing started in the background"}



@router.get("/getOrgScan")
@auth_required()
async def getOrgScan(request: Request, start_index: int = 0 , end_index: int= 10, keyword: str="", sort: bool=False) :
    return ScanOrgGetService.getScanOrg(int(start_index), int(end_index), keyword, sort)


#cancel api
@router.get("/cancelScan")
async def cancelScan() :
    return True
