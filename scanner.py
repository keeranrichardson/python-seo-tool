from requests.models import parse_url
from webPage import WebPage
from urlScanner import UrlScanner
from urlResult import UrlResult
from urllib.parse import urlparse
import datetime

class Scanner:
    def __init__(self, url, restrictToDomain):
        self.restrictToDomain = restrictToDomain
        self.startingUrl = url
        self.results = ScannerResults()
        self.urlsToScan = [self.startingUrl]
        self.urlsScanned = []
        self.urlsStatusChecked = []
    
    def scan(self):
        while len(self.urlsToScan) > 0:
            urlToScan = self.urlsToScan.pop()
            self.urlsScanned.append(urlToScan)  
            self.scanPage(urlToScan)
            

    def scanPage(self, url):
        webPage = WebPage(url)
        if webPage.isUrlScannable():
            self.results.addUrlScanned(url)
            for aLink in webPage.findLinks():
                if aLink in self.urlsStatusChecked:
                    print("status checked already")
                else:
                    link = UrlScanner(aLink)
                    if link.isScannable():
                        self.addUrlToScan(aLink)
                    print(link.getStatus(), aLink)
                    self.results.add(UrlResult(aLink, link.getStatus(), url))
                    self.urlsStatusChecked.append(aLink)

    def getResults(self):
        return self.results

    def addUrlToScan(self, url):
        parsedUrl = urlparse(url)
        if url not in self.urlsScanned:
            if self.restrictToDomain in parsedUrl.netloc:
                self.urlsToScan.append(url)

    def getUrlsToScan(self):
        return self.urlsToScan

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

   
