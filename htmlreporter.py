import datetime

class HTMLReporter:
    def __init__(self, scannerResults):
        self.scannerResult = scannerResults
    
    def aTag(self, url, text):
        tag = "<a href = '"+url+"' target='_blank'>"+text+"</a>"

        return tag
        
    def makeReport(self):
        results = self.scannerResult.getResults()
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

#https://stackoverflow.com/questions/538666/format-timedelta-to-string

        timeDifference = self.scannerResult.getEndDateTimeRaw() - self.scannerResult.getStartDateTimeRaw()
        seconds = timeDifference.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
#https://docs.python.org/3/library/string.html#format-string-syntax
        duration = '{:02} hours, {:02} minutes, {:02} seconds'.format(hours, minutes, seconds)
        timeDifferenceLine = "<p>Duration of scan: {}</p>".format(duration)

        numberOfUrlsFoundLine = "<p>Number of URLs found = {}</p>".format(len(results))

        urlsScanned = self.scannerResult.getUrlsScanned()
        urlsScannedLines = "<p>Number of URLs scanned = {}</p>".format(len(urlsScanned))

        whichUrlsScannedLines = "<p>URLs scanned: </p>"
        whichUrlsScannedLines += "<ul>"
        for url in urlsScanned:
            whichUrlsScannedLines += "<li><a href = '"+url+"' target='_blank'>"+url+"</a></li>"
        whichUrlsScannedLines += "</ul>"


        '''URLs scanned:
            - https:// jfdka
            - https:// fjksao
            '''

        middle = "<p>URLs found:</p>"

        middle +="<ul>"
    
        lineTemplate = "<li>{} {} [{}] {}</li>"

        for result in results:
            statusCodeLink = self.aTag("https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/{}".format(result.getStatusCode()),str(result.getStatusCode()))
            resultUrlLink = self.aTag(result.getURL(), result.getURL())
            parentUrl = self.aTag(result.getParentUrl(), "parent page")
            if result.getRedirectLocation() != None:
                redirectsTo = "Redirects to: "+self.aTag(result.getRedirectLocation(), result.getRedirectLocation())
            else:
                redirectsTo = ""

            lineInMiddle = lineTemplate.format(statusCodeLink, resultUrlLink, parentUrl, redirectsTo)
            middle += lineInMiddle+"\n"
        
        middle +="</ul>"

        html = top + scannerStartDateLine + timeDifferenceLine + numberOfUrlsFoundLine + urlsScannedLines + whichUrlsScannedLines + middle + bottom
        return html