from webPage import WebPage
from urlScanner import UrlScanner
from urlResult import UrlResult
import datetime

class Scanner:
    def __init__(self, url):
        self.url = url
        self.page = WebPage(self.url)
        self.results = ScannerResults()

    def scan(self):
        if self.page.isUrlScannable():
            self.results.addUrlScanned(self.url)
            for aLink in self.page.findLinks():
                link = UrlScanner(aLink)
                print(link.getStatus(), aLink)
                self.results.add(UrlResult(aLink, link.getStatus(), self.url))

    def getResults(self):
        return self.results

class ScannerResults:
    def __init__(self):
        self.results = []
        self.startDateTime = datetime.datetime.now()
        self.endDateTime = self.startDateTime
        self.urlsScanned = []

    def add(self, urlResult):
        self.results.append(urlResult)
        self.endDateTime = datetime.datetime.now()

    def getResults(self):
        return self.results

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
