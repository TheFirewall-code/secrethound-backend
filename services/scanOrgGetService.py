import requests
import subprocess
import os
import json

from models.secret import Secret
from models.repo import Repo
from services.helperWhitelistService import HelperWhitelistSecretService
from repositories.scanOrgRepo import ScanOrgRepo
#from repositories.scanOrgRepo import Mongodb

import logging

# Configure logging
logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)



class ScanOrgGetService :

    def getScanOrg(start_index, end_index, keyword, sort) :
        return ScanOrgRepo().fetchOrgData(start_index, end_index, keyword, sort)
        #return HelperWhitelistSecretService.feedRealSecret(ScanOrgRepo().fetchOrgData())
