import datetime
import re
import argparse

class ConfigParams:
    """Module to store all configuration parameters

    read parameters from command line with defaults if parameters are missing eg:

    python main.py -url https://keeranrichardson.com -cmd true

    or

    python main.py -url https://keeranrichardson.com -cmd=True
    
    Typical usage example:
    
    configParams = ConfigParams()
    configParams.getDefaultConfigParams()
    urlToParse = configParams.getUrlToParse()
    """
    def __init__(self):
        self.vargs = {}

    def getHTMLReportFileName(self):
        now = self.getCurrentDateString()

        # if the filename has not been configured prompt the user to input one

        if self.vargs["filename"] is None:
            fileName = str(input("enter the name of html report file, default file name = "+now+" "))
        else:
            fileName = self.vargs["filename"]

        fileName = self.getAsHtmlFileName(fileName)

        return fileName

    def getUrlToParse(self):

        # if the url has been configured, return it without any spaces at the start or end. Else return an empty string

        if self.vargs["url"] is not None:
            urlToReturn = self.vargs["url"]
        else:
            urlToReturn = ''

        return urlToReturn.strip()

    def getRateLimit(self):
        # Return the ratelimit value
        return self.vargs["rateLimit"]

    def getOpenReport(self):
        # return the boolean for whether the HTML report opens in default browser by default
        return bool(self.vargs["openReport"])

    def getDefaultConfigParams(self):
        # calls function that reads command line parameters for config
        self.getConfigParamsFromCommandLineArguments()

        return

    def ensureBooleanValue(self, aValue):

        # if it is a boolean return it
        if isinstance(aValue,(int)):
            return aValue

        return aValue.lower()=="true"


    def getConfigParamsFromCommandLineArguments(self):
        # reads command line parameters for config
        # defines the command line parameters, defaults and what is displayed when -help is used
        parser = argparse.ArgumentParser(description='Scan site for URLs')
        parser.add_argument('-url', help='the url to scan')
        parser.add_argument('-filename', default=self.getCurrentDateString(), help='the filename of the html report output file')
        parser.add_argument('-cmd', default=False, help='run the program from the command line')
        parser.add_argument('-reportPath', default='', help='path where HTML report will be stored')
        parser.add_argument('-rateLimit', default=0, help='milliseconds to wait between scans')
        parser.add_argument('-openReport', default=True, help='automatically opens report when finished')

        args = parser.parse_args()
        self.vargs = vars(args)

        # argsparse returns String from command line, but boolean from defaults
        self.vargs["cmd"] = self.ensureBooleanValue(self.vargs["cmd"])
        self.vargs["openReport"] = self.ensureBooleanValue(self.vargs["openReport"])

        print(args)

    def getCurrentDateString(self):
        # returns current date and time in the format year-month-day-hour-minute-second
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def getAsHtmlFileName(self, fileNameStr):

        # if user inputted filename with .html already at the end, do not add .html to the end
        suffix = ".html"
        if fileNameStr.endswith(suffix):
            suffix = ''

        # https://docs.python.org/3/library/re.html
        # https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
        # use a regular expression to filter out any invalid filename characters

        fileName = re.sub('[^A-Za-z0-9_\\-\\.]+', '', fileNameStr)+suffix

        # if trimmed filename is empty, then make the filename the default as the current date and time
        if fileName == '.html':
            fileName = self.getCurrentDateString()+'.html'

        return fileName

    def isGui(self):

        return not self.vargs["cmd"]

    def setUrl(self, urlToParse):
        self.vargs["url"] = urlToParse

    def getReportPath(self):
        return self.vargs["reportPath"]

    def setReportPath(self, newPath):
        self.vargs["reportPath"] = newPath

    def setReportFileName(self, newFileName):
        self.vargs["filename"] = newFileName

    def setRateLimit(self, rateLimit):
        self.vargs["rateLimit"] = rateLimit
