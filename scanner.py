from webPage import WebPage
from urlScanner import UrlScanner
from urlResult import UrlResult

class Scanner:
    def __init__(self, url):
        self.url = url
        self.page = WebPage(self.url)
        self.results = ScannerResults()

    def scan(self):
        if self.page.isUrlScannable():
            for aLink in self.page.findLinks():
                link = UrlScanner(aLink)
                print(link.getStatus(), aLink)
                self.results.add(UrlResult(aLink, link.getStatus(), self.url))

    def getResults(self):
        return self.results

class ScannerResults:
    def __init__(self):
        self.results = []

    def add(self, urlResult):
        self.results.append(urlResult)

    def getResults(self):
        return self.results
