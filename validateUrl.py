from urllib.parse import urlparse


class ValidateUrl:
    """Determines whether a url can be scanned
    and makes the url valid

    This class can make a url valid and can
    determine whether a url can be scanned

    Typical usage example:

    urlValidator = ValidateUrl(url)
    if not urlValidator.canUrlBeScanned():
        print("url cannot be scanned")

    Attributes:
        url: the url that you want to validate
             or know if can be scanned
    """

    def __init__(self, url):
        self.url = url

    def canUrlBeScanned(self):
        """
        Allow scanning when the scheme is present e.g. https://
        And the netloc is present (the domain) e.g. keeranrichardson.com
        """
        parseUrl = urlparse(self.url)
        if parseUrl.netloc != "" and parseUrl.scheme != "":
            return True
        else:
            return False

    def tryAndMakeValidUrl(self):
        """
        If there is no scheme then add https://
        and handle relative Urls by replacing /// characters
        """
        goodUrl = self.url
        parsedUrl = urlparse(goodUrl)
        if parsedUrl.scheme == "":
            goodUrl = "https://" + goodUrl

        goodUrl = goodUrl.replace(":////", "://")
        goodUrl = goodUrl.replace(":///", "://")

        return goodUrl
