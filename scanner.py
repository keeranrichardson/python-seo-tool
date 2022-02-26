from urllib.parse import urlparse
import time
from webPage import WebPage
from urlResult import UrlResult
from scannerResults import ScannerResults


class Scanner:
    """Scan and crawl the websites

    This class does all the work for the scanning of the website.

    Typical usage example:

    scanner = Scanner(urlToParse, parseUrl.netloc)
    scanner.scan()

    Attributes:
        url: The url that is being scanned
        restrictToDomain: The domain that we do not want to scan outside of
    """

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

        # the queues for tracking the url states in the scan,
        # these all contain UrlResult objects
        self.urlsToScan = [urlResultHomePage]
        self.urlsScanned = {}
        self.urlsStatusChecked = {}
        self.urlsFound = {self.sanitiseURL(self.startingUrl): urlResultHomePage}

        # configuring scanner to crawl as well as check the status.
        # If false will only check status, which is useful for siteMap processing
        self.canCrawlUrls = True
        self.rateLimitSeconds = 0

        # events to log
        self.events = []

    def clearEvents(self):
        """
        Clear the events log
        """
        self.events = []

    def logEvent(self, eventToLog):
        """
        Add the given text eventToLog to the list of events
        to return to the GUI and write to the command line output
        """
        print(eventToLog)
        self.events.append(eventToLog)

    def scan(self):
        """
        keep scanning while there are
        more urls to scan, and rate limit
        the requests to avoid overloading the site
        """
        while self.isMoreToScan():
            self.scanNext()
            time.sleep(self.rateLimitSeconds)

    def isMoreToScan(self):
        return len(self.urlsToScan) > 0

    def setRateLimitMilliseconds(self, milliseconds):
        self.rateLimitSeconds = int(milliseconds) / 1000

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

    def scanPage(self, urlResult):
        """
        The main method that scans for links on a page and
        adds them to the queues for later processing.
        Only some links are scanned as web pages
        e.g. Images are checked to see if they exist
        but they are not scanned for more urls.
        """

        self.clearEvents()

        self.logEvent("About to check " + urlResult.getURL())

        # gets and sanitises the url to scan
        webPage = WebPage(urlResult.getURL())
        webPageUrl = self.sanitiseURL(webPage.getURL())

        # add the status code to the url result object
        # add the url to the results of the scan
        urlResult.setStatusCode(webPage.getStatusCode())
        self.results.addResult(urlResult)

        # if the url is scannable, add the url to the urls scanned
        if webPage.isUrlScannable():
            self.results.addUrlScanned(webPageUrl)

            if urlResult.statusCode in [301, 302, 307, 308]:

                # add location of redirect to urlresult
                urlResult.setRedirectLocation(webPage.getRedirectLocation())
                aLink = webPage.getRedirectLocation()
                self.logEvent(webPageUrl + " redirects to: " + aLink)

                # follow like normal link
                self.addUrlToScanAndFoundQueues(aLink)

                # report how many links to scan on page
                self.logEvent("number of links to scan: 1 on " + webPageUrl)

            else:
                # We only want to scan links because they are the urls of web pages
                # that have links, images, head links, scripts, iframes
                # and all the other html features that are processed in the scanner
                if urlResult.isLink() and self.isAllowedToBeCrawled(webPageUrl):

                    # each of the following method calls
                    # scans the page for a specific feature
                    # and adds the found url results
                    # to the scan queue
                    self.addResultsToCrawl(
                        webPage.findLinks(),
                        "links",
                        webPageUrl,
                        "url",
                        self.addParentToPage,
                    )
                    self.addResultsToCrawl(
                        webPage.findImages(),
                        "images",
                        webPageUrl,
                        "src",
                        self.addParentToPageImage,
                    )
                    self.addResultsToCrawl(
                        webPage.findHeadLinks(),
                        "head links",
                        webPageUrl,
                        "href",
                        self.addParentToPageHeadLink,
                    )
                    self.addResultsToCrawl(
                        webPage.findScripts(),
                        "scripts",
                        webPageUrl,
                        "src",
                        self.addParentToPageScript,
                    )
                    self.addResultsToCrawl(
                        webPage.findIFrames(),
                        "iframes",
                        webPageUrl,
                        "src",
                        self.addParentToPageIFrame,
                    )

        # track the web page as one that has already
        # had the status code checked
        self.urlsStatusChecked[webPageUrl] = urlResult

        self.logEvent(
            "status code "
            + urlResult.isA()
            + ": "
            + str(webPage.getStatusCode())
            + " - "
            + webPageUrl
            + " "
            + str(urlResult.isInternal())
        )
        return self.events

    def addUrlToScanAndFoundQueues(self, url):
        """
        Adds the url to the scan and found queues if its a url
        that should be added to the scan queue so it can be
        processed in the scan. The url is also marked whether
        it is internal or not as we only want to scan internal links.
        """
        sanitisedALink = self.sanitiseURL(url)
        if self.shouldAddToScanQueue(sanitisedALink):
            result = UrlResult(sanitisedALink, 0)
            self.urlsToScan.append(result)
            self.urlsFound[sanitisedALink] = result
            result.setIsInternal(self.isInternal(sanitisedALink))
            return True

        return False

    def addResultsToCrawl(
        self, foundResults, typeOfResult, webPageUrl, tupleVal, callback
    ):

        self.logEvent(
            "found " + str(len(foundResults)) + " " + typeOfResult + " on " + webPageUrl
        )
        resultsToProcess = 0

        # if the named tuple is added to scan and found queues successfully,
        # add 1 to the results to process
        for aTuple in foundResults:
            if self.addUrlToScanAndFoundQueues(aTuple._asdict()[tupleVal]):
                resultsToProcess += 1
            callback(aTuple, webPageUrl)

        self.logEvent(
            "number of "
            + typeOfResult
            + " to scan: "
            + str(resultsToProcess)
            + " on "
            + webPageUrl
        )

    def addParentToPage(self, aLinkTuple, parentPageUrl):
        """
        add parent link to urlresult object
        """
        sanitisedALink = self.sanitiseURL(aLinkTuple.url)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aLinkTuple.text)

    def addParentToPageImage(self, aImageTuple, parentPageUrl):
        """
        add parent link to urlresult object
        and set the url as an image
        """
        sanitisedALink = self.sanitiseURL(aImageTuple.src)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aImageTuple.alt)
        result.setUrlAsImage()

    def addParentToPageHeadLink(self, aHeadLinkTuple, parentPageUrl):
        """
        add parent link to urlresult object
        and set the url as a head link
        """
        sanitisedALink = self.sanitiseURL(aHeadLinkTuple.href)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, str(aHeadLinkTuple.rel))
        result.setUrlAsHeadLink()

    def addParentToPageScript(self, aScriptTuple, parentPageUrl):
        """
        add parent link to urlresult object
        and set the url as a script
        """
        sanitisedALink = self.sanitiseURL(aScriptTuple.src)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, "")
        result.setUrlAsScript()

    def addParentToPageIFrame(self, aIFrameTuple, parentPageUrl):
        """
        add parent link to urlresult object
        and set the url as an iframe
        """
        sanitisedALink = self.sanitiseURL(aIFrameTuple.src)
        result = self.getUrlFromQueue(sanitisedALink)
        result.addParentUrl(parentPageUrl, aIFrameTuple.title)
        result.setUrlAsIFrame()

    def getUrlFromQueue(self, url):
        """
        Tries to get the urlResult from the url found queue,
        if it can't find it then it traps any errors and returns None
        """
        try:
            return self.urlsFound[self.sanitiseURL(url)]
        except Exception as e:
            print("Exception when trying to find in URL queue " + url)
            print(e)
            return None

    def getResults(self):
        """
        return the ScannerResults
        with all statuses for urls scanned
        """
        return self.results

    def shouldAddToScanQueue(self, url):
        """
        A set of conditions that check
        for whether a url should be added
        to the scan queue
        """
        if self.haveScannedAlready(url):
            return False
        if url in self.urlsStatusChecked:
            return False
        if url in self.urlsFound:
            return False
        return True

    def sanitiseURL(self, url):
        """
        removes ending slash off a url if it has
        one and treatUrlsWithEndingSlashSameAsWithout is True
        """
        if self.treatUrlsWithEndingSlashSameAsWithout:
            if url.endswith("/"):
                url = url.removesuffix("/")
        return url

    def haveScannedAlready(self, url):
        """
        checks if url has already been
        scanned by checking whether the url
        is in self.urlsScanned or not
        """
        url = self.sanitiseURL(url)
        if url not in self.urlsScanned:
            return False
        return True

    def isInternal(self, url):
        """
        Checks the urls netloc against the netloc
        of the original url to see if the url
        is internal or not
        """
        parsedUrl = urlparse(url)
        if self.restrictToDomain in parsedUrl.netloc:
            return True
        return False

    def isAllowedToBeCrawled(self, url):
        """
        url is allowed to be crawled if
        canCrawlUrls is set to False
        and the url is internal
        """
        if self.canCrawlUrls is False:
            return False

        return self.isInternal(url)
