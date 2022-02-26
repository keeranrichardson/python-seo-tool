from urllib.parse import urlparse
from scanner import Scanner
from browserController import BrowserController
from configParams import ConfigParams
from tkinterGui import TkinterGui
from reportGenerator import ReportGenerator
from sitemapScanner import SitemapScanner
from validateUrl import ValidateUrl

"""The file that you run to start the tool

This can be run in two ways either as a command line application or as a tkinter GUI.
You can control this by adding parameters to the command used to run this file.

options:
  -h, --help             show this help message and exit
  -url URL               the url to scan
  -filename FILENAME     the filename of the html report output file
  -cmd CMD               run the program from the command line
  -reportPath REPORTPATH path where HTML report will be stored              
  -rateLimit RATELIMIT   milliseconds to wait between scans
  -openReport OPENREPORT automatically opens report when finished

Typical usage examples:

To run command line app

python main.py -url https://keeranrichardson.com -rateLimit 1000 -cmd True

To run tkinter GUI

python main.py -url https://keeranrichardson.com -rateLimit 1000 -cmd False

By default the GUI will be displayed

Minimum configuration is:

python main.py

"""

# stores the configuration parameters
# from the commmand line
configParams = ConfigParams()
configParams.getDefaultConfigParams()
urlToParse = configParams.getUrlToParse()

# if the user has configured the tool to
# run through the GUI then start tkinter
if configParams.isGui() is True:
    gui = TkinterGui(configParams)
    gui.showGui()
else:
    # if the user did not enter a URL at first then
    # prompt the user to enter a url now
    if urlToParse == "":
        urlToParse = str(input("enter the url to scan: "))

    # if the user still did not enter a URL, then close the application
    if urlToParse == "":
        print("error: This tool needs a url to scan, you did not enter a url")
        exit()

    # check if the url is valid, if not,
    # try and make it valid
    urlValidator = ValidateUrl(urlToParse)
    if not urlValidator.canUrlBeScanned():
        urlToParse = urlValidator.tryAndMakeValidUrl()

    # if the url is still not valid then exit
    # the application and print an error message
    urlValidator = ValidateUrl(urlToParse)
    if not urlValidator.canUrlBeScanned():
        print("error: url is not valid " + urlToParse)
        exit()

    configParams.setUrl(urlToParse)

    # create a scanner object with the url and the network location
    parseUrl = urlparse(urlToParse)
    scanner = Scanner(urlToParse, parseUrl.netloc)

    scanner.setRateLimitMilliseconds(configParams.getRateLimit())

    # if the url is a sitemap set the tool to
    # only scan the urls, not crawl them
    sitemapScanner = SitemapScanner(urlToParse)
    if sitemapScanner.isSitemap():
        sitemapScanner.addSitemapUrlsToScan(scanner)
        scanner.setCanCrawlUrls(False)

    # start the scan
    scanner.scan()

    # generate the HTML report
    report = ReportGenerator(configParams, scanner)
    report.generateReport()

    print("Report written to " + report.getPathAndFileName())

    # if th euser has configures the scan to automatically open report,
    # then open the html report in their default browser
    if configParams.getOpenReport():
        BrowserController().open(report.getPathAndFileName())
