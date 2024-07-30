from pydantic import BaseModel, validator
from typing import List
from models.secret import Secret


class Repo(BaseModel) :
    repository : str
    totalNoCommits : int = None
    secrets : List[Secret] = []