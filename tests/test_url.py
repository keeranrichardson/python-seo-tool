from url import Url

class TestUrl:
    
    def testUrlExistsReturn200(self):
        url = Url('https://keeranrichardson.com')
        assert 200 == url.getStatus()

    def testUrlNotExistsReturn404(self):
        url = Url('https://keeranrichardson.com/6')
        assert 404 == url.getStatus()

    def testErrorReadingUrl(self):
        url = Url('')
        assert 'error'==url.getStatus()