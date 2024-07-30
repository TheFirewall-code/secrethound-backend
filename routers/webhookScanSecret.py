from fastapi import APIRouter, BackgroundTasks, Request
from typing import List

from models.githubPR import GithubPR
from services.webhookSecretSService import WebhookSecretSService
from services.helpers.deleteYaml import delete_old_files

router = APIRouter()

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def background_task(githubP:dict):
    delete_old_files()
    WebhookSecretSService().startScan(githubP)
    return {"message": "Scan done"}


@router.post("/webhookScanSecret")
async def secretScan(request: Request, githubP:dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task, githubP)
    
    # Return a 200 response immediately
    return {"message": "Proccessing PR"}


@router.get("/prScanSecret")
#@auth_admin()
async def prScanSecret(request: Request) :
    return WebhookSecretSService().getScanData()


@router.get("/fetchScanFile")
async def fetchScanFile(date_of_scan) :
    if date_of_scan:
        return WebhookSecretSService().getSecretFile(date_of_scan)
    return {"message": "No search query provided"}



