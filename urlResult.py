from collections import namedtuple

class UrlResult:
    def __init__(self, url, statusCode):
        self.url = url
        self.statusCode = statusCode
        self.parentUrls = []
        self.redirectLocation = None

    def getURL(self):
        return self.url

    def getStatusCode(self):
        return self.statusCode
        
    def setStatusCode(self, aStatusCode):
        self.statusCode = aStatusCode

    def getUrlText(self):
        return self.urlText

    def getParentUrl(self):
        return self.parentUrls[0]

    def getParentUrls(self):
        return self.parentUrls

    def setRedirectLocation(self, location):
        self.redirectLocation = location

    def getRedirectLocation(self):
        return self.redirectLocation

    def addParentUrl(self, url, text):
        
        ParentUrlText = namedtuple("ParentUrlText", ["text","url"])
        parentUrlText = ParentUrlText(text, url)
        self.parentUrls.append(parentUrlText)


    

