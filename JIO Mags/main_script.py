import eel
import fetchMagData
import magazineByID
import fetchIssueData
eel.init('web')

@eel.expose
def getPageData(pagenumber,datatype):
     return fetchMagData.getPageData(pagenumber,datatype)

@eel.expose    
def downloadPDF(magid, issueid):
     return magazineByID.downloadPDF(magid,issueid)

@eel.expose
def getImagebyID(magid,issueid):
    return fetchIssueData.getPageData(magid)

@eel.expose
def updateDatabase():
     import updateByCategory
     import updateBySection
     return "Success"

@eel.expose
def updateIssueDataBase(magid):
     import updateByID
     updateByID.startDownload(magid,1)
     return "Success"

eel.start('viewmagazine.htm')

