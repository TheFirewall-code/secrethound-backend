import re
import requests
import subprocess
import os
import json

from models.secret import Secret
from models.repo import Repo
from models.config import Config
from repositories.scanOrgRepo import ScanOrgRepo
from repositories.configRepo import ConfigRepo

class HelperService :
    def __init__(self) :
        config = self.getConfig()
        self.url = config.url
        self.token = config.access_token

    def cloneRepo(self, repo, target_dir):
            
        clone_url = repo['clone_url']
        subprocess.run(["git", "clone", "https://"+ self.token+":x-oauth-basic@"+clone_url[8:]], cwd=target_dir)
        print(f"Cloned {clone_url}")
        
    def runScan( self, repo, target_dir) :
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

    def cloneBranchRepo(repo, branch, target_dir):
            
        clone_url = repo['clone_url']
        subprocess.run(["git", "-b", branch,"clone", clone_url], cwd=target_dir)
        print(f"Cloned {clone_url}")


    def formatData(self, data, name, out) -> Repo :
        try :
            secrets = []

            for secret in data :
                secrets.append(Secret(**secret))
        except Exception as e :
            print(e)
        
        #fetch total no of commits scanned
        totalNoCommits = self.countScanedCommits(out)
        if totalNoCommits == None :
            totalNoCommits = 0
        else :
            totalNoCommits = int(totalNoCommits)
        return Repo(repository=name, totalNoCommits=totalNoCommits, secrets= secrets)


    def cleaner(self, repo_name, target_dir):
        subprocess.call(["rm", "-rf", repo_name], cwd=target_dir)

        response = subprocess.Popen(["rm -f leaks.json"], shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = response.communicate()
        print(out, err)

    def countScanedCommits(self, data):
        # Simulated Popen output
        popen_output =  data

        # Decoding bytes to string
        decoded_output = popen_output.decode('utf-8')

        # Extracting the number of commits scanned
        commits_found = re.search(r'(\d+) commits scanned', decoded_output)

        # Storing the number of commits in a variable
        total_commits = int(commits_found.group(1)) if commits_found else None

        return total_commits

    def getConfig(self) :
        return ConfigRepo().getConfig()
        #TODO
        #return no settings are updated on first call

    def get_repos(self, url, token):
        all_repos = []
        page = 1
        per_page = 100  # Adjust as per your need, maximum value is 100

        headers = {
            "Accept": "application/vnd.github.v3+json",
        }
        headers["Authorization"] = f"Bearer {token}"

        while True:
            params = {
                "page": page,
                "per_page": per_page
            }
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                repos = response.json()
                if not repos:
                    break
                all_repos.extend(repos)
                page += 1
            else:
                raise Exception(f"Error fetching repos: {response.content}")

        return all_repos

    def getTotalRepoCount(self, url, token ) :
        return len(self.get_repos(url, token))


    def repoDetailsWithRepoName(self, repo_list) :

        all_repoList = self.get_repos(self.url, self.token)

        repo_list_details = []

        for repo in all_repoList :
            if repo["name"] in repo_list :
                 repo_list_details.append(repo)

        return repo_list_details