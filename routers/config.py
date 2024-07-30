from fastapi import APIRouter, Request
from models.config import Config
from services.configService import ConfigService
router = APIRouter()

@router.post("/settings")
#@auth_required()
async def changeConfig(request: Request, config : Config):
    reponse = ConfigService.insertConfig(config)
    return reponse


@router.get("/settings")
#@auth_admin()
async def getConfig(request: Request):
    config = ConfigService.getConfig()
    if config.access_token == None :
        return config
    config.access_token = config.access_token[0:14] + "xxxxxxxxxx" + config.access_token[26:39]

    return config