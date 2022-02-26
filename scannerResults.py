import datetime


class ScannerResults:
    """stores the results of the scan

    This class stores the results of the scan
    and allows you to get filtered results.

    eg:

    - get all external links
    - get all internal links
    - get all links with a particular status code

    Typical usage example:

    results = ScannerResults()
    results.addResult(urlResult)
    """

    def __init__(self):
        self.results = []  # UrlResult Array
        self.startDateTime = datetime.datetime.now()
        self.endDateTime = self.startDateTime
        self.urlsScanned = []  # String Array

    def addResult(self, urlResult):
        self.results.append(urlResult)
        self.endDateTime = datetime.datetime.now()

    def getResults(self):
        return self.results

    def getAllStatusCodes(self):

        statusCodes = []
        for result in self.results:
            statusCodes.append(result.getStatusCode())

        return set(statusCodes)

    def getAllResultsOfStatusCode(self, statusCode):

        results = []
        for result in self.results:
            if result.getStatusCode() == statusCode:
                results.append(result)

        return results

    def getInternalLinkResults(self):
        results = []
        for result in self.getLinkResults():
            if result.isInternal():
                results.append(result)
        return results

    def getExternalLinkResults(self):
        results = []
        for result in self.getLinkResults():
            if not result.isInternal():
                results.append(result)
        return results

    def getResultsWhere(self, typeOf):
        results = []
        for result in self.results:
            if result.isA() == typeOf:
                results.append(result)
        return results

    def getLinkResults(self):
        return self.getResultsWhere("link")

    def getImageResults(self):
        return self.getResultsWhere("image")

    def getHeadLinkResults(self):
        return self.getResultsWhere("headlink")

    def getScriptResults(self):
        return self.getResultsWhere("script")

    def getIFrameResults(self):
        return self.getResultsWhere("iframe")

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
