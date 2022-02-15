import datetime

class HTMLReporter:
    def __init__(self, scannerResults):
        self.scannerResult = scannerResults
    
    def aTag(self, url, text):
        tag = "<a href = '"+url+"' target='_blank'>"+text+"</a>"

        return tag
        
    def makeReport(self):
        results = self.scannerResult.getLinkResults()
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

        numberOfUrlsFoundLine = "<p>Number of URLs found = {}</p>".format(len(results))

        urlsReportSection = self.createHTMLSection("URLs found:", results)

        imageResults = self.scannerResult.getImageResults()
        numberOfImagesFoundLine = "<p>Number of Images found = {}</p>".format(len(imageResults))

        imagesReportSection = self.createHTMLSection("Images found:", imageResults)

        html = top + scannerStartDateLine + timeDifferenceLine + numberOfUrlsFoundLine  + numberOfImagesFoundLine + urlsReportSection + imagesReportSection +  bottom
        return html
    
    def createHTMLSection(self, title, results):

        middle = "<h2>" + title + "</h2>"

        middle +="<ul>"
    
        lineTemplate = "<li>{} {} [{}] {}</li>"

        statusCodeLinks = {}

        for result in results:
            statusCode = result.getStatusCode()
            if str(statusCode) not in statusCodeLinks:
                statusCodeLinks[str(statusCode)] = ""

            
            statusCodeLink = self.aTag("https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{}".format(result.getStatusCode()),str(result.getStatusCode()))
            resultUrlLink = self.aTag(result.getURL(), result.getURL())

            parentUrls = "found on: "
            commaString = ""
            for urlTuple in result.getParentUrls():
                parentUrls += commaString + self.aTag(urlTuple.url, str(urlTuple.url)) + " as: '"+urlTuple.text+"'"
                commaString = ", "   

            if result.getRedirectLocation() != None:
                redirectsTo = "Redirects to: "+self.aTag(result.getRedirectLocation(), result.getRedirectLocation())
            else:
                redirectsTo = ""

            lineInMiddle = lineTemplate.format(statusCodeLink, resultUrlLink, parentUrls, redirectsTo)
            middle += lineInMiddle+"\n"
            statusCodeLinks[str(statusCode)] = statusCodeLinks[str(statusCode)] + lineInMiddle+"\n"
        
        middle +="</ul>"

        for statusCode in statusCodeLinks:
            middle += "\n<h3>"+statusCode+"s:</h3>\n"
            middle +="<ul>"
            middle += statusCodeLinks[statusCode]
            middle +="</ul>"

        return middle
        
       