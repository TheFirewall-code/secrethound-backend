

from repositories.whitelistSecretRepo import WhitelistSecretRepo 
from models.whitelistSecret import WhitelistSecret


class WhitelistSecretService :

    def setWhitelistSecret(whitelistSecret : WhitelistSecret) :

        w1 = WhitelistSecretRepo()
        return w1.inserttWhitelist(whitelistSecret)


    def getWhitelistSecret() :

        w1 = WhitelistSecretRepo()

        #fetch Org level
        orgLevel = w1.fetchOrgWhitelist()

        #fetch Repo level
        repoLevel = w1.fetchRepoWhitelist()

        return {"orgscope": orgLevel, "reposcope" : repoLevel}


    def removeWhitelistSecret(secret) :

        w1 = WhitelistSecretRepo()

        return w1.deleteWhitelist(secret)







