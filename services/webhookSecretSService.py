from models.githubPR import GithubPR
from models.webhookConfig import WebhookConfig
from services.webhookConfigService import WebhookConfigService
from services.helperWhitelistService import HelperWhitelistSecretService
from repositories.webhookSecretSRepo import WebhookSecretSRepo
from services.helpers.githubService import GithubService

import subprocess
import json
import yaml
from datetime import datetime

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebhookSecretSService :

    def __init__(self) :
        #will initialise all the global variables over here
        webhookConfig = WebhookConfigService.getConfig()
        self.git = webhookConfig.git
        self.scanType = webhookConfig.scanType
        self.PRcomment = webhookConfig.PRcomment
        self.blockPR = webhookConfig.blockPR
        self.gitActions =webhookConfig.gitActions
        self.targetRepos = webhookConfig.targetRepos 


    def looseScan(self, g1) :
        #only PR filesds
        if self.git == "github" :

            #getFilePaths by git helper
            filenamePath = g1.findLooseScanFilePath()
            print(filenamePath)
            #clone the repo
            g1.cloneRepo()
        print("hey-in")

        commitSecretsList = []
        # loop over it and scan each file and store result in a file
        for file in filenamePath : 
            #scan file
            print(g1.target_dir+g1.repository+"/"+file)
            response = subprocess.Popen(["sudo trufflehog filesystem "+g1.target_dir+"/"+g1.repository+"/"+file+" --json"], shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = response.communicate()
            print(out, err)
            print("HELO")
            if out != b'' :
                print("HELO1")
                out = out.decode("utf-8")
                out = out.split('\n')
                for sec in out :
                    print("HELO2")
                    if sec :
                        print("HELO3")
                        sec = json.loads(sec)
                        #whitelist secret
                        if sec["Raw"] in g1.secMap :
                            continue
                        print("HELO4")
                        if "line" not in sec["SourceMetadata"]["Data"]["Filesystem"] :
                            line = 0
                        else : 
                            line = sec["SourceMetadata"]["Data"]["Filesystem"]["line"]
                        sec["secUrl"] = filenamePath[file] + "#L"+ str(line)
                        # apend the date to master json list
                        sec["RepoName"] = g1.repository
                        commitSecretsList.append(sec)
                        print("out :",sec)

        print(commitSecretsList)
        subprocess.call(["rm", "-rf", g1.repository], cwd=g1.target_dir)
        print("AFTER :", commitSecretsList)
        return commitSecretsList

    '''
    def formatFile(self, file_path, repoName ) :
        secMap = HelperWhitelistSecretService().filterSecretPRScan(repoName)
        yaml_list = []
        with open("TH_new.txt","r") as f :
            for case in f.readlines() :
                if case.strip() == "" :
                    continue
                singleSec = json.loads(case)
                if singleSec["Raw"] in secMap :
                    continue
                #yaml_data = yaml.dump(singleSec, default_flow_style=False)
                yaml_list.append(singleSec)
                print("----------------------------------------------------------------------")

        with open(file_path, 'w') as file:
            yaml.dump(yaml_list, file, default_flow_style=False, sort_keys=False)
    '''

    def aggressiveScan(self, g1) :
        if self.git == "github" :
            print("ehy")
            # get list of commits
            commitsList = g1.fetchPRCommits()

            #create final json file
            masterSecretList = []
            
            # for loop on list of commits
            for commit_sha in commitsList :
                full_filename = g1.target_dir+"/"+g1.repository+"/"+commit_sha
                commitSecretsList = g1.create_commit_diff_file(commit_sha, full_filename)
                print("commitSecretsList : " , commitSecretsList)
                masterSecretList = masterSecretList + commitSecretsList
            
            return masterSecretList

    def startScan(self, pr) :

        gitObject = None
        if self.git == "github" :
            logger.info("hey")
            print("hey")
            pr = GithubPR(**pr)
            if pr.action not in self.gitActions :
                print("PR action : ", pr.action)
                return
            print("hey-120")
            #fetch the PR no
            gitObject = GithubService(pr)
            logger.info("hey-done")


        if self.git == "bitbucket" :
            #pr = BitbucketPR(**pr
            print("hey")
        if self.scanType == "Loose" :
            masterSecretList = self.looseScan(gitObject)
        else :
            masterSecretList = self.aggressiveScan(gitObject)
        print("hey-out")

        #calculate scan result
        if len(masterSecretList) > 0 :
            scan_result = False
        else : 
            scan_result = True

        #result file
        date_of_scan = str(datetime.now())
        fileName = "pr_scan/"+date_of_scan+"_"+gitObject.repository+"_"+str(gitObject.prNo)+".yaml"

        #create result file
        with open(fileName, 'w') as file:
            yaml.dump(masterSecretList, file, default_flow_style=False)
        

        saveData = { "prLink": gitObject.prHtmlUrl,
                    "repoName": gitObject.repository,
                    "scan_result": scan_result,
                    "secret_no": len(masterSecretList),
                    "secrets_link": fileName,
                    "date_of_scan": date_of_scan
                    }

        ## save the scan with PR in a file and save data n db[ prlink, reponame, pr_success, secrets_no, secrets_link, date_of_scan]
        WebhookSecretSRepo().insertData(saveData)
        # return the json scan data

        #comment and scan
        if scan_result == False :
            gitObject.commentPR(self.PRcomment, masterSecretList)
        if self.blockPR == True :
            gitObject.updateStatus(scan_result)
        

    def getScanData(self) :
        return WebhookSecretSRepo().getData()


    def getSecretFile(self, date_of_scan) :
        return WebhookSecretSRepo().fetchSecretFile(date_of_scan)

