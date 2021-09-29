

class HTMLReporter:
    def __init__(self, scannerResults):
        self.scannerResult = scannerResults
        

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
        middle = ""
        for result in results:
            lineInMiddle = "<li>"+str(result.getStatus())+" <a href = '"+result.url+"' target='_blank'>"+result.url+"</a></li>"
            middle += lineInMiddle+"\n"
        
        html = top+middle+bottom
        return html