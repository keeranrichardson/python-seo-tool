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
        """
        Return an array of
        all the urlResult objects
        """
        return self.results

    def getAllStatusCodes(self):
        """
        Return an array of
        all the status codes
        on urlResult objects
        """
        statusCodes = []
        for result in self.results:
            statusCodes.append(result.getStatusCode())

        return set(statusCodes)

    def getAllResultsOfStatusCode(self, statusCode):
        """
        Return an array of
        all the urlResult objects
        that have a particular
        status code
        """
        results = []
        for result in self.results:
            if result.getStatusCode() == statusCode:
                results.append(result)

        return results

    def getInternalLinkResults(self):
        """
        Return an array of
        all the urlResult objects
        that have internal links
        """
        results = []
        for result in self.getLinkResults():
            if result.isInternal():
                results.append(result)
        return results

    def getExternalLinkResults(self):
        """
        Return an array of
        all the urlResult objects
        that have external links
        """
        results = []
        for result in self.getLinkResults():
            if not result.isInternal():
                results.append(result)
        return results

    def getResultsWhere(self, typeOf):
        """
        Return an array of
        all the urlResult objects
        of a particular type
        """
        results = []
        for result in self.results:
            if result.isA() == typeOf:
                results.append(result)
        return results

    def getLinkResults(self):
        """
        Return an array of all results of type link
        """
        return self.getResultsWhere("link")

    def getImageResults(self):
        """
        Return an array of all results of type image
        """
        return self.getResultsWhere("image")

    def getHeadLinkResults(self):
        """
        Return an array of all results of type headlink
        """
        return self.getResultsWhere("headlink")

    def getScriptResults(self):
        """
        Return an array of all results of type script
        """
        return self.getResultsWhere("script")

    def getIFrameResults(self):
        """
        Return an array of all results of type iframe
        """
        return self.getResultsWhere("iframe")

    def getStartDateTime(self):
        """
        Return the start date and time of the scan in the format
        day/month/year hour:minute:second
        """
        return self.startDateTime.strftime("%d/%m/%Y %H:%M:%S")

    def getStartDateTimeRaw(self):
        """
        Return the start date and time
        without any formatting
        """
        return self.startDateTime

    def getEndDateTimeRaw(self):
        """
        Return the end date and time
        without any formatting
        """
        return self.endDateTime

    def addUrlScanned(self, url):
        """
        add url to the list of scanned urls
        """
        self.urlsScanned.append(url)

    def getUrlsScanned(self):
        """
        get all urls scanned
        """
        return self.urlsScanned
