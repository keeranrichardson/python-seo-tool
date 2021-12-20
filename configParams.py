import datetime
import re
import argparse

# read prameters from command line with defaults if parameters are missing eg:
# python main.py -url https://keeranrichardson.com -cmd true
# or
# python main.py -url https://keeranrichardson.com -cmd=True 

class ConfigParams:
    def __init__(self):
        self.vargs = {}

    def getHTMLReportFileName(self):
        now = self.getCurrentDateString()

        if self.vargs["filename"] is None:
            fileName = str(input("enter the name of html report file, default file name = "+now+" "))
        else:
            fileName = self.vargs["filename"]

        fileName = self.getAsHtmlFileName(fileName)

        return fileName

    def getUrlToParse(self):

        if self.vargs["url"] is not None:
            urlToReturn = self.vargs["url"]
        else:
            urlToReturn = ''

        return urlToReturn.strip()

    def getDefaultConfigParams(self):
        self.getConfigParamsFromCommandLineArguments()

        return

    def getConfigParamsFromCommandLineArguments(self):
        parser = argparse.ArgumentParser(description='Scan site for URLs')
        parser.add_argument('-url', help='the url to scan')
        parser.add_argument('-filename', default=self.getCurrentDateString(), help='the filename of the html report output file')
        parser.add_argument('-cmd', default=False, help='run the program from the command line')

        self.args = parser.parse_args()
        self.vargs = vars(self.args)
        print(self.args)

    def getCurrentDateString(self):

        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def getAsHtmlFileName(self, fileNameStr):
        suffix = ".html"
        if fileNameStr.endswith(suffix):
            suffix = ''

        fileName = re.sub('[^A-Za-z0-9_\-\.]+', '', fileNameStr)+suffix

        if fileName == '.html':
            fileName = self.getCurrentDateString()+'.html'

        return fileName

    def isGui(self):
        return not self.vargs["cmd"]

    def setUrl(self, urlToParse):
        self.vargs["url"] = urlToParse

        


#todo: add unit tests
#todo: default to /reports folder and store reports in default folder