import requests

class UrlScanner:
    def __init__(self, url):
        self.url = url
        self.response = None

    def getStatus(self):
        try:
            if self.response is None:
                self.response = requests.head(self.url)
            return self.response.status_code
        except:
            print("error reading "+ self.url)
            return "error"

    def isScannable(self):
        if self.getStatus() != 200:
            return False
        else:
            return True