from pydantic import BaseModel, validator
from typing import List, Dict, Any

class GithubPR(BaseModel) :
    action : str = None
    number : int = None
    pull_request : Dict[str, Any]
    repository : Dict[str, Any]
    #organization : Dict[str, Any]
    sender : Dict[str, Any]