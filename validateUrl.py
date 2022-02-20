from urllib.parse import urlparse


class ValidateUrl:
    """Determines whether a url can be scanned and makes the url valid

    This class can make a url valid and can determine whether a url can be scanned

    Typical usage example:

    urlValidator = ValidateUrl(url)
    if not urlValidator.canUrlBeScanned():
        print("url cannot be scanned")

    Attributes:
        url: the url that you want to validate or know if can be scanned
    """
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
