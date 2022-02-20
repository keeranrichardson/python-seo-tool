from urlResult import UrlResult

class TestUrlResult:
    
    def testGetParentUrl(self):
        assert None is UrlResult("https://test.com", 200).getParentUrl()
    
    def testAddParentUrl(self):
        url = UrlResult("https://test.com/test", 200)
        url.addParentUrl("https://test.com", "text")
        assert "https://test.com" == url.getParentUrl().url
        assert 1 == len(url.getParentUrls())

    def testAddTwoParentUrls(self):
        url = UrlResult("https://test.com/test", 200)
        url.addParentUrl("https://test.com", "text")
        url.addParentUrl("https://test.com/test2", "text")
        assert 2 == len(url.getParentUrls())
        assert "https://test.com" is url.getParentUrls()[0].url
        assert "https://test.com/test2" is url.getParentUrls()[1].url

    def testOfType(self):
        url = UrlResult("https://test.com/test", 200)
        assert url.isLink()
        url.setUrlAsImage()
        assert url.isImage()
        url.setUrlAsHeadLink()
        assert url.isHeadLink()
        url.setUrlAsIFrame()
        assert url.isIFrame()
        url.setUrlAsScript()
        assert url.isScript()
        