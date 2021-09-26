from scanner import Scanner
from htmlreporter import HTMLReporter

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

file = open("htmlReport.html", "w")
file.write(HTMLReporter(scanner.getResults()).makeReport())
file.close()