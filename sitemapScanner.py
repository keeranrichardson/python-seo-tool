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
        """
        checks if the url is a sitemap
        """
        if self.url.endswith(".xml") or self.url.endswith(".xml.gz"):
            return True
        return False

    def addSitemapUrlsToScan(self, scanner):
        """
        adds the urls from the sitemap to the scan queue
        """
        # use advertools to get and process the sitemap file
        sitemap = adv.sitemap_to_df(self.url)
        # get the location values from the sitemap
        urlList = sitemap["loc"].tolist()

        # for each url, validate it and add valid URLs
        # to the scanner for processing
        for url in urlList:
            validator = ValidateUrl(url)

            if validator.canUrlBeScanned() is False:
                url = validator.tryAndMakeValidUrl()

            validator = ValidateUrl(url)

            if validator.canUrlBeScanned():
                scanner.addUrlToScanAndFoundQueues(url)
            else:
                print("error: found invalid URL in Sitemap " + url)
