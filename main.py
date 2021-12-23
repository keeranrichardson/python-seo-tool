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
from reportGenerator import ReportGenerator

configParams = ConfigParams()
configParams.getDefaultConfigParams()
urlToParse = configParams.getUrlToParse()

if configParams.isGui():
    gui = TkinterGui(configParams)
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
    
    report = ReportGenerator(configParams, scanner)
    report.generateReport()

    BrowserController().open(report.getPathAndFileName())

    #todos
