from requests.models import parse_url
from webPage import WebPage
from urlScanner import UrlScanner
from urlResult import UrlResult
from urllib.parse import urlparse
import datetime
from scannerResults import ScannerResults

class Scanner:
    def __init__(self, url, restrictToDomain):
        # config for handling urls with slash at end
        self.treatUrlsWithEndingSlashSameAsWithout = True 
        # the domain we are restricting the scan to
        self.restrictToDomain = restrictToDomain
        # the url we start the scan with
        self.startingUrl = url
        # the results from the scan
        self.results = ScannerResults()
        # creating the first object to add to the queue
        urlResultHomePage = UrlResult(self.sanitiseURL(self.startingUrl), 0)
        # the queues for tracking the url states in the scan
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

                self.addUrlToScanAndFoundQueues(aLink, "",webPageUrl)

                events.append("number of links to scan: 1 on " + webPageUrl)

            else:
                if self.isAllowedToBeCrawled(webPageUrl):
                    # do not add if already checked
                    links = webPage.findLinks()
                    events.append("found " + str(len(links)) + " links on " + webPageUrl)
                    linksToProcess = 0

                    for aLinkTuple in links:
                        if self.addUrlToScanAndFoundQueues(aLinkTuple.url, aLinkTuple.text, webPageUrl):
                            linksToProcess += 1
                        self.addParentToPage(aLinkTuple, webPageUrl)


                    events.append("number of links to scan: " + str(linksToProcess) + " on " + webPageUrl)

        self.urlsStatusChecked[webPageUrl] = urlResult
        events.append("status code: " + str(webPage.getStatusCode()) + " - " + webPageUrl)
        return events
    
    def addUrlToScanAndFoundQueues(self, url, linkText, webPageUrl):
        sanitisedALink = self.sanitiseURL(url)
        if self.shouldAddToScanQueue(sanitisedALink):
            result = UrlResult(sanitisedALink, 0)
            self.urlsToScan.append(result)
            self.urlsFound[sanitisedALink] = result
            return True

        return False

    def addParentToPage(self,aLinkTuple,parentPageUrl):
        # add parent link to urlresult object
        sanitisedALink = self.sanitiseURL(aLinkTuple.url)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aLinkTuple.text)

    def getUrlFromQueue(self, url):
        try:
            return self.urlsFound[self.sanitiseURL(url)]
        except:
            return None

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
   
