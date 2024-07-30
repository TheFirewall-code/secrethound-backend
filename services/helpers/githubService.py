import requests
import os
import subprocess
import json

from models.githubPR import GithubPR
from repositories.configRepo import ConfigRepo
from services.helperWhitelistService import HelperWhitelistSecretService


class GithubService :

    def __init__(self, pr: GithubPR) :
        config = self.getConfig()
        self.token = config.access_token
        self.prNo = pr.pull_request["number"]
        self.repository = pr.repository["name"]
        self.sourceBranch = pr.pull_request['head']['ref']
        self.desitnationBranch = pr.pull_request['base']['ref']
        self.full_reponame = pr.repository["full_name"]
        self.clone_url = pr.repository["clone_url"]
        self.target_dir = os.getcwd() +  "/repoScan"
        self.prLink = pr.pull_request["url"]
        self.prHtmlUrl = pr.pull_request["html_url"]
        self.statusesUrl = pr.pull_request['head']["repo"]["statuses_url"][:-6] +"/"+ pr.pull_request['head']["sha"]
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)
        self.secMap = HelperWhitelistSecretService().filterSecretPRScan(self.repository)
        print("hey-githubservice")

    def getConfig(self) :
        return ConfigRepo().getConfig()

    def findLooseScanFilePath(self) :
        # Your GitHub personal access token
        ACCESS_TOKEN = self.token
        REPO_NAME = self.full_reponame #'your_username/your_repository_name'  # Example: 'octocat/Hello-World'
        PULL_REQUEST_NUMBER = self.prNo  # Change to your pull request number
        API_URL = f'https://api.github.com/repos/{REPO_NAME}/pulls/{PULL_REQUEST_NUMBER}/files'

        # GitHub base URL for constructing file view URLs
        GITHUB_REPO_URL = f'https://github.com/{REPO_NAME}'

        # Set up headers for authorization and response format
        headers = {
            'Authorization': f'token {ACCESS_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Make the request to get the files of the PR
        response = requests.get(API_URL, headers=headers)

        filenameList = {}
        # Check if the request was successful
        if response.status_code == 200:
            files_data = response.json()
            for file in files_data:
                filename = file['filename']
                print(f"File path: {filename}")
                file_url = file["blob_url"]
                filenameList[filename] = file_url
                # Construct and print the URL to view the file on GitHub
                file_url = f"{GITHUB_REPO_URL}/blob/{file['sha']}/{filename}"
                print(f"View on GitHub: {file_url}")
        else:
            print(f"Failed to fetch PR details: {response.status_code}")

        return filenameList

    def cloneRepo(self):
            
        clone_url = self.clone_url
        print("git", "clone", "-b ", self.sourceBranch , " https://"+ self.token+":x-oauth-basic@"+clone_url[8:])
        subprocess.run(["git", "clone", "-b", self.sourceBranch , "https://"+ self.token+":x-oauth-basic@"+clone_url[8:]], cwd=self.target_dir)
        print(f"Cloned {clone_url}")

    def fetchPRCommits(self) :
        # GitHub API URL for fetching PR commits
        url = f"https://api.github.com/repos/{self.full_reponame}/pulls/{self.prNo}/commits"

        # If you're using a personal access token (PAT) for private repos or rate limiting
        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        } if self.token else {"Accept": "application/vnd.github.v3+json"}

        response = requests.get(url, headers=headers)

        commitsList = []
        if response.status_code == 200:
            commits = response.json()
            for commit in commits:
                # Extracting and printing some details about each commit
                print(f"Commit SHA: {commit['sha']}")
                print(f"Author: {commit['commit']['author']['name']}")
                print(f"Date: {commit['commit']['author']['date']}")
                print(f"Message: {commit['commit']['message']}\n")
                commitsList.append(commit['sha'])

        else:
            print(f"Failed to fetch commits: {response.status_code} - {response.text}")
        
        return commitsList

    # Function to fetch and print the diff for a single commit
    def create_commit_diff_file(self, commit_sha, full_filename):
        url = f"https://api.github.com/repos/{self.full_reponame}/commits/{commit_sha}"

        headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        } if self.token else {"Accept": "application/vnd.github.v3+json"}

        response = requests.get(url, headers=headers)
        commitSecretsList = []
        if response.status_code == 200:
            commit_data = response.json()
            # Print commit information
            print(f"Commit: {commit_sha}")
            print(f"Author: {commit_data['commit']['author']['name']}")
            print(f"Date: {commit_data['commit']['author']['date']}")
            print("Changes:")
            
            # Iterate over files in the commit and print the patch/diff
            for file in commit_data['files']:
                scan_temp_data_file = full_filename+"_"+file['filename']+".txt"
                with open(scan_temp_data_file, "w") as f :
                    #print(f"\nFile: {file['filename']}")
                    if 'patch' in file:
                        # Filter and print only added lines
                        for line in file['patch'].split('\n'):
                            if line.startswith('+') and not line.startswith('+++'):
                                print(line[1:])  # Remove the leading '+' to display the line without it
                                f.write(line[1:]+ "\n")

                #scan the file under commit
                response = subprocess.Popen(["sudo trufflehog filesystem "+scan_temp_data_file+" --json"], shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = response.communicate()
                print(out, err)
                
                # if data in out then add commit hash and file name in data
                if out != b'' :
                    out = out.decode("utf-8")
                    out = out.split('\n')
                    for sec in out :
                        if sec :
                            sec = json.loads(sec)
                            #whitelist secret
                            if sec["Raw"] in self.secMap :
                                continue
                            sec["commit_sha"] = commit_sha
                            if not sec["SourceMetadata"]["Data"]["Filesystem"]["line"] :
                                line = 0
                            else : 
                                line = sec["SourceMetadata"]["Data"]["Filesystem"]["line"]
                            sec["secUrl"] = file["blob_url"] + "#L"+ str(line)
                            sec["RepoName"] = g1.repository
                            # apend the date to master json list
                            commitSecretsList.append(sec)
                            print("out :",sec)

                #remove the temp file
                response = subprocess.Popen(["rm "+scan_temp_data_file], shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = response.communicate()
                print("out :" ,out, err)

        else:
            print(f"Failed to fetch commit {commit_sha}: {response.status_code} - {response.text}")
        print("commitSecretsList :", commitSecretsList)
        return commitSecretsList



    def commentPR(self, PRcomment, masterSecretList) :

        token = self.token
        repo = self.full_reponame #'your_username/your_repository_name'  # Example: 'octocat/Hello-World'
        pr_number = self.prNo  # Change to your pull request number
        #API_URL = f'https://api.github.com/repos/{REPO_NAME}/pulls/{PULL_REQUEST_NUMBER}/files'


        # The API URL to post comments on a pull request
        url = f'https://api.github.com/repos/{repo}/issues/{pr_number}/comments'

        # Headers including the authorization token
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
        }
        comment = ""
        for key in masterSecretList :
            comment += key["secUrl"] + "\n"
        # The data to be sent with the post request
        data = {
            'body': PRcomment +"\n\n" + comment 
        }
        # Sending the post request to the GitHub API
        response = requests.post(url, headers=headers, json=data)

        # Checking if the request was successful
        if response.status_code == 201:
            print('Comment posted successfully.')
        else:
            print('Failed to post comment.', response.json())


    def updateStatus(self, status) :
        # Update the status of the commit related to the pull request
        statuses_href = self.statusesUrl
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
        }

        if status == False :
            response_status = requests.post(
                statuses_href,
                headers=headers,
                json={
                    'state': 'failure',
                    'target_url': "",
                    'description': 'Secret caught !',
                    'context': 'Inhouse Secret Hound'
                }
            )
        else :
            response_status = requests.post(
                statuses_href,
                headers=headers,
                json={
                    'state': 'success',
                    'target_url': "",
                    'description': 'No secret found',
                    'context': 'Inhouse Secret Hound'
                }
            )

        if response_status.status_code == 201:
            print('status updated successfully.')
        else:
            print('Failed to post comment.', response_status.json())


