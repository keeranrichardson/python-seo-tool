from requests.models import parse_url
from webPage import WebPage
from urlScanner import UrlScanner
from urlResult import UrlResult
from urllib.parse import urlparse
import datetime
from scannerResults import ScannerResults

#make everything work with dictionaries

class Scanner:
    def __init__(self, url, restrictToDomain):
        self.treatUrlsWithEndingSlashSameAsWithout = True 
        self.restrictToDomain = restrictToDomain
        self.startingUrl = url
        self.results = ScannerResults()
        urlResultHomePage = UrlResult(self.sanitiseURL(self.startingUrl), 0, self.sanitiseURL(self.startingUrl))
        self.urlsToScan = [urlResultHomePage]
        self.urlsScanned = {}
        self.urlsStatusChecked = {}
        self.urlsFound = {self.sanitiseURL(self.startingUrl):urlResultHomePage}
        
    
    def scan(self):
        while self.isMoreToScan():
            events = self.scanNext()
            for event in events:
                print(event)
            
    def isMoreToScan(self):
        return len(self.urlsToScan) > 0

    
    def scanNext(self):
        urlToScan = self.getNextURLToScan()
        self.urlsScanned[self.sanitiseURL(urlToScan.getURL())] = urlToScan  
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
        webPageUrl = self.sanitiseURL(webPage.getURL())

        if webPage.isUrlScannable():
            self.results.addUrlScanned(webPageUrl)
            urlResult.setStatusCode(webPage.getStatusCode())
            self.results.addResult(urlResult)
        
            # todo: refactor to remove duplicate code
            if urlResult.statusCode in [301, 302, 307, 308]:
                # add loxation to urlresult
                urlResult.setRedirectLocation(webPage.getRedirectLocation())
                aLink = webPage.getRedirectLocation()
                events.append(webPageUrl + " redirects to: " + aLink)
                # follow like normal link
                sanitisedALink = self.sanitiseURL(aLink)
                if self.shouldAddToScanQueue(sanitisedALink):
                    result = UrlResult(sanitisedALink, 0, webPageUrl)
                    self.urlsToScan.append(result)
                    self.urlsFound[sanitisedALink] = result
                events.append("number of links to scan: 1 on " + webPageUrl)

            else:
                if self.isAllowedToBeCrawled(webPageUrl):
                    # do not add if already checked
                    links = webPage.findLinks()
                    events.append("found " + str(len(links)) + " links on " + webPageUrl)
                    linksToProcess = 0

                    for aLink in links:
                        sanitisedALink = self.sanitiseURL(aLink)
                        if self.shouldAddToScanQueue(sanitisedALink):
                            linksToProcess += 1
                            result = UrlResult(sanitisedALink, 0, webPageUrl)
                            self.urlsToScan.append(result)
                            self.urlsFound[sanitisedALink] = result
                        #else:
                            #add parent link to urlresult object

                    events.append("number of links to scan: " + str(linksToProcess) + " on " + webPageUrl)

        self.urlsStatusChecked[webPageUrl] = urlResult
        events.append("status code: " + str(webPage.getStatusCode()) + " - " + webPageUrl)
        return events

    def getResults(self):
        return self.results

    def shouldAddToScanQueue(self, url):
        if self.haveScannedAlready(url):
            return False
        if url in self.urlsStatusChecked:
            return False
        if url in self.urlsFound:
            return False
        return True

    def sanitiseURL(self, url):
        if self.treatUrlsWithEndingSlashSameAsWithout:
            if url.endswith('/'):
                url = url.removesuffix('/')
        return url

    def haveScannedAlready(self, url):
        url = self.sanitiseURL(url)
        if url not in self.urlsScanned:
            return False
        return True

    def isAllowedToBeCrawled(self, url):
        parsedUrl = urlparse(url)
        if self.restrictToDomain in parsedUrl.netloc:
                return True
        return False
   
