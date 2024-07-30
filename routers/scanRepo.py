from fastapi import APIRouter, Request
from typing import List

from services.scanRepoService import ScanRepoService

router = APIRouter()

@router.post("/scanRepo")
#@auth_admin()
async def repoScan(request: Request, Repos: List[str]):
    ScanRepoService.scanRepoList(Repos)
    return {"message": "Scan done"}


@router.post("/newRepo")
async def repoScan(gitRawData: dict):
    Repo = ScanRepoService.getRepoList(gitRawData)
    if Repo != None :
        ScanRepoService.scanRepoList(Repo)

    return {"message": "Scan done"}