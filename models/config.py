from pydantic import BaseModel, validator
from typing import List


class Config(BaseModel) :
    git: str = None
    access_token: str = None
    url: str = None
    PRcomment: str = None
    blockPR: bool = None
    totalRepos:  int = 0