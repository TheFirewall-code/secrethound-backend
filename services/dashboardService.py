from repositories.dashboardRepo import DashboardRepo

class DashboardService :

    def getLatestDataDb(d1) :
        #sort the collection
        d1 = DashboardRepo()
        # fetch latest collection and calculate the data
        latestCollection = d1.getOrgCollections()
        scanOrgData = d1.fetchScanOrgData(latestCollection)

        #convert to dash data format
        scanOrgData = DashboardService.convertToDash(latestCollection, scanOrgData)
        #print(len(scanOrgData["data"]))
        #get DashboardData
        dashData = d1.getLastDash()
        #print(len(dashData["data"]))
        #print(DashboardService.compareData(scanOrgData, dashData))
        #check if the collection is present in dashboard data
        if dashData == None or DashboardService.compareData(scanOrgData, dashData) == False :
            d1.storeDash(scanOrgData)
        ## if not store the collection name(date time) , secrets per repo.
        ## if yes, then match the calculated data with latest dashboard data
        ### if unmatch, store new dashboard data
        # {
        #   "collection_name" : "date_time",
        #   "data" : {"reponame": int(no of secrets)} 
        #}
        # return the data based on pagination

    def convertToDash(latestCollection, scanOrgData) :
        convertDash = {"collection_name": str(latestCollection.name), "data":{}}

        scanOrgData = scanOrgData.dict()
        for repos in scanOrgData["repositories"] :
            convertDash["data"][repos["repository"]] = len(repos["secrets"])

        return convertDash

    def compareData(scanOrgData, dashData) :
        #check for collection name 
        if scanOrgData["collection_name"] != dashData["collection_name"] :
            return False

        # if yes, then match the calculated data with latest dashboard data

        for repoName in scanOrgData["data"] :
            #print(repoName)
            if repoName not in dashData["data"] :
                return False
            if dashData["data"][repoName] != scanOrgData["data"][repoName] :
                return False

            
        return True

    def getDash(start_index, end_index) :
        d1 = DashboardRepo()
        DashboardService.getLatestDataDb(d1)

        return d1.getDashData(start_index, end_index)
        

        
