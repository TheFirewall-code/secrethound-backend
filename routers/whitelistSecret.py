from fastapi import APIRouter, Request
from typing import List
from aws_cognito.auth_admin import auth_admin

from models.whitelistSecret import WhitelistSecret
from services.whitelistSecretService import WhitelistSecretService

router = APIRouter()

@router.post("/setWhitelistSecrets")
@auth_admin()
async def whitelistSecrets(request: Request, ListOfSecrets: List[WhitelistSecret]) :
    for whitelistSecrets in ListOfSecrets :
        data = WhitelistSecretService.setWhitelistSecret(whitelistSecrets)
    return data

@router.get("/getWhitelistSecrets")
@auth_admin()
async def getWhitelistSecret(request: Request) :
    data = WhitelistSecretService.getWhitelistSecret()

    return data


@router.post("/removeWhitelistSecrets")
@auth_admin()
async def removeWhitelistSecret(request: Request, blacklist: dict) :
    #blacklist = json.load(blacklist)
    data = WhitelistSecretService.removeWhitelistSecret(blacklist["removeWhitelistSecret"])

    return data






