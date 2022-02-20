import advertools as adv
# https://advertools.readthedocs.io/en/master/advertools.sitemaps.htmldfas
from validateUrl import ValidateUrl


class SitemapScanner:
    def __init__(self, url):
        self.url = url

    def isSitemap(self):
        if self.url.endswith(".xml") or self.url.endswith(".xml.gz"):
            return True
        return False

    def addSitemapUrlsToScan(self, scanner):
        sitemap = adv.sitemap_to_df(self.url)
        urlList = sitemap['loc'].tolist()
        for url in urlList:
            validator = ValidateUrl(url)

            if validator.canUrlBeScanned() is False:
                url = validator.tryAndMakeValidUrl()

            validator = ValidateUrl(url)

            if validator.canUrlBeScanned():
                scanner.addUrlToScanAndFoundQueues(url)
            else:
                print("error: found invalid URL in Sitemap " + url)
