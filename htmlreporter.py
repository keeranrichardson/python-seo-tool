
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
                        <ul>
                        '''
        bottom = '''
                        </ul>
                    </body>
                </html>'''
        scannerStartDateLine = "<h2>Date and time of scan: "+self.scannerResult.getStartDateTime()+"</h2>\n"
        numberOfUrlsFound = str(len(results))
        numberOfUrlsFoundLine = "<p>Number of URLs found = "+numberOfUrlsFound+"</p>"
        middle = ""
        for result in results:
            statusCodeLink = self.aTag("https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/"+str(result.getStatusCode()),str(result.getStatusCode()))
            resultUrlLink = self.aTag(result.getURL(), result.getURL())

            lineInMiddle = "<li>"+statusCodeLink+" "+resultUrlLink+"</li>"
            middle += lineInMiddle+"\n"
        
        html = top+scannerStartDateLine+numberOfUrlsFoundLine+middle+bottom
        return html