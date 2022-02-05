
class UrlResult:
    def __init__(self, url, statusCode, parentUrl):
        self.url = url
        self.statusCode = statusCode
        self.parentUrls = [parentUrl]
        self.redirectLocation = None

    def getURL(self):
        return self.url

    def getStatusCode(self):
        return self.statusCode
        
    def setStatusCode(self, aStatusCode):
        self.statusCode = aStatusCode

    def getParentUrl(self):
        return self.parentUrls[0]

    def getParentUrls(self):
        return self.parentUrls

    def setRedirectLocation(self, location):
        self.redirectLocation = location

    def getRedirectLocation(self):
        return self.redirectLocation

    def addParentUrl(self, url):
        self.parentUrls.append(url)


    

