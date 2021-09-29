import datetime
import re

class FileName:
    def __init__(self):
        ''

    def getHTMLReportFileName(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

        fileName = str(input("enter the name of html report file, default file name = "+now))

        fileName = re.sub('[^A-Za-z0-9_\-\.]+', '', fileName)+'.html'

        if fileName == '.html':
            fileName = now+'.html'

        return fileName

#todo: add unit tests
#todo: default to /reports folder and store reports in default folder