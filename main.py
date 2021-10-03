from scanner import Scanner
from htmlreporter import HTMLReporter
from browserController import BrowserController
from fileName import FileName
from folderUtils import FolderUtils
import os

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

fileName = FileName().getHTMLReportFileName()

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

