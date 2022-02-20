import advertools as adv
# https://advertools.readthedocs.io/en/master/advertools.sitemaps.htmldfas
from validateUrl import ValidateUrl


class SitemapScanner:
    """Loads and finds all links in sitemaps
    
    This class determines whether a link is a sitemap and adds the urls found
    on a sitemap to be scanned by a Scanner object.
    
    Typical usage example:
    
    sitemapScanner = SitemapScanner("https://mywebsite.com/sitemap.xml")
    if sitemapScanner.isSitemap():
        sitemapScanner.addSitemapUrlsToScan(scanner)

    Attributes:
        url: The url that is being scanned
    """
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
