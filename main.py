from scanner import Scanner
from htmlreporter import HTMLReporter
from browserController import BrowserController
from fileName import FileName

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

fileName = FileName().getHTMLReportFileName()

file = open(fileName, "w")
file.write(HTMLReporter(scanner.getResults()).makeReport())
file.close()

BrowserController().open(fileName)

