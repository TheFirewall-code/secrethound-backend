from pydantic import BaseModel, validator
from typing import List
from enum import Enum


# Enums for constrained values
class AllowedScanType(str, Enum):
    option1 = "Loose"
    option2 = "aggressive"

class AllowedGit(str, Enum) :
    option1 = "github"

class WebhookConfig(BaseModel) :
    git: AllowedGit = None
    scanType: AllowedScanType = None
    PRcomment: str = "Secrets Caught !"
    blockPR: bool = None
    gitActions: List[str] = ["synchronize","opened","reopened"]
    targetRepos: List[str] = ["All"]