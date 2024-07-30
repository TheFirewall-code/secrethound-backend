

from repositories.whitelistSecretRepo import WhitelistSecretRepo 
from models.whitelistSecret import WhitelistSecret
from models.repo import Repo
from models.org import Org



class HelperWhitelistSecretService :

    def feedRealSecret(self, orgData : Org) :

        whitelistSecret = self.getWhitelistSecret()

        #collect repolevel whitelist into a list  -> ease for searching
        orgLevelSecret = []
        for secret in whitelistSecret["orgscope"] :
            orgLevelSecret.append(secret["Secret"])

        orgData = orgData.dict()
        #new Org data
        newOrgData =  {"name": orgData["name"], "scanedRepos": orgData["scannedRepos"], "repositories": []}

        for repo in orgData["repositories"] :
            #collect repolevel whitelist into a list  -> ease for searching
            repoLevelSecret = []
            for secret in whitelistSecret["reposcope"] :
                if secret["Repository"] == repo["repository"] :
                    repoLevelSecret.append(secret["Secret"])

            #new repo list
            newRepository = {"repository": repo["repository"], "totalNoCommits":  repo["totalNoCommits"],"secrets": [] }
            for secret in repo["secrets"] :
                if secret["Secret"] in orgLevelSecret  or secret["Secret"] in repoLevelSecret :
                    continue
                else :
                    newRepository["secrets"].append(secret)

            newOrgData["repositories"].append(newRepository)

        return Org(**newOrgData)

    def filterSecretPRScan(self, repoName) :
        whitelistSecret = self.getWhitelistSecret()
    
        #collect repolevel whitelist into a list  -> ease for searching
        orgLevelSecret = []
        for secret in whitelistSecret["orgscope"] :
            orgLevelSecret.append(secret.Secret)


        #collect repolevel whitelist into a list  -> ease for searching
        repoLevelSecret = []
        for secret in whitelistSecret["reposcope"] :
            if secret.Repository == repoName :
                repoLevelSecret.append(secret.Secret)

        return orgLevelSecret + repoLevelSecret
        

    def setWhitelistSecret(self, whitelistSecret : WhitelistSecret) :

        w1 = WhitelistSecretRepo()
        return w1.inserttWhitelist(whitelistSecret)


    def getWhitelistSecret(self) :

        w1 = WhitelistSecretRepo()

        #fetch Org level
        orgLevel = w1.fetchOrgWhitelist()

        #fetch Repo level
        repoLevel = w1.fetchRepoWhitelist()

        return {"orgscope": orgLevel, "reposcope" : repoLevel}


    def removeWhitelistSecret(self,secret) :

        w1 = WhitelistSecretRepo()

        return w1.deleteWhitelist(secret)







