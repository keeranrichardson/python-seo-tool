from collections import namedtuple

class UrlResult:
    def __init__(self, url, statusCode):
        self.url = url
        self.statusCode = statusCode
        self.parentUrls = []
        self.redirectLocation = None
        self.isOfType = "link"
        self.isUrlInternal = True


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

    def addParentUrl(self, url, text):
        if text == None:
            text = ''
        ParentUrlText = namedtuple("ParentUrlText", ["text","url"])
        parentUrlText = ParentUrlText(text, url)
        self.parentUrls.append(parentUrlText)

    def setUrlAsImage(self):
        self.isOfType = "image"
    
    def setUrlAsHeadLink(self):
        self.isOfType = "headlink"

    def setUrlAsScript(self):
        self.isOfType = "script"

    def setIsInternal(self, internal):
        self.isUrlInternal = internal

    def isInternal(self):
        return self.isUrlInternal        

    def isA(self):
        return self.isOfType

    def isImage(self):
        return (self.isOfType == "image")

    def isLink(self):
        return (self.isOfType == "link")

    def isHeadLink(self):
        return (self.isOfType == "headlink")

    def isScript(self):
        return (self.isOfType == "script")


    

