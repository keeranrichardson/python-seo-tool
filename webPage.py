from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urlScanner import UrlScanner

class WebPage:
    def __init__(self, url):
        self.url = url

    def isUrlScannable(self):
        self.statusCode = UrlScanner(self.url).getStatus()

        if self.statusCode != 200:
            print("can't find the links for "+ self.url+ " because status code = "+ str(self.statusCode))
            return False

        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")

        return True

    def makeFullUrl(self, base, end):
        return urljoin(base, end)

    def findLinks(self):
        self.urlsFound = []
        
        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                self.urlsFound.append(self.makeFullUrl(self.url,href))
        
        return self.urlsFound
    
    def findImages(self):
        self.imagesFound = []

        for image in self.soup.find_all('img'):
            source = image.get('scr')
            if source is not None:
                self.imagesFound.append(self.makeFullUrl(self.url,source))
        
        return self.imagesFound

    