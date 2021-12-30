
class UrlResult:
    def __init__(self, url, statusCode, parentUrl):
        self.url = url
        self.statusCode = statusCode
        self.parentUrl = parentUrl

    def getURL(self):
        return self.url

    def getStatusCode(self):
        return self.statusCode
        
    def setStatusCode(self, aStatusCode):
        self.statusCode = aStatusCode

    def getParentUrl(self):
        return self.parentUrl

    def setRedirectLocation(self, location):
        self.redirectLocation = location

    

