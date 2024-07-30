from pydantic import BaseModel, validator
from typing import List
from models.repo import Repo

class Org(BaseModel) :
    name: str = "Random"
    scanedRepos : int = None
    startIndex : int = None
    endIndex : int = None
    totalPages : int = None
    repositories : List[Repo] = []