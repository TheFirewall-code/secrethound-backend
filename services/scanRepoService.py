import requests
import os
from services.helperService import HelperService
from repositories.scanRepoRepo import ScanRepoRepo


class ScanRepoService :

    def getRepoList(gitRawData) :
        with open("gitData.txt", "w") as f :
            f.write(str(gitRawData))
        print(gitRawData)
        if gitRawData["action"] == "created" :
            return [gitRawData["repository"]["name"]]
        return None

    def scanRepoList(repo_list) :
        db = ScanRepoRepo()

        target_dir = os.getcwd() +  "/repoScan"
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        h1 = HelperService()

        repo_list_details = h1.repoDetailsWithRepoName(repo_list)


        for repo in repo_list_details :

            ## clone the repo
            h1.cloneRepo(repo, target_dir)
            
            ## run scan
            data, out = h1.runScan(repo, target_dir)

            
            ##format data
            repo_data = h1.formatData(data, repo["name"], out)
            
            #logger.info(repo_data)
            ## save the data
            db.setScanRepo(repo_data)

            ## delete the repo
            h1.cleaner(repo["name"], target_dir)