from urllib.parse import urlparse
from scanner import Scanner
from browserController import BrowserController
from configParams import ConfigParams
from tkinterGui import TkinterGui
from reportGenerator import ReportGenerator
from sitemapScanner import SitemapScanner
from validateUrl import ValidateUrl

configParams = ConfigParams()
configParams.getDefaultConfigParams()
urlToParse = configParams.getUrlToParse()

if configParams.isGui() is True:
    gui = TkinterGui(configParams)
    gui.showGui()
else:
    if urlToParse == '':
        urlToParse= str(input("enter the url to scan: "))

    if urlToParse == '':
        print("error: This tool needs a url to scan, you did not enter a url")
        exit()

    urlValidator = ValidateUrl(urlToParse)
    if not urlValidator.canUrlBeScanned():
        urlToParse = urlValidator.tryAndMakeValidUrl()

    urlValidator = ValidateUrl(urlToParse)
    if not urlValidator.canUrlBeScanned():
        print("error: url is not valid " + urlToParse)
        exit()

    configParams.setUrl(urlToParse)

    parseUrl = urlparse(urlToParse)
    scanner = Scanner(urlToParse, parseUrl.netloc)

    scanner.setRateLimitMilliseconds(configParams.getRateLimit())

    # if sitemap, do not crawl urls found
    sitemapScanner = SitemapScanner(urlToParse)
    if sitemapScanner.isSitemap():
        sitemapScanner.addSitemapUrlsToScan(scanner)
        scanner.setCanCrawlUrls(False)

    scanner.scan()

    report = ReportGenerator(configParams, scanner)
    report.generateReport()

    print("Report written to " + report.getPathAndFileName())

    if configParams.getOpenReport():
        BrowserController().open(report.getPathAndFileName())

    #todos
