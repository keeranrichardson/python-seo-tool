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
        #self.urlsToScan = [self.startingUrl]
        self.urlsToScan = [UrlResult(self.startingUrl, 0, self.startingUrl)]
        self.urlsScanned = []
        self.urlsStatusChecked = []
        #self.urlsToCrawl = []
        #self.urlsCrawled = []
        #config
        self.treatUrlsWithEndingSlashSameAsWithout = True 
    
    def scan(self):
        while self.isMoreToScan():
            self.scanNext()
            
    def isMoreToScan(self):
        return len(self.urlsToScan) > 0

    
    def scanNext(self):
        urlToScan = self.getNextURLToScan()
        self.urlsScanned.append(urlToScan)  
        return self.scanPage(urlToScan)

    def getNextURLToScan(self):
        if self.isMoreToScan():
            return self.urlsToScan.pop()
        return None

    def getNextURLToCrawl(self):
        ''

    def crawlURL(self, url):
        webPage = WebPage(url)
        links = webPage.findLinks()
        return links 

    # processing URL
    # check status code for URL to see if 2XX
    # check url to see if it should be scanned
    # get all links on page of URL
    # each link becomes processing URL
    def scanPage(self, urlResult):
        events=[]
        webPage = WebPage(urlResult.getURL())
        if webPage.isUrlScannable():
            self.results.addUrlScanned(urlResult.getURL())
            urlResult.setStatusCode(webPage.statusCode)
            self.results.addResult(urlResult)

            if self.isAllowedToBeCrawled(urlResult.getURL()):
                # do not add if already checked
                for aLink in webPage.findLinks():
                    if not self.haveScannedAlready(aLink) and not aLink in self.urlsStatusChecked:
                        self.urlsToScan.append(UrlResult(aLink, 0, urlResult.getURL()))

 #           for aLink in webPage.findLinks():
 #               if aLink in self.urlsStatusChecked:
 #                   print("status checked already", aLink)
 #                   events.append("status checked already - "+str(aLink))
 #               else:
 #                   link = UrlScanner(aLink)
 #                   if link.isScannable():
 #                       self.addUrlToScan(aLink)
 #                   print(link.getStatus(), aLink)
 #                   events.append("status code: " + str(link.getStatus()) + " - " + str(aLink))
 #                   if not self.haveScannedAlready(aLink):
 #                       self.results.addResult(UrlResult(aLink, link.getStatus(), url))
 #                       self.urlsStatusChecked.append(aLink)

        self.urlsStatusChecked.append(urlResult.getURL())
        events.append("status code: " + str(webPage.statusCode) + " - " + urlResult.getURL())
        return events

    def oldScanPage(self, url):
        events=[]
        webPage = WebPage(url)
        if webPage.isUrlScannable():
            self.results.addUrlScanned(url)
            for aLink in webPage.findLinks():
                if aLink in self.urlsStatusChecked:
                    print("status checked already", aLink)
                    events.append("status checked already - "+str(aLink))
                else:
                    link = UrlScanner(aLink)
                    if link.isScannable():
                        self.addUrlToScan(aLink)
                    print(link.getStatus(), aLink)
                    events.append("status code: " + str(link.getStatus()) + " - " + str(aLink))
                    if not self.haveScannedAlready(aLink):
                        self.results.addResult(UrlResult(aLink, link.getStatus(), url))
                        self.urlsStatusChecked.append(aLink)
        else:
            events.append("status code: " + str(webPage.statusCode) + " - " +url)
        return events

    def getResults(self):
        return self.results

    def addUrlToScan(self, url):
        if not self.haveScannedAlready(url) and self.isAllowedToBeScanned(url):
            self.urlsToScan.append(url)

    def getUrlsToScan(self):
        return self.urlsToScan

    def haveScannedAlready(self, url):
        if self.treatUrlsWithEndingSlashSameAsWithout:
            if url.endswith('/'):
                url = url.removesuffix('/')
        if url not in self.urlsScanned:
            return False
        return True

    def isAllowedToBeCrawled(self, url):
        parsedUrl = urlparse(url)
        if self.restrictToDomain in parsedUrl.netloc:
                return True
        return False


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

   
