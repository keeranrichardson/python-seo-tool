class HTMLReporter:

    """Generates the HTML for an HTML report

    This class parses the scanner result and reports them in a user-friendly format.
    This class does not write the HTML report, it generates the HTML string.

    Typical usage example:

    report = HTMLReporter(self.scanner.getResults()).makeReport()

    Attributes:
        scannerResults: a ScannerResults objects
    """

    def __init__(self, scannerResults):
        self.scannerResult = scannerResults
        self.summaryCountLines = []
        self.tableOfContentsList = []

    def aTag(self, url, text):
        # Creates an html string for an <a> tag when given the url and text

        tag = "<a href = '" + url + "' target='_blank'>" + text + "</a>"

        return tag

    def makeReport(self):

        # top and bottom are parts of the HTML report that will be the same between every report

        top = """
                <html>
                    <head>
                        <title>HTML Report:</title>
                    </head>
                    <body>
                        <h1>
                            Scan Results:
                        </h1>
                        """
        bottom = """
                    </body>
                </html>"""

        # Creates the line of the HTML report that shows the date and time of
        # when the scan started from the scannerResult object passed into this class
        scannerStartDateLine = "<h2>Date and time of scan: {}</h2>\n".format(
            self.scannerResult.getStartDateTime()
        )

        # https://stackoverflow.com/questions/538666/format-timedelta-to-string

        # Calculates the amount of time the scan took
        timeDifference = (
            self.scannerResult.getEndDateTimeRaw()
            - self.scannerResult.getStartDateTimeRaw()
        )
        seconds = timeDifference.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        # https://docs.python.org/3/library/string.html#format-string-syntax
        duration = "{:02} hours, {:02} minutes, {:02} seconds".format(
            hours, minutes, seconds
        )
        # Line of report that will show the duration of the scan
        timeDifferenceLine = "<p>Duration of scan: {}</p>".format(duration)

        # Defining variable that will store the different sections of the report
        htmlSections = []

        # Storing the internal links found in the scan from
        # the scannerResult object into variable results
        results = self.scannerResult.getInternalLinkResults()

        # Calls the functions that adds the status codes
        # to the summary of the HTML report
        self.makeStatusCodeSection()

        # Adds number of internal URLs found to summary of HTML report
        self.addSummaryCountLine("Number of internal URLs found", len(results))

        # creates and adds section to htmlSections on internal URLs
        internalUrlsReportSection = self.createHTMLSection(
            "Internal URLs found:", results
        )
        htmlSections.append(internalUrlsReportSection)

        # Storing the external links found in the scan from the scannerResult
        # object into variable results
        results = self.scannerResult.getExternalLinkResults()

        # Adds number of external URLs found to summary of HTML report
        self.addSummaryCountLine("Number of external URLs found", len(results))

        # creates and adds section to htmlSections on external URLs
        externalUrlsReportSection = self.createHTMLSection(
            "External URLs found:", results
        )
        htmlSections.append(externalUrlsReportSection)

        # Storing the images found in the scan from the scannerResult object
        imageResults = self.scannerResult.getImageResults()

        # Adds number of images found to summary of HTML report
        self.addSummaryCountLine("Number of Images found", len(imageResults))

        # creates and adds section to htmlSections on images
        imagesReportSection = self.createHTMLSection("Images found:", imageResults)
        htmlSections.append(imagesReportSection)

        # Storing the head links found in the scan from the scannerResult
        # object and adds number of head links found to summary of HTML report
        headLinkResults = self.scannerResult.getHeadLinkResults()
        self.addSummaryCountLine("Number of Head Links found", len(headLinkResults))

        # creates and adds section to htmlSections on head links
        headLinksReportSection = self.createHTMLSection(
            "Head Links found:", headLinkResults
        )
        htmlSections.append(headLinksReportSection)

        # Storing the scripts found in the scan from the scannerResult
        # object and adds number of scripts found to summary of HTML report
        scriptResults = self.scannerResult.getScriptResults()
        self.addSummaryCountLine("Number of Scripts found", len(scriptResults))

        # creates and adds section to htmlSections on scripts
        scriptsReportSection = self.createHTMLSection("Scripts found:", scriptResults)
        htmlSections.append(scriptsReportSection)

        # Storing the iframes found in the scan from the scannerResult
        # object and adds number of iframes found to summary of HTML report
        iFrameResults = self.scannerResult.getIFrameResults()
        self.addSummaryCountLine("Number of IFrames found", len(iFrameResults))

        # creates and adds section to htmlSections on iframes
        iFrameReportSection = self.createHTMLSection("IFrames found:", iFrameResults)
        htmlSections.append(iFrameReportSection)

        # adds all of the html strings from the differecnt sections together
        html = (
            top
            + scannerStartDateLine
            + timeDifferenceLine
            + self.getSummaryCountSection()
            + self.getTableOfContents()
            + " ".join(htmlSections)
            + bottom
        )
        return html

    def makeStatusCodeSection(self):
        statusCodes = self.scannerResult.getAllStatusCodes()
        for statusCode in statusCodes:
            amount = len(self.scannerResult.getAllResultsOfStatusCode(statusCode))
            self.addSummaryCountLine(str(statusCode) + "s", amount)

    def getSummaryCountSection(self):
        summaryCountSection = (
            "<h2>Summary</h2><ul>" + "\n".join(self.summaryCountLines) + "</ul>"
        )
        return summaryCountSection

    def addSummaryCountLine(self, title, number):
        lineTemplate = "<li>{} = {}</li>"
        line = lineTemplate.format(title, number)

        self.summaryCountLines.append(line)

    def getTableOfContents(self):

        tableOfContents = (
            "<h2>Table of Contents</h2><ul>"
            + "\n".join(self.tableOfContentsList)
            + "</ul>"
        )
        return tableOfContents

    def addToTableOfContents(self, hashValue, displayText):

        lineTemplate = "<li><a href='#{}'>{}</a></li>"
        line = lineTemplate.format(hashValue, displayText)

        self.tableOfContentsList.append(line)

    def createHTMLSection(self, title, results):

        self.addToTableOfContents(title, title)

        middle = "<h2 id='" + title + "'>" + title + "</h2>"

        middle += "<ul>"

        lineTemplate = "<li>{} {} {} {}</li>"

        statusCodeLinks = {}

        for result in results:
            statusCode = result.getStatusCode()
            if str(statusCode) not in statusCodeLinks:
                statusCodeLinks[str(statusCode)] = ""

            statusCodeLink = self.aTag(
                "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{}".format(
                    result.getStatusCode()
                ),
                str(result.getStatusCode()),
            )
            resultUrlLink = self.aTag(result.getURL(), result.getURL())

            parentUrls = ""
            if len(result.getParentUrls()) > 0:
                parentUrls = "<ul><li>found on:<ul>"

                newLine = ""
                for urlTuple in result.getParentUrls():
                    parentUrls += (
                        newLine
                        + "<li>"
                        + self.aTag(urlTuple.url, str(urlTuple.url))
                        + " as: '"
                        + str(urlTuple.text)
                        + "'</li>"
                    )
                    newLine = "\n"
                parentUrls += "</ul></li></ul>"

            if result.getRedirectLocation() is not None:
                redirectsTo = (
                    "<ul><li>redirects to:<ul>"
                    + "<li>"
                    + self.aTag(
                        result.getRedirectLocation(), result.getRedirectLocation()
                    )
                    + "</li></ul></li></ul>"
                )
            else:
                redirectsTo = ""

            lineInMiddle = lineTemplate.format(
                statusCodeLink, resultUrlLink, parentUrls, redirectsTo
            )
            middle += lineInMiddle + "\n"
            statusCodeLinks[str(statusCode)] = (
                statusCodeLinks[str(statusCode)] + lineInMiddle + "\n"
            )

        middle += "</ul>"

        for statusCode, link in statusCodeLinks.items():
            middle += "\n<h3>" + statusCode + "s:</h3>\n"
            middle += "<ul>"
            middle += link
            middle += "</ul>"

        return middle
