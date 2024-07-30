from fastapi import APIRouter, Request
from models.webhookConfig import WebhookConfig
from services.webhookConfigService import WebhookConfigService
router = APIRouter()

@router.post("/webhookConfig")
#@auth_admin()
async def changeConfig(request: Request, webhookConfig : WebhookConfig):
    response = WebhookConfigService.insertConfig(webhookConfig)
    return response


@router.get("/webhookConfig")
#@auth_admin()
async def getConfig(request: Request):
    webhookConfig =  WebhookConfigService.getConfig()
    
    return webhookConfig