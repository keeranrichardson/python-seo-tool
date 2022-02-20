class HTMLReporter:
    def __init__(self, scannerResults):
        self.scannerResult = scannerResults
        self.summaryCountLines = []
        self.tableOfContentsList = []

    def aTag(self, url, text):
        tag = "<a href = '"+url+"' target='_blank'>"+text+"</a>"

        return tag

    def makeReport(self):

        top = '''
                <html>
                    <head>
                        <title>HTML Report:</title>
                    </head>
                    <body>
                        <h1>
                            Scan Results:
                        </h1>
                        '''
        bottom = '''
                    </body>
                </html>'''

        scannerStartDateLine = "<h2>Date and time of scan: {}</h2>\n".format(self.scannerResult.getStartDateTime())

# https://stackoverflow.com/questions/538666/format-timedelta-to-string

        timeDifference = self.scannerResult.getEndDateTimeRaw() - self.scannerResult.getStartDateTimeRaw()
        seconds = timeDifference.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
# https://docs.python.org/3/library/string.html#format-string-syntax
        duration = '{:02} hours, {:02} minutes, {:02} seconds'.format(hours, minutes, seconds)
        timeDifferenceLine = "<p>Duration of scan: {}</p>".format(duration)

        htmlSections = []

        results = self.scannerResult.getInternalLinkResults()

        self.makeStatusCodeSection()

        self.addSummaryCountLine("Number of internal URLs found", len(results))

        internalUrlsReportSection = self.createHTMLSection("Internal URLs found:", results)
        htmlSections.append(internalUrlsReportSection)

        results = self.scannerResult.getExternalLinkResults()

        self.addSummaryCountLine("Number of external URLs found", len(results))

        externalUrlsReportSection = self.createHTMLSection("External URLs found:", results)
        htmlSections.append(externalUrlsReportSection)

        imageResults = self.scannerResult.getImageResults()

        self.addSummaryCountLine("Number of Images found", len(imageResults))

        imagesReportSection = self.createHTMLSection("Images found:", imageResults)
        htmlSections.append(imagesReportSection)

        headLinkResults = self.scannerResult.getHeadLinkResults()
        self.addSummaryCountLine("Number of Head Links found", len(headLinkResults))

        headLinksReportSection = self.createHTMLSection("Head Links found:", headLinkResults)
        htmlSections.append(headLinksReportSection)

        scriptResults = self.scannerResult.getScriptResults()
        self.addSummaryCountLine("Number of Scripts found", len(scriptResults))

        scriptsReportSection = self.createHTMLSection("Scripts found:", scriptResults)
        htmlSections.append(scriptsReportSection)

        iFrameResults = self.scannerResult.getIFrameResults()
        self.addSummaryCountLine("Number of IFrames found", len(iFrameResults))

        iFrameReportSection = self.createHTMLSection("IFrames found:", iFrameResults)
        htmlSections.append(iFrameReportSection)

        html = top + scannerStartDateLine + timeDifferenceLine + self.getSummaryCountSection()  + self.getTableOfContents() + " ".join(htmlSections) + bottom
        return html

    def makeStatusCodeSection(self):
        statusCodes = self.scannerResult.getAllStatusCodes()
        for statusCode in statusCodes:
            amount = len(self.scannerResult.getAllResultsOfStatusCode(statusCode))
            self.addSummaryCountLine(str(statusCode)+"s", amount)


    def getSummaryCountSection(self):
        summaryCountSection = "<h2>Summary</h2><ul>"+"\n".join(self.summaryCountLines)+"</ul>"
        return summaryCountSection

    def addSummaryCountLine(self, title, number):
        lineTemplate = "<li>{} = {}</li>"
        line = lineTemplate.format(title, number)

        self.summaryCountLines.append(line)

    def getTableOfContents(self):

        tableOfContents = "<h2>Table of Contents</h2><ul>"+"\n".join(self.tableOfContentsList)+"</ul>"
        return tableOfContents

    def addToTableOfContents(self, hashValue, displayText):

        lineTemplate = "<li><a href='#{}'>{}</a></li>"
        line = lineTemplate.format(hashValue, displayText)

        self.tableOfContentsList.append(line)


    def createHTMLSection(self, title, results):

        self.addToTableOfContents(title, title)

        middle = "<h2 id='"+title+"'>" + title + "</h2>"

        middle +="<ul>"

        lineTemplate = "<li>{} {} {} {}</li>"

        statusCodeLinks = {}

        for result in results:
            statusCode = result.getStatusCode()
            if str(statusCode) not in statusCodeLinks:
                statusCodeLinks[str(statusCode)] = ""


            statusCodeLink = self.aTag("https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{}".format(result.getStatusCode()),str(result.getStatusCode()))
            resultUrlLink = self.aTag(result.getURL(), result.getURL())

            parentUrls = ""
            if len(result.getParentUrls()) > 0:
                parentUrls = "<ul><li>found on:<ul>" 

                newLine = ""
                for urlTuple in result.getParentUrls():
                    parentUrls += newLine +"<li>"+ self.aTag(urlTuple.url, str(urlTuple.url)) + " as: '" + str(urlTuple.text) + "'</li>"
                    newLine = "\n"
                parentUrls += "</ul></li></ul>"

            if result.getRedirectLocation() is not None:
                redirectsTo = "<ul><li>redirects to:<ul>"+"<li>"+self.aTag(result.getRedirectLocation(), result.getRedirectLocation())+"</li></ul></li></ul>"
            else:
                redirectsTo = ""

            lineInMiddle = lineTemplate.format(statusCodeLink, resultUrlLink, parentUrls, redirectsTo)
            middle += lineInMiddle+"\n"
            statusCodeLinks[str(statusCode)] = statusCodeLinks[str(statusCode)] + lineInMiddle+"\n"

        middle +="</ul>"

        for statusCode, link in statusCodeLinks.items():
            middle += "\n<h3>"+statusCode+"s:</h3>\n"
            middle +="<ul>"
            middle += link
            middle +="</ul>"

        return middle
       