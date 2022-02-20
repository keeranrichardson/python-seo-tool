from urllib.parse import urlparse


class ValidateUrl:
    def __init__(self, url):
        self.url = url

    def canUrlBeScanned(self):
        parseUrl = urlparse(self.url)
        if parseUrl.netloc != '' and parseUrl.scheme != '':
            return True
        else:
            return False

    def tryAndMakeValidUrl(self):
        goodUrl = self.url
        parsedUrl = urlparse(goodUrl)
        if parsedUrl.scheme == '':
            goodUrl = "https://" + goodUrl

        goodUrl = goodUrl.replace(":////", "://")
        goodUrl = goodUrl.replace(":///", "://")

        return goodUrl
