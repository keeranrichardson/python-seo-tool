from urllib.parse import urlparse
import time
from webPage import WebPage
from urlResult import UrlResult
from scannerResults import ScannerResults

class Scanner:
    def __init__(self, url, restrictToDomain):
        # config for handling urls with slash at end
        self.treatUrlsWithEndingSlashSameAsWithout = False
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
        # configuring scanner to crawl as well as check the status. If false will only check status
        self.canCrawlUrls = True
        self.rateLimitSeconds = 0
        # events to log
        self.events=[]

    def clearEvents(self):
        self.events = []

    def logEvent(self, eventToLog):
        print(eventToLog)
        self.events.append(eventToLog)

    def scan(self):
        while self.isMoreToScan():
            self.scanNext()
            time.sleep(self.rateLimitSeconds)

    def isMoreToScan(self):
        return len(self.urlsToScan) > 0

    def setRateLimitMilliseconds(self, milliseconds):
        self.rateLimitSeconds = int(milliseconds)/1000

    def setCanCrawlUrls(self, canCrawl):
        self.canCrawlUrls = canCrawl

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
        self.clearEvents()

        self.logEvent("About to check "+ urlResult.getURL())

        webPage = WebPage(urlResult.getURL())
        webPageUrl = self.sanitiseURL(webPage.getURL())

        urlResult.setStatusCode(webPage.getStatusCode())
        self.results.addResult(urlResult)

        if webPage.isUrlScannable():
            self.results.addUrlScanned(webPageUrl)

            if urlResult.statusCode in [301, 302, 307, 308]:

                # add location to urlresult
                urlResult.setRedirectLocation(webPage.getRedirectLocation())
                aLink = webPage.getRedirectLocation()
                self.logEvent(webPageUrl + " redirects to: " + aLink)

                # follow like normal link
                self.addUrlToScanAndFoundQueues(aLink)

                self.logEvent("number of links to scan: 1 on " + webPageUrl)

            else:
                if self.isAllowedToBeCrawled(webPageUrl):
                    # links
                    # do not add if already checked

                    self.addResultsToCrawl(webPage.findLinks(), "links", webPageUrl,'url', self.addParentToPage)

                    # images

                    self.addResultsToCrawl(webPage.findImages(), "images", webPageUrl,'src', self.addParentToPageImage)

                    # headlinks

                    self.addResultsToCrawl(webPage.findHeadLinks(), "head links", webPageUrl,'href', self.addParentToPageHeadLink)

                    # scripts

                    self.addResultsToCrawl(webPage.findScripts(), "scripts", webPageUrl,'src', self.addParentToPageScript)

                    # iframes

                    self.addResultsToCrawl(webPage.findIFrames(), "iframes", webPageUrl,'src', self.addParentToPageIFrame)


        self.urlsStatusChecked[webPageUrl] = urlResult

        self.logEvent("status code " + urlResult.isA() + ": " + str(webPage.getStatusCode()) + " - " + webPageUrl + " " + str(urlResult.isInternal()))
        return self.events

    def addUrlToScanAndFoundQueues(self, url):
        sanitisedALink = self.sanitiseURL(url)
        if self.shouldAddToScanQueue(sanitisedALink):
            result = UrlResult(sanitisedALink, 0)
            self.urlsToScan.append(result)
            self.urlsFound[sanitisedALink] = result
            result.setIsInternal(self.isInternal(sanitisedALink))
            return True

        return False

    def addResultsToCrawl(self, foundResults, typeOfResult, webPageUrl,tupleVal, callback):

        self.logEvent("found " + str(len(foundResults)) + " " + typeOfResult + " on " + webPageUrl)
        resultsToProcess = 0

        for aTuple in foundResults:
            if self.addUrlToScanAndFoundQueues(aTuple._asdict()[tupleVal]):
                resultsToProcess += 1
            callback(aTuple, webPageUrl)

        self.logEvent("number of " + typeOfResult + " to scan: " + str(resultsToProcess) + " on " + webPageUrl)

    def addParentToPage(self,aLinkTuple,parentPageUrl):
        # add parent link to urlresult object
        sanitisedALink = self.sanitiseURL(aLinkTuple.url)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aLinkTuple.text)

    def addParentToPageImage(self,aImageTuple,parentPageUrl):
        # add parent link to urlresult object
        sanitisedALink = self.sanitiseURL(aImageTuple.src)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aImageTuple.alt)
        result.setUrlAsImage()

    def addParentToPageHeadLink(self, aHeadLinkTuple, parentPageUrl):
        sanitisedALink = self.sanitiseURL(aHeadLinkTuple.href)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, str(aHeadLinkTuple.rel))
        result.setUrlAsHeadLink()

    def addParentToPageScript(self, aScriptTuple, parentPageUrl):
        sanitisedALink = self.sanitiseURL(aScriptTuple.src)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, '')
        result.setUrlAsScript()

    def addParentToPageIFrame(self, aIFrameTuple, parentPageUrl):
        sanitisedALink = self.sanitiseURL(aIFrameTuple.src)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aIFrameTuple.title)
        result.setUrlAsIFrame()

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

    def isInternal(self,url):
        parsedUrl = urlparse(url)
        if self.restrictToDomain in parsedUrl.netloc:
            return True
        return False

    def isAllowedToBeCrawled(self, url):

        if self.canCrawlUrls is False:
            return False

        return self.isInternal(url)
