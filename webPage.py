from urllib.parse import urljoin
from urllib.parse import urlparse
from collections import namedtuple
from bs4 import BeautifulSoup
import requests
from urlScanner import UrlScanner

class WebPage:
    """Finds the different types of links on a page
    
    This is the class that makes the http request for the HTML of a page and filters the different
    types of links from the HTML.
    
    Typical usage example:
    
    webPage = WebPage(url)
    images = webPage.findImages()

    Attributes:
        url: the url that you want to get the links on
    """
    def __init__(self, url):
        self.url = url
        self.urlScanner = UrlScanner(self.url)
        self.statusCode = self.urlScanner.getStatus()
        self.html = None
        self.soup = None

    def isUrlScannable(self):

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

    def getPage(self):
        if self.html is None:
            self.html = requests.get(self.url, allow_redirects=False, timeout=10).text
        if self.soup is None:
            self.soup = BeautifulSoup(self.html, "html.parser")
        return

    def findLinks(self):
        urlsFound = []

        try:
            self.getPage()

            for link in self.soup.find_all('a'):
                href = link.get('href')

                if href is not None:
                    if len(link.contents) == 0:
                        linkContents = "MISSING"
                    else:
                        linkContents = link.contents[0]
                    LinkTuple = namedtuple("LinkTuple", ["url","text","parentPage"])
                    aLinkTuple = LinkTuple(self.makeFullUrl(self.url,href), linkContents, self.url)
                    urlsFound.append(aLinkTuple)
        except Exception as e:
            print("Exception when trying to find links on " + self.url)
            print(e)

        return urlsFound

    def findImages(self):
        imagesFound = []

        try:
            self.getPage()

            for image in self.soup.find_all('img'):
                source = image.get('src')
                if source is not None:
                    ImageTuple = namedtuple("ImageTuple", ["src","alt","parentPage"])
                    aImageTuple = ImageTuple(self.makeFullUrl(self.url,source), image.get('alt'), self.url)
                    imagesFound.append(aImageTuple)
        except Exception as e:
            print("Exception when trying to find images on " + self.url)
            print(e)

        return imagesFound

    def findHeadLinks(self):
        headLinksFound = []

        try:
            self.getPage()

            for link in self.soup.find_all('link'):
                source = link.get('href')

                if source is not None:
                    HeadLinkTuple = namedtuple("HeadLinkTuple", ["href","rel","type","title","parentPage"])

                    relVal = ""
                    typeVal = ""
                    titleVal = ""
                    if link.get("rel") is not None:
                        relVal = link.get("rel")

                    if link.get("type") is not None:
                        typeVal = link.get("type")

                    if link.get("title") is not None:
                        titleVal = link.get("title")

                    aHeadLinkTuple = HeadLinkTuple(self.makeFullUrl(self.url,source), relVal, typeVal, titleVal, self.url)
                    headLinksFound.append(aHeadLinkTuple)
        except Exception as e:
            print("Exception when trying to find Head links on " + self.url)
            print(e)

        return headLinksFound

    def findScripts(self):
        scriptsFound = []

        try:
            self.getPage()

            for script in self.soup.find_all('script'):
                source = script.get('src')

                if source is not None:
                    ScriptTuple = namedtuple("ScriptTuple", ["src","parentPage"])
                    aScriptTuple = ScriptTuple(self.makeFullUrl(self.url,source), self.url)
                    scriptsFound.append(aScriptTuple)
        except Exception as e:
            print("Exception when trying to find scripts on " + self.url)
            print(e)

        return scriptsFound

    def findIFrames(self):
        iFramesFound = []

        try:
            self.getPage()

            for iFrame in self.soup.find_all('iframe'):
                source = iFrame.get('src')

                if source is not None:
                    IFrameTuple = namedtuple("IFrameTuple", ["src","title","parentPage"])

                    titleVal = ""
                    if iFrame.get("title") is not None:
                        titleVal = iFrame.get("title")

                    aIFrameTuple = IFrameTuple(self.makeFullUrl(self.url,source), titleVal, self.url)
                    iFramesFound.append(aIFrameTuple)
        except Exception as e:
            print("Exception when trying to find iframes on " + self.url)
            print(e)

        return iFramesFound

    def getStatusCode(self):
        return self.statusCode

    def getURL(self):
        return self.url
    