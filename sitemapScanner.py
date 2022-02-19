import advertools as adv
# https://advertools.readthedocs.io/en/master/advertools.sitemaps.html

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
            scanner.addUrlToScanAndFoundQueues(url)
