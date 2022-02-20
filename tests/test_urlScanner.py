from urlScanner import UrlScanner

class TestUrl:
    
    def testUrlExistsReturn200(self):
        url = UrlScanner('https://keeranrichardson.com')
        assert 200 == url.getStatus()

    def testUrlNotExistsReturn404(self):
        url = UrlScanner('https://keeranrichardson.com/6')
        assert 404 == url.getStatus()

    def testErrorReadingUrl(self):
        url = UrlScanner('')
        assert 'error'==url.getStatus()