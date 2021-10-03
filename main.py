from scanner import Scanner
from htmlreporter import HTMLReporter
from browserController import BrowserController
from fileName import FileName
import os

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

fileName = FileName().getHTMLReportFileName()

directory = "reports"
parentDir = os.getcwd() #gets current working director
path = os.path.join(parentDir, directory)
try:
    os.mkdir(path)
except OSError as error:
    pass

pathAndFileName = os.path.join(path, fileName)

file = open(pathAndFileName, "w")
file.write(HTMLReporter(scanner.getResults()).makeReport())
file.close()

BrowserController().open(pathAndFileName)

