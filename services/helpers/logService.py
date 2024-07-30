from repositories.logRepo import LogRepo



class LogService :

    def insertLogs(logs) :
        LogRepo().insertLogs(logs)
        
    
    def getLogs(start_index, end_index) :
        return LogRepo().getLogs(start_index, end_index)
        #TODO
        #return no settings are updated on first call