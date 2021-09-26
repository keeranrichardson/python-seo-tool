from webPage import WebPage
from url import Url

class Scanner:
    def __init__(self, url):
        self.url = url
        self.page = WebPage(self.url)
        self.results = ScannerResults()

    def scan(self):
        if self.page.isUrlScannable():
            for aLink in self.page.findLinks():
                link = Url(aLink)
                print(link.getStatus(), aLink)
                self.results.add(link)

    def getResults(self):
        return self.results

class ScannerResults:
    def __init__(self):
        self.results = []

    def add(self, link):
        self.results.append(link)

    def getResults(self):
        return self.results
