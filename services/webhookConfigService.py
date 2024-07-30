from models.webhookConfig import WebhookConfig
from repositories.webhookConfigRepo import WebhookConfigRepo
from services.helperService import HelperService


class WebhookConfigService :

    def insertConfig(webhookConfig: WebhookConfig) :
        
        c1 = WebhookConfigRepo()
        #clear the document from the collection
        c1.deleteConfig()   

        c1.insertConfig(webhookConfig)

        return {"message": "Webhook configs updated !"}
    
    def getConfig() :
        return WebhookConfigRepo().getConfig()
        #TODO
        #return no settings are updated on first call