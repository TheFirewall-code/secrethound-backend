import requests
import subprocess
import os
import json
from threading import Lock

lock = Lock()

from models.secret import Secret
from models.repo import Repo
from models.config import Config
from repositories.scanOrgRepo import ScanOrgRepo
from services.helperService import HelperService
#from repositories.scanOrgRepo import Mongodb

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScanOrgService :

    def __init__(self) :
        self.token = None
        self.url = None



    def fetchOrgDetails(self) :
        config = HelperService()
        self.url = config.url
        self.token = config.token
    '''
    def get_repos(self, org_name):
        #url = f"https://api.github.com/orgs/{org_name}/repos"
        #url = f"https://api.github.com/users/LavleshJ/repos"
        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        response = requests.get(self.url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching repos: {response.content}")
    '''
    def get_repos(self, org_name):
        all_repos = []
        page = 1
        per_page = 100  # Adjust as per your need, maximum value is 100

        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        while True:
            params = {
                "page": page,
                "per_page": per_page
            }
            response = requests.get(self.url, headers=headers, params=params)
            if response.status_code == 200:
                repos = response.json()
                if not repos:
                    break
                all_repos.extend(repos)
                page += 1
            else:
                raise Exception(f"Error fetching repos: {response.content}")

        return all_repos

    def clone_repos(self, repo, target_dir):
            
        clone_url = repo['clone_url']
        subprocess.run(["git", "clone", "https://"+ self.token+":x-oauth-basic@"+clone_url[8:]], cwd=target_dir)
        print(f"Cloned {clone_url}")


    def runScan(self, repo, target_dir) :
        repository = target_dir +"/"+ repo["name"]
        response = subprocess.Popen(["gitleaks --source "+ repository+" detect -f json -r leaks.json"], shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = response.communicate()
        print(out, err)

        if err:
            print("Error:", err.decode())

        # Decode the bytes to string
        out_str = out.decode()

        # Convert the JSON string to a dictionary
        try:
            with open("leaks.json", 'r') as file:
                data = json.load(file)

            return data, out
        except json.JSONDecodeError as e:
            logger.info("Failed to parse JSON:", e)
 
            return {"error": e}
        
    def formatData(self, data, name, out) -> Repo :
        try :
            secrets = []

            for secret in data :
                secrets.append(Secret(**secret))
        except Exception as e :
            print(e)
        
        #fetch total no of commits scanned
        totalNoCommits = HelperService().countScanedCommits(out)
        if totalNoCommits == None :
            totalNoCommits = 0
        else :
            totalNoCommits = int(totalNoCommits)
        return Repo(repository=name, totalNoCommits=totalNoCommits, secrets= secrets)
    

    def scanOrgService(self, org_name) :
        #fetch config
        self.fetchOrgDetails()

        if self.url == None or self.token == None:
            return {"message" : "Update the settings" }

        #TODO
        # get repo list
        repo_list = self.get_repos(org_name)
        #logger.info(repo_list)


        # iterate repo list
        target_dir = os.getcwd() +  "/repoScan"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        db = ScanOrgRepo()

        HardRest = None
        #isntialize new coolection in mongodb
        noDocuments = db.getNoScannedRepo()
        if noDocuments == len(repo_list) or noDocuments == 0 :
            db.orgScanStart()
            HardRest = True
        else :
            db.setLastCollection()
            print("nohard scan")
            HardRest = False

            

        for repo in repo_list :
            with lock :
                if repo["name"] == "genomics-computational-infrastructure" :
                    continue
                #check if repo is already in collection
                if HardRest == False :
                    if db.checkForRepo(repo["name"]) == True :
                        print("continue..")
                        continue

                ## clone the repo
                self.clone_repos(repo, target_dir)
                
                ## run scan
                data, out = self.runScan(repo, target_dir)

                
                ##format data
                repo_data = self.formatData(data, repo["name"], out)
                
                #logger.info(repo_data)
                ## save the data
                db.insertRepoData(repo_data)

                ## delete the repo
                subprocess.call(["rm", "-rf", repo["name"]], cwd=target_dir)
            

