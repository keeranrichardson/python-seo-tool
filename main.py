from scanner import Scanner
from htmlreporter import HTMLReporter
from browserController import BrowserController
import datetime
import re

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

fileName = str(input("enter the name of html report file, default file name = "+now))

fileName = re.sub('[^A-Za-z0-9_\-\.]+', '', fileName)+'.html'

if fileName == '.html':
    fileName = now+'.html'

file = open(fileName, "w")
file.write(HTMLReporter(scanner.getResults()).makeReport())
file.close()

BrowserController().open(fileName)

