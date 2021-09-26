from scanner import Scanner
from htmlreporter import HTMLReporter

scanner = Scanner('https://keeranrichardson.com')
scanner.scan()

#print(HTMLReporter(scanner.getResults()).makeReport())

file = open("htmlReport.html", "w")
file.write(HTMLReporter(scanner.getResults()).makeReport())
file.close()