from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from urllib.parse import urlparse
from urlScanner import UrlScanner
from collections import namedtuple

class WebPage:
    def __init__(self, url):
        self.url = url
        self.urlScanner = UrlScanner(self.url)

    def isUrlScannable(self):
        self.statusCode = self.urlScanner.getStatus()

        validStatusCodes = [
                            200,    # OK
                            301,    # Permanent redirect
                            302,    # Temporary redirect
                            307,
                            308
                            ]

        if self.statusCode not in validStatusCodes:
            print("can't find the links for "+ self.url+ " because status code = "+ str(self.statusCode))
            return False


        return True

    def getRedirectLocation(self):
        redirectLocation = self.urlScanner.getLocation()
        parsedUrl = urlparse(redirectLocation)
        if parsedUrl.scheme == '':
            redirectLocation = self.makeFullUrl(self.url, redirectLocation)

        return redirectLocation

    def makeFullUrl(self, base, end):
        return urljoin(base, end)

    def findLinks(self):
        self.urlsFound = []
        # todo: find links must be called before find images
        self.html = requests.get(self.url, allow_redirects=False).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        
        for link in self.soup.find_all('a'):
            href = link.get('href')
            # todo: report if href is none
            if href is not None:
                LinkTuple = namedtuple("LinkTuple", ["url","text","parentPage"])
                aLinkTuple = LinkTuple(self.makeFullUrl(self.url,href), link.contents[0], self.url)
                self.urlsFound.append(aLinkTuple)
        
        return self.urlsFound
    
    def findImages(self):
        self.imagesFound = []

        for image in self.soup.find_all('img'):
            source = image.get('src')
            # todo: report if src is none
            if source is not None:
                ImageTuple = namedtuple("ImageTuple", ["src","alt","parentPage"])
                aImageTuple = ImageTuple(self.makeFullUrl(self.url,source), image.get('alt'), self.url)
                self.imagesFound.append(aImageTuple)
        
        return self.imagesFound

    def findHeadLinks(self):
        self.headLinksFound = []

        for link in self.soup.find_all('link'):
            source = link.get('href')
            # todo: report if href is none
            if source is not None:
                HeadLinkTuple = namedtuple("HeadLinkTuple", ["href","rel","type","title","parentPage"])

                relVal = ""
                typeVal = ""
                titleVal = ""
                if link.get("rel") != None:
                    relVal = link.get("rel")
                
                if link.get("type") != None:
                    typeVal = link.get("type")

                if link.get("title") != None:
                    titleVal = link.get("title")

                aHeadLinkTuple = HeadLinkTuple(self.makeFullUrl(self.url,source), relVal, typeVal, titleVal, self.url)
                self.headLinksFound.append(aHeadLinkTuple)
        
        return self.headLinksFound

    def findScripts(self):
        self.scriptsFound = []

        for script in self.soup.find_all('script'):
            source = script.get('src')
            # todo: report if src is none
            if source is not None:
                ScriptTuple = namedtuple("ScriptTuple", ["src","parentPage"])
                aScriptTuple = ScriptTuple(self.makeFullUrl(self.url,source), self.url)
                self.scriptsFound.append(aScriptTuple)
        
        return self.scriptsFound

    def getStatusCode(self):
        return self.statusCode

    def getURL(self):
        return self.url
    