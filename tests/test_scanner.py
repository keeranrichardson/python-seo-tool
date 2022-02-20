from scanner import Scanner

class TestScanner:

    def testUrlAddedToQueue(self):
        scanner = Scanner("https://keeranrichardson.com","keeranrichardson.com")
        assert "https://keeranrichardson.com" == scanner.getUrlFromQueue("https://keeranrichardson.com").getURL()

    def testUrlNotInQueueIsNone(self):
        scanner = Scanner("https://keeranrichardson.com","keeranrichardson.com")
        assert None is scanner.getUrlFromQueue("https://notfound.com")
