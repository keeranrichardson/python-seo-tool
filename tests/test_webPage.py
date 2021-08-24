from webPage import WebPage

class TestWebPage:
    
    def testWebPageScannable(self):
        webPage = WebPage('https://keeranrichardson.com')
        assert True == webPage.isUrlScannable()

    def testWebPageNotScannable(self):
        webPage = WebPage('https://keeranrichardson.com/6')
        assert False == webPage.isUrlScannable()

    def testWebPageError(self):
        webPage = WebPage('')
        assert False == webPage.isUrlScannable()

    def testWebPageMakeFullUrl(self):
        webPage = WebPage('https://keeranrichardson.com')
        assert 'https://keeranrichardson.com/bobdobbs' == webPage.makeFullUrl('https://keeranrichardson.com','/bobdobbs')