import requests

'''

Url Scanner issues a head request that allows us
to get information like status code and location.

'''

class UrlScanner:
    def __init__(self, url):
        self.url = url
        self.response = None
        self.location = ''

    def getStatus(self):
        try:
            if self.response is None:
                self.response = requests.head(self.url, allow_redirects=False)
            if self.response.status_code in [301,302,307,308]:
                self.location = self.response.headers['Location']

            return self.response.status_code
        except:
            print("error reading "+ self.url)
            return "error"

    def getLocation(self):
        return self.location