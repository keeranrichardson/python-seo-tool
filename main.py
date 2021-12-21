from requests.models import parse_url
from scanner import Scanner
from htmlreporter import HTMLReporter
from browserController import BrowserController
from configParams import ConfigParams
from folderUtils import FolderUtils
from urllib.parse import urlparse
import os
import tkinter as tk
from tkinterGui import TkinterGui

configParams = ConfigParams()
configParams.getDefaultConfigParams()
urlToParse = configParams.getUrlToParse()

if configParams.isGui():
    gui = TkinterGui()
    gui.showGui()
else:
    if urlToParse == '':
        urlToParse= str(input("enter the url to scan: "))

    if urlToParse == '':
        print("error: This tool needs a url to scan, you did not enter a url")
        exit()

    configParams.setUrl(urlToParse)

    parseUrl = urlparse(urlToParse)
    scanner = Scanner(urlToParse, parseUrl.netloc)
    scanner.scan()

    fileName = configParams.getHTMLReportFileName()

    #creates directory
    directory = "reports"

    reportsFolder = FolderUtils(directory)
    reportsFolder.createCWDFolder()
    path = reportsFolder.getCWDPath()

    #creates full directory
    pathAndFileName = os.path.join(path, fileName)

    #writes report to file
    file = open(pathAndFileName, "w")
    file.write(HTMLReporter(scanner.getResults()).makeReport())
    file.close()

    BrowserController().open(pathAndFileName)

    #todos
