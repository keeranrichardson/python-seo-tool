from scanner import Scanner
from htmlreporter import HTMLReporter
from browserController import BrowserController

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

fileName = str(input("enter the name of html report file"))+".html"
file = open(fileName, "w")
file.write(HTMLReporter(scanner.getResults()).makeReport())
file.close()

BrowserController().open(fileName)

