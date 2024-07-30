from models.config import Config
from repositories.configRepo import ConfigRepo
from services.helperService import HelperService


class ConfigService :

    def insertConfig(config: Config) :
        
        c1 = ConfigRepo()
        #clear the document from the collection
        c1.deleteConfig()   

        config.totalRepos = HelperService().getTotalRepoCount(config.url, config.access_token)
        c1.insertConfig(config)

        return {"message": "settings updated !"}
    
    def getConfig() :
        return ConfigRepo().getConfig()
        #TODO
        #return no settings are updated on first call