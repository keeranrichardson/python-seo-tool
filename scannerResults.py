import datetime

class ScannerResults:
    def __init__(self):
        self.results = [] # UrlResult Array
        self.startDateTime = datetime.datetime.now()
        self.endDateTime = self.startDateTime
        self.urlsScanned = [] # String Array

    def addResult(self, urlResult):
        self.results.append(urlResult)
        self.endDateTime = datetime.datetime.now()

    def getResults(self):
        return self.results

    def getLinkResults(self):
        linkResults = []
        for link in self.results:
            if link.isLink():
                linkResults.append(link)
        return linkResults

    def getImageResults(self):
        imageResults = []
        for result in self.results:
            if result.isImage():
                imageResults.append(result)
        return imageResults

    def getHeadLinkResults(self):
        headLinkResults = []
        for result in self.results:
            if result.isHeadLink():
                headLinkResults.append(result)
        return headLinkResults

    def getStartDateTime(self):
        return self.startDateTime.strftime("%d/%m/%Y %H:%M:%S")
    
    def getStartDateTimeRaw(self):
        return self.startDateTime

    def getEndDateTimeRaw(self):
        return self.endDateTime

    def addUrlScanned(self, url):
        self.urlsScanned.append(url)
        
    def getUrlsScanned(self):
        return self.urlsScanned