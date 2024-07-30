from pydantic import BaseModel, validator
from typing import List

class WhitelistSecret(BaseModel) :
    Secret: str = "Random"
    OrgScope : bool = None
    Repository : str = "Random"