import requests


class UrlScanner:
    """Gets the status code and location of a link

    Url Scanner issues a head request that allows us
    to get information like status code and location.

    Typical usage example:

    urlScanner = UrlScanner(url)
    redirectLocation = urlScanner.getLocation()

    Attributes:
        url: the url that you want the status code or location of
    """

    def __init__(self, url):
        self.url = url
        self.response = None
        self.location = ""

    def getStatus(self):
        """
        Make an HTTP HEAD request on the url to get
        the status code and any important headers.
        Currently only use the Location header for
        redirect status codes
        """
        try:
            if self.response is None:
                self.response = requests.head(
                    self.url, allow_redirects=False, timeout=10
                )
            if self.response.status_code in [301, 302, 307, 308]:
                self.location = self.response.headers["Location"]

            return self.response.status_code
        except Exception as e:
            print("Exception when trying to HEAD request on " + self.url)
            print(e)
            return "error"

    def getLocation(self):
        return self.location
