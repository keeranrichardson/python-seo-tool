from webPage import WebPage
from url import Url

class Interface:
    def __init__(self, url):
        self.url = url
        self.page = WebPage(self.url)

    def scan(self):
        if self.page.isUrlScannable():
            for aLink in self.page.findLinks():
                link = Url(aLink)
                print(link.getStatus(), aLink)