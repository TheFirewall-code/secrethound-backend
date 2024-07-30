from pydantic import BaseModel, validator
from typing import List

class Secret(BaseModel) :
    Description : str
    StartLine : int
    EndLine : int
    StartColumn : int
    EndColumn : int
    Match : str
    Secret : str
    File : str
    SymlinkFile : str
    Commit : str
    Entropy : float
    Author : str
    Email : str
    Date : str
    Message : str
    Tags : List[str]
    RuleID : str
    Fingerprint : str
