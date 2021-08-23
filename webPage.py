from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from url import Url

class WebPage:
    def __init__(self, url):
        self.url = url

    def isUrlScannable(self):
        self.statusCode = Url(self.url).getStatus()

        if self.statusCode != 200:
            print("can't find the links for "+ self.url+ " because status code = "+ str(self.statusCode))
            return False

        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")

        return True

    def findLinks(self):
        self.urlsFound = []
        
        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                self.urlsFound.append(href)
                print(href)
        
        return self.urlsFound